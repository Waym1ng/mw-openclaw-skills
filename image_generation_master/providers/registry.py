"""
Provider 注册工厂
负责 Provider 的注册、获取和自动路由
"""
from typing import Optional
from .base import BaseProvider


class ProviderRegistry:
    """
    Provider 注册表
    管理所有可用的图像生成供应商
    """
    
    def __init__(self):
        self._providers = {}
    
    def register(self, name: str, provider_class: type):
        """
        注册一个 Provider
        
        Args:
            name: Provider 名称（如 'blt', 'grsai'）
            provider_class: Provider 类（必须继承 BaseProvider）
        """
        if not issubclass(provider_class, BaseProvider):
            raise TypeError(f"{provider_class.__name__} 必须继承 BaseProvider")
        self._providers[name.lower()] = provider_class
    
    def get(self, name: Optional[str] = None, model: Optional[str] = None) -> BaseProvider:
        """
        获取 Provider 实例
        
        Args:
            name: Provider 名称（如 'blt', 'grsai'），None 或 'auto' 表示自动选择
            model: 模型名称，用于自动推断 Provider
            
        Returns:
            BaseProvider: Provider 实例
        """
        # 自动选择模式
        if not name or name.lower() == "auto":
            return self._auto_select(model)
        
        # 按名称获取
        provider_class = self._providers.get(name.lower())
        if not provider_class:
            available = ", ".join(self._providers.keys())
            raise ValueError(
                f"未找到 Provider: '{name}'。"
                f"可用的 Provider: {available}"
            )
        
        return provider_class()
    
    def _auto_select(self, model: Optional[str]) -> BaseProvider:
        """
        根据模型名称自动选择 Provider
        
        优先级规则：
        1. 如果有 model，根据模型前缀推断
        2. 默认使用第一个注册的 Provider
        
        Args:
            model: 模型名称
        """
        if model:
            # 柏拉图平台模型特征
            blt_models = ["nano", "doubao", "flux", "gpt-4o-image", "sora_image"]
            if any(model.startswith(prefix) for prefix in blt_models):
                if "blt" in self._providers:
                    return self._providers["blt"]()
            
            # GrsAI 平台模型特征
            grsai_models = ["sora-image", "gpt-image", "nano-banana-fast", "nano-banana-pro"]
            if any(model.startswith(prefix) for prefix in grsai_models):
                if "grsai" in self._providers:
                    return self._providers["grsai"]()
        
        # 默认返回第一个注册的 Provider
        if self._providers:
            first_provider = next(iter(self._providers.values()))
            return first_provider()
        
        raise ValueError("没有可用的 Provider")
    
    def list_providers(self) -> list:
        """返回所有已注册的 Provider 名称"""
        return list(self._providers.keys())


# 全局注册表实例
_registry = ProviderRegistry()


def register_provider(name: str, provider_class: type):
    """
    注册 Provider 的便捷函数
    
    使用示例：
        from providers.blt_provider import BltProvider
        register_provider("blt", BltProvider)
    """
    _registry.register(name, provider_class)


def get_provider(name: Optional[str] = None, model: Optional[str] = None) -> BaseProvider:
    """
    获取 Provider 实例的便捷函数
    
    使用示例：
        # 自动选择
        provider = get_provider()
        
        # 指定 Provider
        provider = get_provider("blt")
        
        # 根据模型自动选择
        provider = get_provider(model="nano-banana")
    """
    return _registry.get(name, model)


def list_providers() -> list:
    """返回所有已注册的 Provider 名称"""
    return _registry.list_providers()
