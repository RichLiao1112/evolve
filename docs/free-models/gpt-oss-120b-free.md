# OpenAI GPT-OSS 120B - 免费模型 - 2026-03

## 先给结论

**OpenAI 首个开源权重模型，免费且 Apache 2.0 许可。**

如果你只有 20 秒，可以直接看这张表：

| 问题 | 快速判断 |
| --- | --- |
| 现在免费吗 | 是，OpenRouter 当前显示输入/输出都是 `0` |
| 能直接用吗 | 能，直接用 `openai/gpt-oss-120b:free` |
| 值不值得试 | **值得**，OpenAI 官方开源模型 |
| 适不适合高敏任务 | Apache 2.0，可本地部署 |
| 要不要长期保留 | 开源权重，建议进主力池 |

---

## 关键信息

| 项目 | 当前信息 |
| --- | --- |
| 模型名 | OpenAI GPT-OSS 120B |
| OpenRouter slug | `openai/gpt-oss-120b:free` |
| OpenRouter 页面 | https://openrouter.ai/openai/gpt-oss-120b:free |
| 当前是否免费 | 是 |
| 架构 | MoE（117B 参数） |
| 模态 | text → text |
| 上下文窗口 | 131K |
| 许可证 | Apache 2.0（完全开源） |
| 支持功能 | reasoning、function calling、tools、structured output |
| 上架 OpenRouter 时间 | 2026-03 |

---

## 为什么说它"可直接用"

- 有明确 slug：`openai/gpt-oss-120b:free`
- 当前可直接通过 OpenRouter 调用
- **OpenAI 首个开源权重模型**
- **Apache 2.0 许可证**，完全开源可商用
- 支持可配置推理深度和完整思维链
- 原生支持工具调用和结构化输出

---

## 适合马上试的场景

- 需要开源权重的生产环境
- 数据隐私要求高的场景（可本地部署）
- 需要 reasoning 能力的任务
- Agent 和工具调用场景
- 想要对比 OpenAI 风格的任务

---

## 不要直接无脑上的地方

### 1. 120B 规模需要算力

本地部署需要较强 GPU 资源。

### 2. 性能定位

开源版与 GPT-4o 等闭源模型仍有差距，需根据任务评估。

---

## 最终判断

> **GPT-OSS 120B 的意义：OpenAI 正式进入开源大模型领域。**

### 我的建议

- **现在就试**：如果你想体验 OpenAI 的开源模型
- **开源首选**：Apache 2.0 许可证，无商业限制
- **可本地部署**：适合数据敏感场景

## 信息来源说明

本文基于 OpenRouter 当前公开可见的模型接口与页面信息整理，结论适用于**当前时点的快速使用判断**。

- 来源: https://openrouter.ai/openai/gpt-oss-120b:free
