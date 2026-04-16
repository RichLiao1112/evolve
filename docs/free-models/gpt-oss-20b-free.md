# OpenAI GPT-OSS 20B - 免费模型 - 2026-03

## 先给结论

**OpenAI 开源小模型，Apache 2.0，当前免费。**

如果你只有 20 秒，可以直接看这张表：

| 问题 | 快速判断 |
| --- | --- |
| 现在免费吗 | 是，OpenRouter 当前显示输入/输出都是 `0` |
| 能直接用吗 | 能，直接用 `openai/gpt-oss-20b:free` |
| 值不值得试 | 值得，OpenAI 官方开源，可本地部署 |
| 适不适合高敏任务 | Apache 2.0，可本地部署 |
| 要不要长期保留 | 小模型边缘部署首选 |

---

## 关键信息

| 项目 | 当前信息 |
| --- | --- |
| 模型名 | OpenAI GPT-OSS 20B |
| OpenRouter slug | `openai/gpt-oss-20b:free` |
| OpenRouter 页面 | https://openrouter.ai/openai/gpt-oss-20b:free |
| 当前是否免费 | 是 |
| 架构 | MoE（21B 参数，3.6B 激活） |
| 模态 | text → text |
| 上下文窗口 | 131K |
| 许可证 | Apache 2.0 |
| 支持功能 | reasoning、function calling、tools |
| 上架 OpenRouter 时间 | 2026-03 |

---

## 为什么说它"可直接用"

- 有明确 slug：`openai/gpt-oss-20b:free`
- 当前可直接通过 OpenRouter 调用
- **OpenAI 官方开源模型**
- **Apache 2.0 许可证**
- MoE 架构高效（21B 参数仅激活 3.6B）
- 适合边缘部署

---

## 与 GPT-OSS 120B 的区别

| 对比项 | GPT-OSS 20B | GPT-OSS 120B |
|-------|-------------|--------------|
| 总参数 | 21B | 117B |
| 激活参数 | 3.6B | 5.1B |
| 上下文 | 131K | 131K |
| 定位 | 边缘/高效 | 高性能 |
| 本地部署 | 更容易 | 需要更强算力 |

---

## 适合马上试的场景

- 边缘设备部署
- 资源受限环境
- 需要 OpenAI 风格输出的任务
- 数据隐私要求高的场景（可本地部署）

---

## 最终判断

> **GPT-OSS 20B 是 OpenAI 开源模型中部署门槛最低的选择。**

### 我的建议

- **现在就试**：如果你需要可本地部署的 OpenAI 模型
- **边缘首选**：比 120B 更容易部署
- **与 120B 互补**：根据算力选择

## 信息来源说明

本文基于 OpenRouter API 直接获取的模型信息整理。

- 来源: https://openrouter.ai/openai/gpt-oss-20b:free
