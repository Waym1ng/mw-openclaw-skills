"""
GrsAI 平台模型到端点映射
复用参考代码的端点映射逻辑
"""
from typing import Dict, Optional
from enum import Enum


class GrsaiEndpoint(str, Enum):
    """GrsAI API 端点枚举"""
    COMPLETIONS = "/v1/draw/completions"
    NANO_BANANA = "/v1/draw/nano-banana"


# === 模型到端点映射 ===
MODEL_ENDPOINT_MAPPING: Dict[str, str] = {
    # /v1/draw/completions 端点
    "sora-image": GrsaiEndpoint.COMPLETIONS,
    "gpt-image-1.5": GrsaiEndpoint.COMPLETIONS,
    
    # /v1/draw/nano-banana 端点
    "nano-banana-fast": GrsaiEndpoint.NANO_BANANA,
    "nano-banana": GrsaiEndpoint.NANO_BANANA,
    "nano-banana-pro": GrsaiEndpoint.NANO_BANANA,
    "nano-banana-pro-vt": GrsaiEndpoint.NANO_BANANA,
    "nano-banana-pro-cl": GrsaiEndpoint.NANO_BANANA,
    "nano-banana-pro-vip": GrsaiEndpoint.NANO_BANANA,
    "nano-banana-pro-4k-vip": GrsaiEndpoint.NANO_BANANA,
}


def get_endpoint_for_model(model: str) -> str:
    """
    获取模型对应的 API 端点
    
    Args:
        model: 模型名称
        
    Returns:
        str: API 端点路径
        
    Raises:
        ValueError: 如果模型不支持
    """
    endpoint = MODEL_ENDPOINT_MAPPING.get(model)
    if not endpoint:
        supported = ", ".join(MODEL_ENDPOINT_MAPPING.keys())
        raise ValueError(
            f"不支持的模型: {model}，"
            f"支持的模型: {supported}"
        )
    return endpoint


def get_supported_models() -> list:
    """返回所有支持的模型名称"""
    return list(MODEL_ENDPOINT_MAPPING.keys())


def is_nano_banana_endpoint(model: str) -> bool:
    """检查模型是否使用 nano-banana 端点"""
    return MODEL_ENDPOINT_MAPPING.get(model) == GrsaiEndpoint.NANO_BANANA


def is_completions_endpoint(model: str) -> bool:
    """检查模型是否使用 completions 端点"""
    return MODEL_ENDPOINT_MAPPING.get(model) == GrsaiEndpoint.COMPLETIONS
