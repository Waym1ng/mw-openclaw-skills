---
name: image_generation_master
description: |
  图像生成能力 - 通过自然语言对话生成AI图片，集成柏拉图和GrsAI双供应商。

  **何时使用**: 当用户要求"生成图片"、"画一个xxx"、"帮我做个图"、"用AI生成xxx"、"创建图片"、"xxx风格的图片"等时使用。

  **支持功能**: 文生图、图生图（参考图片）、指定尺寸/宽高比、选择模型/供应商、生成多张图片。

  **推荐调用方式**: Shell 脚本（推荐）或 Python 代码
  
  Shell 调用示例:
  - 基本用法: `./image_generation_master/generate.sh "提示词"`
  - 指定参数: `./image_generation_master/generate.sh "提示词" --model nano-banana --size 1024x1024`
  - 宽屏图片: `./image_generation_master/generate.sh "提示词" --aspect-ratio 16:9`
  - 生成多张: `./image_generation_master/generate.sh "提示词" --n 2`
  - 查看帮助: `./image_generation_master/generate.sh --help`

  **常见触发**: "画一个美女"、"生成风景照"、"创建logo"、"改成动漫风格"（附图）、"用banana模型生成"。
---

# Image Generation Master

统一的图像生成能力，支持多供应商。

## 快速开始

用户说这些话时，立即使用此技能：
- "生成一张..." / "画一个..." / "帮我做个图..."
- "用AI生成..." / "创建图片..."
- 附上图片说"改成xxx风格"（图生图）

## 使用方式

### 方式 1: Python 代码调用

最简用法 - 只描述想要的图片：

```python
from image_generation_master import run

result = await run({
    "prompt": "一只可爱的橘猫坐在窗台上"
})
```

### 方式 2: Shell 脚本调用

对于非 Python 环境或快速测试，可以使用提供的 shell 脚本：

```bash
# 赋予执行权限（首次使用）
chmod +x image_generation_master/generate.sh

# 最简单用法
./image_generation_master/generate.sh "一只可爱的橘猫坐在窗台上"

# 查看帮助
./image_generation_master/generate.sh --help
```

## 常见参数组合

### 指定尺寸

```python
result = await run({
    "prompt": "未来科技城市，赛博朋克风格",
    "size": "1024x1024"  # 1:1 方形
})
```

### 竖屏/宽屏

```python
result = await run({
    "prompt": "性感的少女",
    "aspect_ratio": "9:16"  # 竖屏，自动转为 768x1366
})

result = await run({
    "prompt": "壮丽的山川河流",
    "aspect_ratio": "16:9"  # 宽屏，自动转为 1366x768
})
```

### 指定模型

```python
result = await run({
    "prompt": "抽象艺术画作",
    "model": "flux-pro"  # 高质量模型
})
```

### 生成多张

```python
result = await run({
    "prompt": "美丽的风景",
    "n": 2  # 生成2张
})
```

## 常用模型

### 柏拉图 (provider: blt)

- **nano-banana** - 通用，质量好，速度快
- **flux-pro** - Flux专业版，高质量
- **doubao-seedream-4-0-250828** - 豆包
- **gpt-4o-image** - GPT-4o图像
- **sora_image** - Sora图像

### GrsAI (provider: grsai)

- **nano-banana** - 基础
- **nano-banana-pro** - 专业版，质量更好
- **sora-image** - Sora
- **gpt-image-1.5** - GPT图像

## 输出格式

```python
{
    "success": True,              # 是否成功
    "images": ["url1", "url2"],   # 图片URL列表
    "provider": "blt",            # 实际用的供应商
    "model": "nano-banana",       # 实际用的模型
    "message": None               # 错误信息（如果失败）
}
```

## 图生图

用户附上图片并要求改变风格时：

```python
result = await run({
    "prompt": "将这张图片改成动漫风格",
    "image_urls": ["https://example.com/ref.jpg"],
    "model": "nano-banana"
})
```

## Shell 脚本详细用法

Shell 脚本支持所有参数，适合快速测试和命令行使用：

### 最简单用法
```bash
./image_generation_master/generate.sh "一只可爱的橘猫坐在窗台上"
```

### 指定模型和尺寸
```bash
./image_generation_master/generate.sh "赛博朋克风格城市" --model flux-pro --size 1024x1024
```

### 竖屏/宽屏
```bash
# 竖屏
./image_generation_master/generate.sh "性感的少女" --aspect-ratio 9:16

# 宽屏
./image_generation_master/generate.sh "壮丽的山川河流" --aspect-ratio 16:9
```

### 生成多张
```bash
./image_generation_master/generate.sh "美丽的风景" --n 2
```

### 图生图
```bash
./image_generation_master/generate.sh "改成动漫风格" --image-url "https://example.com/ref.jpg"
```

### 完整参数示例
```bash
./image_generation_master/generate.sh "高质量肖像画" \
  --model nano-banana \
  --provider blt \
  --size 1024x1024 \
  --n 1
```

### 输出格式
脚本以 JSON 格式输出结果：
```json
{
  "success": true,
  "images": ["https://example.com/generated.jpg"],
  "provider": "blt",
  "model": "nano-banana",
  "message": null
}
```

### 查看帮助
```bash
./image_generation_master/generate.sh --help
```

## 智能路由

- 不指定provider → 根据model自动选
- 不指定model → 用供应商默认模型
- size和aspect_ratio自动互转

## 对话示例

**用户**: "帮我生成一张猫的图片"
**助手**: 默认设置生成

**用户**: "用flux-pro模型生成赛博朋克风格，要宽屏"
**助手**: model="flux-pro", aspect_ratio="16:9"

**用户**: "要竖屏的，性感的，中国少女"
**助手**: aspect_ratio="9:16", prompt包含"性感的中国少女"

**用户**: [附图] "把这张照片改成油画风格"
**助手**: image_urls=["..."], 图生图

**用户**: "生成两张不同风格的风景画"
**助手**: n=2

## 配置

API 密钥支持两种方式（优先级从高到低）：

### 方式 1: 环境变量（优先）

```bash
export BLT_API_KEY="your-blt-key"
export GRSAI_API_KEY="your-grsai-key"
```

### 方式 2: 配置文件

在 `config.yaml` 中配置：

```yaml
blt:
  api_key: "your-blt-key"
  base_url: "https://api.bltcy.ai"

grsai:
  api_key: "your-grsai-key"
  base_url: "https://api.grsai.com"

defaults:
  provider: "auto"
  model: "nano-banana"
  size: "1024x1024"
  n: 1
  timeout: 600
```

**注意**: 环境变量优先级高于配置文件。
