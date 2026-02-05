"""
Providers 包初始化
自动注册所有可用的 Provider
"""
from .base import BaseProvider
from .blt_provider import BltProvider
from .grsai_provider import GrsaiProvider
from .registry import (
    register_provider,
    get_provider,
    list_providers
)

# 自动注册所有 Provider
register_provider("blt", BltProvider)
register_provider("grsai", GrsaiProvider)

__all__ = [
    "BaseProvider",
    "BltProvider",
    "GrsaiProvider",
    "register_provider",
    "get_provider",
    "list_providers",
]
