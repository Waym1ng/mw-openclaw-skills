"""
统一的图像生成请求 Schema（标准库版本）
定义标准化的输入参数结构
"""
import json
from typing import Optional, List, Dict, Any


class ImageGenerationRequest:
    """图像生成请求的统一数据结构"""

    def __init__(
        self,
        prompt: str,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        size: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        n: int = 1,
        image_urls: Optional[List[str]] = None,
        **kwargs
    ):
        self.prompt = prompt
        self.model = model
        self.provider = provider
        self.size = size
        self.aspect_ratio = aspect_ratio
        self.n = n
        self.image_urls = image_urls or []
        self.extra_params = kwargs

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "prompt": self.prompt,
            "model": self.model,
            "provider": self.provider,
            "size": self.size,
            "aspect_ratio": self.aspect_ratio,
            "n": self.n,
            "image_urls": self.image_urls,
            **self.extra_params
        }


class ImageGenerationResult:
    """图像生成结果的统一数据结构"""

    def __init__(
        self,
        success: bool,
        images: Optional[List[str]] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        message: Optional[str] = None,
        raw_response: Optional[Dict[str, Any]] = None
    ):
        self.success = success
        self.images = images or []
        self.provider = provider
        self.model = model
        self.message = message
        self.raw_response = raw_response

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "images": self.images,
            "provider": self.provider,
            "model": self.model,
            "message": self.message
        }
