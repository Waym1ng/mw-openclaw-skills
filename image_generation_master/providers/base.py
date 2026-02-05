"""
Provider 抽象基类
定义所有图像生成供应商必须实现的接口
"""
from abc import ABC, abstractmethod
from ..schema import ImageGenerationRequest, ImageGenerationResult


class BaseProvider(ABC):
    """
    图像生成供应商抽象基类
    所有具体的 Provider 实现（BltProvider、GrsaiProvider）都必须继承此类
    """
    
    # Provider 名称标识
    name: str = "base"
    
    # Provider 支持的模型列表（用于验证）
    supported_models: list = []
    
    @abstractmethod
    async def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        """
        生成图片的核心方法
        
        Args:
            request: 统一的图像生成请求
            
        Returns:
            ImageGenerationResult: 统一的生成结果
        """
        pass
    
    def supports_model(self, model: str) -> bool:
        """检查 Provider 是否支持指定模型"""
        if not self.supported_models:
            return True  # 空列表表示支持所有模型
        return model in self.supported_models
    
    def normalize_request(self, request: ImageGenerationRequest) -> dict:
        """
        将统一请求转换为 Provider 特定格式
        子类可以重写此方法以实现自定义的参数转换
        
        Args:
            request: 统一的图像生成请求
            
        Returns:
            dict: Provider 特定的请求参数
        """
        return {
            "prompt": request.prompt,
            "model": request.model,
            "size": request.size,
            "n": request.n,
        }
