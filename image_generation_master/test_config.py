#!/usr/bin/env python3
"""
测试配置加载
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from image_generation_master.utils.config_loader import get_config


def test_config_loader():
    """测试配置加载器"""
    print("🧪 测试配置加载器")

    config = get_config()

    print(f"✅ 配置文件路径: {config._config_path}")
    print(f"✅ 柏拉图 API Key: {config.get_blt_api_key()[:20]}..." if config.get_blt_api_key() else "❌ 未找到柏拉图 API Key")
    print(f"✅ GrsAI API Key: {config.get_grsai_api_key()[:20]}..." if config.get_grsai_api_key() else "❌ 未找到 GrsAI API Key")
    print(f"✅ 默认供应商: {config.get_default_provider()}")
    print(f"✅ 默认模型: {config.get_default_model()}")
    print(f"✅ 默认尺寸: {config.get_default_size()}")
    print(f"✅ 超时时间: {config.get_timeout()}秒")


if __name__ == "__main__":
    test_config_loader()
