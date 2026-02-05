"""
配置文件加载工具
支持从 config.yaml 读取 API 密钥
"""
import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """配置管理器"""

    def __init__(self):
        self._config: Optional[Dict[str, Any]] = None
        self._config_path: Optional[Path] = None

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self._config is not None:
            return self._config

        # 查找配置文件
        possible_paths = [
            # 当前目录的 config.yaml
            Path(__file__).parent.parent / "config.yaml",
            # 工作区的 config.yaml
            Path.cwd() / "config.yaml",
            # 技能目录的 config.yaml
            Path(__file__).parent.parent.parent / "skills" / "image_generation_master" / "config.yaml",
        ]

        for path in possible_paths:
            if path.exists():
                self._config_path = path
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        self._config = yaml.safe_load(f)
                    return self._config
                except Exception as e:
                    # 配置文件读取失败，返回空配置
                    self._config = {}
                    return self._config

        # 没找到配置文件
        self._config = {}
        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键，支持点号分隔的路径，如 "blt.api_key"
            default: 默认值

        Returns:
            配置值或默认值
        """
        config = self._load_config()

        # 支持点号分隔的路径
        keys = key.split('.')
        value = config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    def get_blt_api_key(self) -> Optional[str]:
        """获取柏拉图 API Key"""
        # 优先从环境变量读取
        env_key = os.getenv("BLT_API_KEY")
        if env_key:
            return env_key

        # 从配置文件读取
        return self.get("blt.api_key")

    def get_grsai_api_key(self) -> Optional[str]:
        """获取 GrsAI API Key"""
        # 优先从环境变量读取
        env_key = os.getenv("GRSAI_API_KEY")
        if env_key:
            return env_key

        # 从配置文件读取
        return self.get("grsai.api_key")

    def get_blt_base_url(self) -> str:
        """获取柏拉图基础 URL"""
        # 优先从环境变量读取
        env_url = os.getenv("BLT_BASE_URL")
        if env_url:
            return env_url

        # 从配置文件读取
        return self.get("blt.base_url", "https://api.bltcy.ai")

    def get_grsai_base_url(self) -> str:
        """获取 GrsAI 基础 URL"""
        # 优先从环境变量读取
        env_url = os.getenv("GRSAI_BASE_URL")
        if env_url:
            return env_url

        # 从配置文件读取
        return self.get("grsai.base_url", "https://api.grsai.com")

    def get_default_provider(self) -> str:
        """获取默认供应商"""
        return self.get("defaults.provider", "auto")

    def get_default_model(self) -> str:
        """获取默认模型"""
        return self.get("defaults.model", "nano-banana")

    def get_default_size(self) -> str:
        """获取默认尺寸"""
        return self.get("defaults.size", "1024x1024")

    def get_default_n(self) -> int:
        """获取默认生成数量"""
        return self.get("defaults.n", 1)

    def get_timeout(self) -> int:
        """获取超时时间"""
        return self.get("defaults.timeout", 600)


# 全局配置实例
_config = Config()


def get_config() -> Config:
    """获取配置实例"""
    return _config
