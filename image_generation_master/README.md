# 图像生成大师 - OpenClaw Skill

统一的图像生成能力，支持多个第三方供应商（柏拉图、GrsAI）。

## 特性

✅ **多供应商支持** - 柏拉图和 GrsAI 两个平台  
✅ **智能路由** - 根据模型名称自动选择供应商  
✅ **参数自动兼容** - size 和 aspect_ratio 自动转换  
✅ **统一接口** - 一致的输入输出格式  
✅ **配置灵活** - 支持环境变量和配置文件  
✅ **可扩展架构** - 轻松添加新的供应商  
✅ **零外部依赖** - 只使用 Python 标准库

## 注册供应商
[柏拉图平台](https://api.bltcy.ai/register?aff=0e8deb35793)
[GrsAI平台](https://grsai.ai/)

## 安装

无需安装额外依赖！本技能只使用 Python 标准库。

## 配置

API 密钥支持两种方式（**环境变量优先级更高**）：

### 方式 1: 环境变量（优先）

```bash
# 柏拉图平台
export BLT_API_KEY="your-blt-api-key"

# GrsAI 平台
export GRSAI_API_KEY="your-grsai-api-key"
```

### 方式 2: 配置文件

复制 `config.example.yaml` 为 `config.yaml` 并填入 API 密钥：

```bash
cp config.example.yaml config.yaml
```

然后编辑 `config.yaml`：

```yaml
blt:
  api_key: "your-blt-api-key"
  base_url: "https://api.bltcy.ai"

grsai:
  api_key: "your-grsai-api-key"
  base_url: "https://api.grsai.com"

defaults:
  provider: "auto"
  model: "nano-banana"
  size: "1024x1024"
  n: 1
  timeout: 600
```

**配置优先级**：环境变量 > 配置文件 > 默认值

## 使用方法

### 基本用法

```python
import asyncio
from image_generation_master import run

async def generate_image():
    result = await run({
        "prompt": "一只可爱的橘猫坐在窗台上"
    })
    
    if result["success"]:
        print("生成的图片:", result["images"])
    else:
        print("错误:", result["message"])

asyncio.run(generate_image())
```

### 指定供应商和模型

```python
result = await run({
    "prompt": "未来科技城市，赛博朋克风格",
    "provider": "blt",
    "model": "nano-banana",
    "aspect_ratio": "16:9"
})
```

### 自动选择供应商

```python
result = await run({
    "prompt": "抽象艺术画作",
    "model": "flux-pro"  # 自动路由到柏拉图平台
})
```

## 参数说明

### 输入参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| prompt | string | ✅ | 图片生成提示词 |
| model | string | ❌ | 模型名称（如 `nano-banana`） |
| provider | string | ❌ | 供应商（`blt`/`grsai`/`auto`） |
| size | string | ❌ | 图片尺寸（如 `1024x1024`） |
| aspect_ratio | string | ❌ | 宽高比（如 `16:9`） |
| n | integer | ❌ | 生成数量（默认 1） |
| image_urls | array | ❌ | 参考图片 URL 列表 |

### 输出结果

```python
{
    "success": True,              # 是否成功
    "images": ["url1", "url2"],   # 图片 URL 列表
    "provider": "blt",            # 实际使用的供应商
    "model": "nano-banana",       # 实际使用的模型
    "message": None               # 错误信息（如果失败）
}
```

## 支持的模型

### 柏拉图平台

- `nano-banana`, `nano-banana-hd`, `nano-banana-2`
- `doubao-seedream-4-0-250828`, `doubao-seedream-4-5-251128`
- `gpt-4o-image`, `gpt-4o-image-vip`, `gpt-image-1`
- `sora_image`, `sora_image-vip`
- `flux`, `flux-dev`, `flux-pro`, `flux-pro-max`
- `flux-kontext-pro`, `flux-kontext-max`

### GrsAI 平台

- `nano-banana`, `nano-banana-fast`
- `nano-banana-pro`, `nano-banana-pro-vt`
- `nano-banana-pro-cl`, `nano-banana-pro-vip`
- `nano-banana-pro-4k-vip`
- `sora-image`, `gpt-image-1.5`

## 测试

运行测试脚本：

```bash
# 配置测试（不调用 API）
python3 test_config.py

# 实际生成测试（会调用 API）
python3 test_real_generation.py
```

## 目录结构

```
image_generation_master/
├── SKILL.md              # Skill 能力定义（AI 助手使用）
├── README.md             # 本文件
├── skill.yaml            # Skill 元数据
├── skill.py              # 主入口
├── config.yaml           # 配置文件（需创建）
├── config.example.yaml   # 配置示例
├── schema.py             # 统一 Schema
├── providers/
│   ├── base.py          # Provider 抽象基类
│   ├── blt_provider.py  # 柏拉图平台
│   ├── grsai_provider.py# GrsAI 平台
│   ├── registry.py      # Provider 注册工厂
│   └── __init__.py
├── models/
│   ├── blt_adapters.py  # 柏拉图模型适配器
│   ├── grsai_mapper.py  # GrsAI 模型映射
│   └── __init__.py
└── utils/
    ├── config_loader.py # 配置文件加载器
    ├── param_mapper.py  # 参数映射工具
    └── __init__.py
```

## 设计架构

```
用户请求
    ↓
Skill 主入口 (skill.py)
    ↓
统一 Schema (schema.py)
    ↓
配置加载器 (config_loader.py)
    ↓
Provider 注册工厂 (registry.py)
    ↓
┌─────────────┬──────────────┐
│  BltProvider│ GrsaiProvider│
│             │              │
│ 模型适配器  │  端点映射    │
│ (adapters)  │  (mapper)    │
└─────────────┴──────────────┘
    ↓
统一结果返回
```

## 扩展指南

### 添加新的供应商

1. 在 `providers/` 下创建新的 Provider 文件
2. 继承 `BaseProvider` 类
3. 实现 `generate()` 方法
4. 在 `providers/__init__.py` 中注册

示例：

```python
from .base import BaseProvider
from ..schema import ImageGenerationRequest, ImageGenerationResult

class NewProvider(BaseProvider):
    name = "new-provider"
    
    async def generate(self, request: ImageGenerationRequest) -> ImageGenerationResult:
        # 实现你的逻辑
        pass
```

## 技术栈

- **Python 3.8+** - 异步编程支持
- **urllib** - HTTP 请求（标准库）
- **yaml** - 配置文件解析
- **typing** - 类型注解

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
