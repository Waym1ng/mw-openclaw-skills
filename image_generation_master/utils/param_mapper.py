"""
参数映射工具
处理 size 和 aspect_ratio 之间的自动转换
"""
from typing import Optional, Tuple


def normalize_size_and_ratio(
    size: Optional[str] = None,
    aspect_ratio: Optional[str] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    标准化 size 和 aspect_ratio 参数
    
    当只提供其中一个时，自动推断另一个值
    
    Args:
        size: 图片尺寸，如 "1024x1024"
        aspect_ratio: 宽高比，如 "16:9", "1:1"
    
    Returns:
        Tuple[size, aspect_ratio]: 标准化后的 (size, aspect_ratio)
    
    Examples:
        >>> normalize_size_and_ratio(aspect_ratio="16:9")
        ("1366x768", "16:9")
        
        >>> normalize_size_and_ratio(size="1024x1024")
        ("1024x1024", "1:1")
    """
    # 如果两者都有，直接返回
    if size and aspect_ratio:
        return size, aspect_ratio
    
    # 都没有，返回默认值
    if not size and not aspect_ratio:
        return "1024x1024", "1:1"
    
    # 只有 aspect_ratio，推断 size
    if aspect_ratio and not size:
        size = _aspect_ratio_to_size(aspect_ratio)
        return size, aspect_ratio
    
    # 只有 size，推断 aspect_ratio
    if size and not aspect_ratio:
        aspect_ratio = _size_to_aspect_ratio(size)
        return size, aspect_ratio


def _aspect_ratio_to_size(aspect_ratio: str) -> str:
    """
    将 aspect_ratio 转换为对应的 size
    
    Args:
        aspect_ratio: 宽高比，如 "16:9", "1:1"
    
    Returns:
        str: 对应的尺寸，如 "1366x768"
    """
    ratio_map = {
        "1:1": "1024x1024",
        "16:9": "1366x768",
        "9:16": "768x1366",
        "4:3": "1024x768",
        "3:4": "768x1024",
        "3:2": "1024x683",
        "2:3": "683x1024",
        "21:9": "1366x585",
        "9:21": "585x1366",
    }
    
    # 标准化输入（处理可能的空格）
    ratio = aspect_ratio.strip().lower()
    
    return ratio_map.get(ratio, "1024x1024")


def _size_to_aspect_ratio(size: str) -> str:
    """
    将 size 转换为对应的 aspect_ratio
    
    Args:
        size: 尺寸，如 "1024x1024"
    
    Returns:
        str: 对应的宽高比，如 "1:1"
    """
    # 解析尺寸
    try:
        parts = size.lower().split("x")
        if len(parts) != 2:
            return "1:1"
        
        width, height = int(parts[0]), int(parts[1])
        
        # 计算比例
        from math import gcd
        divisor = gcd(width, height)
        ratio_w = width // divisor
        ratio_h = height // divisor
        
        return f"{ratio_w}:{ratio_h}"
    
    except (ValueError, IndexError):
        return "1:1"


def format_size_for_provider(size: str, provider: str) -> str:
    """
    根据不同的 Provider 格式化 size 参数
    
    某些 Provider 可能需要特定的 size 格式
    
    Args:
        size: 标准尺寸，如 "1024x1024"
        provider: Provider 名称
    
    Returns:
        str: Provider 特定的 size 格式
    """
    # 目前大部分 Provider 都使用标准格式
    # 如果有特殊需求，在这里添加转换逻辑
    return size


def format_aspect_ratio_for_provider(aspect_ratio: str, provider: str) -> str:
    """
    根据不同的 Provider 格式化 aspect_ratio 参数
    
    Args:
        aspect_ratio: 标准宽高比，如 "16:9"
        provider: Provider 名称
    
    Returns:
        str: Provider 特定的 aspect_ratio 格式
    """
    # GrsAI 使用 aspectRatio（驼峰命名）
    if provider == "grsai":
        return aspect_ratio
    
    # 其他 Provider 使用标准格式
    return aspect_ratio
