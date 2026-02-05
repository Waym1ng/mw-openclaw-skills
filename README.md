# MW OpenClaw Skills

一个模块化的 OpenClaw Skill 集合，提供各种可复用的 AI 能力组件。

## 项目简介

MW OpenClaw Skills 是一个可扩展的技能集合项目，每个技能（Skill）都是一个独立的功能模块，可以通过统一的接口集成到 OpenClaw 平台中。项目采用模块化设计，方便添加新技能和复用现有功能。

## SKILLS 列表

### 🎨 图像生成大师 (image_generation_master)

统一的图像生成能力，支持多个第三方供应商（柏拉图、GrsAI）。

**核心特性：**
- ✅ 多供应商支持 - 柏拉图和 GrsAI 两个平台
- ✅ 智能路由 - 根据模型名称自动选择供应商
- ✅ 参数自动兼容 - size 和 aspect_ratio 自动转换
- ✅ 统一接口 - 一致的输入输出格式
- ✅ 配置灵活 - 支持环境变量和配置文件
- ✅ 可扩展架构 - 轻松添加新的供应商
- ✅ 零外部依赖 - 只使用 Python 标准库

**支持的模型包括：**
- nano-banana 系列（高清、极速、专业版）
- flux 系列（flux、flux-dev、flux-pro 等）
- sora-image、gpt-image 系列等

[查看详细文档 →](./image_generation_master/README.md)

---

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue。
