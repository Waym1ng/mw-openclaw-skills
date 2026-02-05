"""
GrsAI 平台 Provider 实现（标准库版本）
支持多端点映射
"""
import json
import urllib.request
import urllib.error
from typing import Optional

from ..schema import ImageGenerationRequest, ImageGenerationResult
from .base import BaseProvider
from ..models.grsai_mapper import (
    get_endpoint_for_model,
    is_nano_banana_endpoint,
    is_completions_endpoint
)
from ..utils.param_mapper import normalize_size_and_ratio
from ..utils.config_loader import get_config


class GrsaiProvider(BaseProvider):
    """GrsAI 平台图像生成 Provider"""

    name = "grsai"

    def __init__(self):
        """初始化 Provider"""
        self.config = get_config()
        self.api_base_url = self.config.get_grsai_base_url()
        self.api_url = None

    async def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        """
        生成图片

        Args:
            request: 统一的图像生成请求

        Returns:
            ImageGenerationResult: 生成结果
        """
        try:
            # 获取模型
            model = request.model or self.config.get_default_model()

            # 获取端点
            endpoint = get_endpoint_for_model(model)
            self.api_url = f"{self.api_base_url}{endpoint}"

            # 标准化参数
            size, aspect_ratio = normalize_size_and_ratio(
                request.size, request.aspect_ratio
            )

            # 根据端点类型构建请求
            if is_nano_banana_endpoint(model):
                payload = self._build_nano_banana_payload(
                    request, aspect_ratio
                )
            elif is_completions_endpoint(model):
                payload = self._build_completions_payload(
                    request, size
                )
            else:
                raise ValueError(f"未知的端点: {endpoint}")

            # 发送 API 请求（同步方式）
            api_response = self._call_api(payload)

            # 解析响应
            return self._parse_response(api_response, model)

        except Exception as e:
            return ImageGenerationResult(
                success=False,
                images=[],
                provider=self.name,
                model=request.model,
                message=f"GrsaiProvider 错误: {str(e)}"
            )

    def _build_nano_banana_payload(
        self,
        request: ImageGenerationRequest,
        aspect_ratio: str
    ) -> dict:
        """
        构建 nano-banana 端点的请求参数

        Args:
            request: 统一请求
            aspect_ratio: 宽高比

        Returns:
            dict: 请求参数
        """
        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "aspectRatio": aspect_ratio,
            "shutProgress": True  # 关闭进度回复
        }

        # 添加图片 URL
        if request.image_urls:
            payload["urls"] = request.image_urls

        return payload

    def _build_completions_payload(
        self,
        request: ImageGenerationRequest,
        size: str
    ) -> dict:
        """
        构建 completions 端点的请求参数

        Args:
            request: 统一请求
            size: 图片尺寸

        Returns:
            dict: 请求参数
        """
        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "size": size,
            "variants": request.n,
            "shutProgress": True  # 关闭进度回复
        }

        # 添加图片 URL
        if request.image_urls:
            payload["urls"] = request.image_urls

        return payload

    def _call_api(self, payload: dict) -> dict:
        """
        调用 GrsAI API

        Args:
            payload: 请求参数

        Returns:
            dict: API 响应

        Raises:
            RuntimeError: HTTP 请求错误
        """
        # 从配置文件或环境变量获取 API Key
        api_key = self.config.get_grsai_api_key()
        if not api_key:
            raise ValueError("未设置 GRSAI_API_KEY 环境变量或配置文件")

        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        req = urllib.request.Request(
            self.api_url,
            method="POST",
            headers=headers,
            data=body
        )

        timeout = self.config.get_timeout()

        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                # GrsAI 返回 SSE 流式响应，需要解析
                response_text = resp.read().decode("utf-8")
                return self._parse_sse_response(response_text)
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GrsAI API 请求失败 ({e.code}): {error_msg}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"GrsAI API 连接失败: {e.reason}") from e

    def _parse_sse_response(self, response_text: str) -> dict:
        """
        解析 SSE 流式响应

        Args:
            response_text: SSE 响应文本

        Returns:
            dict: 解析后的 JSON 数据
        """
        lines = response_text.strip().split('\n')
        valid_result = None

        for line in lines:
            line = line.strip()
            if line.startswith('data: '):
                json_str = line.replace('data: ', '').strip()
                # 跳过结束标记
                if json_str == '[DONE]':
                    continue
                # 解析 JSON，使用最后一个有效的结果
                try:
                    valid_result = json.loads(json_str)
                except json.JSONDecodeError:
                    continue

        if valid_result:
            return valid_result
        else:
            # 如果没有找到有效的 data: 前缀，尝试直接解析整个响应
            return json.loads(response_text.strip())

    def _parse_response(
        self,
        api_response: dict,
        model: str
    ) -> ImageGenerationResult:
        """
        解析 API 响应

        Args:
            api_response: API 返回的原始响应
            model: 使用的模型名称

        Returns:
            ImageGenerationResult: 统一格式的结果
        """
        try:
            # 检查任务状态
            if api_response.get("status") == "succeeded":
                # 兼容 results 数组
                results = api_response.get("results")
                if results and isinstance(results, list):
                    images = [
                        r.get("url", "")
                        for r in results
                        if r.get("url")
                    ]
                else:
                    # 尝试获取 url 字段（completions 端点的旧参数）
                    url = api_response.get("url")
                    images = [url] if url else []

                return ImageGenerationResult(
                    success=True,
                    images=images,
                    provider=self.name,
                    model=model,
                    raw_response=api_response
                )

            elif api_response.get("status") == "failed":
                message = api_response.get("failure_reason", "")
                error = api_response.get("error", "")
                return ImageGenerationResult(
                    success=False,
                    images=[],
                    provider=self.name,
                    model=model,
                    message=f"API 失败: {message} {error}"
                )

            elif api_response.get("code") == -1:
                return ImageGenerationResult(
                    success=False,
                    images=[],
                    provider=self.name,
                    model=model,
                    message=api_response.get("msg", "未知错误")
                )

            else:
                return ImageGenerationResult(
                    success=False,
                    images=[],
                    provider=self.name,
                    model=model,
                    message=f"未知状态: {api_response.get('status')}"
                )

        except Exception as e:
            return ImageGenerationResult(
                success=False,
                images=[],
                provider=self.name,
                model=model,
                message=f"解析响应失败: {str(e)}",
                raw_response=api_response
            )
