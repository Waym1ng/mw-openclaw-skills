"""
柏拉图平台 Provider 实现（标准库版本）
使用适配器模式支持多种模型
"""
import json
import urllib.request
import urllib.error
from typing import Optional

from ..schema import ImageGenerationRequest, ImageGenerationResult
from .base import BaseProvider
from ..models.blt_adapters import build_request
from ..utils.param_mapper import normalize_size_and_ratio
from ..utils.config_loader import get_config


class BltProvider(BaseProvider):
    """柏拉图平台图像生成 Provider"""

    name = "blt"

    def __init__(self):
        """初始化 Provider"""
        self.config = get_config()
        self.api_base_url = self.config.get_blt_base_url()
        self.api_endpoint = "/v1/images/generations"
        self.api_url = f"{self.api_base_url}{self.api_endpoint}"

    async def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        """
        生成图片

        Args:
            request: 统一的图像生成请求

        Returns:
            ImageGenerationResult: 生成结果
        """
        try:
            # 标准化参数
            size, aspect_ratio = normalize_size_and_ratio(
                request.size, request.aspect_ratio
            )

            # 构建请求数据
            request_data = {
                "model": request.model or self.config.get_default_model(),
                "prompt": request.prompt,
                "size": size,
                "aspect_ratio": aspect_ratio,
                "n": request.n,
            }

            # 添加图片 URL
            if request.image_urls:
                request_data["image"] = request.image_urls

            # 使用适配器构建最终请求参数
            payload = build_request(request_data)

            # 发送 API 请求（同步方式）
            api_response = self._call_api(payload)

            # 解析响应
            return self._parse_response(api_response, request.model)

        except Exception as e:
            return ImageGenerationResult(
                success=False,
                images=[],
                provider=self.name,
                model=request.model,
                message=f"BltProvider 错误: {str(e)}"
            )

    def _call_api(self, payload: dict) -> dict:
        """
        调用柏拉图 API

        Args:
            payload: 请求参数

        Returns:
            dict: API 响应

        Raises:
            RuntimeError: HTTP 请求错误
        """
        # 从配置文件或环境变量获取 API Key
        api_key = self.config.get_blt_api_key()
        if not api_key:
            raise ValueError("未设置 BLT_API_KEY 环境变量或配置文件")

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
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"柏拉图 API 请求失败 ({e.code}): {error_msg}") from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"柏拉图 API 连接失败: {e.reason}") from e

    def _parse_response(
        self,
        api_response: dict,
        model: Optional[str]
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
            # 提取图片 URL
            if api_response.get("data") and len(api_response["data"]) > 0:
                images = [
                    item.get("url", "")
                    for item in api_response["data"]
                    if item.get("url")
                ]

                return ImageGenerationResult(
                    success=True,
                    images=images,
                    provider=self.name,
                    model=model,
                    raw_response=api_response
                )
            else:
                return ImageGenerationResult(
                    success=False,
                    images=[],
                    provider=self.name,
                    model=model,
                    message="API 响应中未包含图片数据"
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
