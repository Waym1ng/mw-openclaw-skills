"""
模型适配器包初始化
"""
from .blt_adapters import (
    build_request as blt_build_request,
    get_supported_models as blt_get_supported_models
)
from .grsai_mapper import (
    get_endpoint_for_model,
    get_supported_models as grsai_get_supported_models
)

__all__ = [
    "blt_build_request",
    "blt_get_supported_models",
    "get_endpoint_for_model",
    "grsai_get_supported_models"
]
