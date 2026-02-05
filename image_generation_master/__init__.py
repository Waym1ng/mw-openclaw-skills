"""
图像生成大师 - OpenClaw Skill

统一的图像生成能力，支持多个第三方供应商
"""
from .skill import run, run_sync
from .schema import ImageGenerationRequest, ImageGenerationResult

__version__ = "1.0.0"
__all__ = ["run", "run_sync", "ImageGenerationRequest", "ImageGenerationResult"]
