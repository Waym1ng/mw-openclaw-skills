"""
柏拉图平台模型适配器
复用参考代码的适配器注册模式
"""
from typing import Dict, Any
from abc import ABC, abstractmethod


# === 适配器注册表 ===
ADAPTER_REGISTRY = {}


def register_adapter(*names: str):
    """
    装饰器：支持多个真实模型名映射到同一个适配器
    
    使用示例：
        @register_adapter("nano-banana", "nano-banana-hd")
        class NanoBananaAdapter(BaseAdapter):
            pass
    """
    def wrapper(cls):
        if not issubclass(cls, BaseAdapter):
            raise TypeError(f"{cls.__name__} 必须继承 BaseAdapter")
        for name in names:
            ADAPTER_REGISTRY[name] = cls()
        return cls
    return wrapper


# === 抽象基类 ===
class BaseAdapter(ABC):
    """适配器基类"""
    
    @abstractmethod
    def build_payload(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建请求载荷
        
        Args:
            request: 包含 model, prompt 等参数的字典
            
        Returns:
            dict: 适配后的请求参数
        """
        pass


# === 适配器实现 ===

@register_adapter("nano-banana", "nano-banana-hd", "nano-banana-2")
class NanoBananaAdapter(BaseAdapter):
    """Nano Banana 系列模型适配器"""
    
    def build_payload(self, request: Dict[str, Any]) -> Dict[str, Any]:
        payload_data = {
            "model": request["model"],
            "prompt": request["prompt"],
            "response_format": request.get("response_format", "url"),
            "image": request.get("image", []),
        }
        
        # 添加 aspect_ratio 参数
        if request.get("aspect_ratio") and request.get("aspect_ratio") != "auto":
            payload_data["aspect_ratio"] = request.get("aspect_ratio")
        
        return payload_data


@register_adapter("doubao-seedream-4-0-250828", "doubao-seedream-4-5-251128")
class Jimeng4Adapter(BaseAdapter):
    """豆包系列模型适配器"""
    
    def build_payload(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # 将 aspect_ratio 融入 prompt
        if request.get("aspect_ratio") and request.get("aspect_ratio") != "auto":
            payload_prompt = f"{request['prompt']} 比例: {request.get('aspect_ratio')}"
        else:
            payload_prompt = request["prompt"]
        
        payload_data = {
            "model": request["model"],
            "prompt": payload_prompt,
            "image": request.get("image", []),
            "sequential_image_generation": request.get("sequential_image_generation", "auto"),
            "response_format": request.get("response_format", "url"),
            "size": "2K",
            "stream": request.get("stream", False),
            "watermark": request.get("watermark", False),
            "n": request.get("n", 1),
        }
        return payload_data


@register_adapter("gpt-4o-image", "gpt-4o-image-vip", "sora_image", "sora_image-vip", "gpt-image-1")
class OpenAIImageAdapter(BaseAdapter):
    """OpenAI 图像模型适配器"""
    
    def build_payload(self, request: Dict[str, Any]) -> Dict[str, Any]:
        payload_data = {
            "size": request.get("size", "1024x1024"),
            "prompt": request["prompt"],
            "sync_mode": request.get("sync_mode", False),
            "model": request["model"],
            "n": request.get("n", 1),
            "image": request.get("image", []),
        }
        return payload_data


@register_adapter("flux-kontext-pro", "flux-kontext-max")
class FluxKontextAdapter(BaseAdapter):
    """Flux Kontext 系列模型适配器"""
    
    def build_payload(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Flux 接口以 size 控制比例；如仅给了 aspect_ratio，则做映射
        size = request.get("size")
        if not size:
            aspect_ratio = request.get("aspect_ratio")
            if isinstance(aspect_ratio, str):
                ratio_to_size = {
                    "1:1": "1024x1024",
                    "16:9": "1366x768",
                    "9:16": "768x1366",
                    "4:3": "1024x768",
                    "3:4": "768x1024",
                }
                size = ratio_to_size.get(aspect_ratio, "1024x1024")
        
        return {
            "model": request["model"],
            "prompt": request["prompt"],
            "size": size or "1024x1024",
            "response_format": request.get("response_format", "url"),
            "n": request.get("n", 1),
            "image": request.get("image", []),
        }


@register_adapter("flux", "flux-dev", "flux-pro", "flux-pro-max")
class FluxAdapter(BaseAdapter):
    """Flux 系列模型适配器"""
    
    def build_payload(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # 与 FluxKontext 一致：优先使用 size；若仅传入 aspect_ratio 则做映射
        size = request.get("size")
        if not size:
            aspect_ratio = request.get("aspect_ratio")
            if isinstance(aspect_ratio, str):
                ratio_to_size = {
                    "1:1": "1024x1024",
                    "16:9": "1366x768",
                    "9:16": "768x1366",
                    "4:3": "1024x768",
                    "3:4": "768x1024",
                }
                size = ratio_to_size.get(aspect_ratio, "1024x1024")
        
        return {
            "model": request["model"],
            "prompt": request["prompt"],
            "size": size or "1024x1024"
        }


# === 工厂方法 ===
def build_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    根据真实模型名选择对应的适配器
    
    Args:
        request: 包含 model 字段的请求字典
        
    Returns:
        dict: 适配后的请求参数
        
    Raises:
        ValueError: 如果未找到模型适配器
    """
    model = request.get("model")
    if not model:
        raise ValueError("请求中必须包含 model 字段")
    
    adapter = ADAPTER_REGISTRY.get(model)
    if not adapter:
        available = ", ".join(ADAPTER_REGISTRY.keys())
        raise ValueError(
            f"未找到模型适配器: {model}。"
            f"支持的模型: {available}"
        )
    
    return adapter.build_payload(request)


def get_supported_models() -> list:
    """返回所有支持的模型名称"""
    return list(ADAPTER_REGISTRY.keys())
