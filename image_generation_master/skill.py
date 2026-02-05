"""
图像生成大师 Skill 主入口
统一编排层，负责 Provider 路由和结果返回
"""
from .schema import ImageGenerationRequest
from .providers import get_provider


async def run(inputs: dict) -> dict:
    """
    Skill 主入口函数
    
    Args:
        inputs: 输入参数，包含：
            - prompt: 必需，图片生成描述
            - model: 可选，模型名称
            - provider: 可选，供应商名称（blt/grsai）
            - size: 可选，图片尺寸（如 "1024x1024"）
            - aspect_ratio: 可选，宽高比（如 "16:9"）
            - n: 可选，生成数量（默认 1）
            - image_urls: 可选，参考图片列表
    
    Returns:
        dict: 包含以下字段：
            - success: 是否成功
            - images: 生成的图片 URL 列表
            - provider: 实际使用的供应商
            - model: 实际使用的模型
            - message: 错误信息（如果失败）
    """
    try:
        # 创建统一请求对象
        request = ImageGenerationRequest(**inputs)
        
        # 获取 Provider（自动选择或指定）
        provider = get_provider(request.provider, request.model)
        
        # 调用 Provider 生成图片
        result = await provider.generate(request)
        
        # 返回字典格式结果
        return {
            "success": result.success,
            "images": result.images,
            "provider": result.provider,
            "model": result.model,
            "message": result.message
        }
        
    except Exception as e:
        # 统一错误处理
        return {
            "success": False,
            "images": [],
            "provider": inputs.get("provider"),
            "model": inputs.get("model"),
            "message": f"Skill 执行错误: {str(e)}"
        }


# 同步版本（如果需要）
def run_sync(inputs: dict) -> dict:
    """
    同步版本的 Skill 入口
    使用 asyncio.run 在同步上下文中运行异步函数
    """
    import asyncio
    return asyncio.run(run(inputs))
