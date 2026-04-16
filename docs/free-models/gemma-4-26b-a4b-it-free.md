# Google Gemma 4 26B A4B - 免费模型 - 2026-04-03

## 先给结论

**MoE 架构高效模型，支持图文视频，当前免费。**

如果你只有 20 秒，可以直接看这张表：

| 问题 | 快速判断 |
| --- | --- |
| 现在免费吗 | 是，OpenRouter 当前显示输入/输出都是 `0` |
| 能直接用吗 | 能，直接用 `google/gemma-4-26b-a4b-it:free` |
| 值不值得试 | 值得，MoE 架构高效，支持多模态 |
| 适不适合高敏任务 | Apache 2.0 开源，相对可控 |
| 要不要长期保留 | 值得进候选池，性价比不错 |

---

## 关键信息

| 项目 | 当前信息 |
| --- | --- |
| 模型名 | Google Gemma 4 26B A4B Instruct |
| OpenRouter slug | `google/gemma-4-26b-a4b-it:free` |
| OpenRouter 页面 | https://openrouter.ai/google/gemma-4-26b-a4b-it:free |
| 当前是否免费 | 是 |
| 架构 | MoE（25.2B 参数，3.8B 激活/ token） |
| 模态 | text + image + video → text |
| 上下文窗口 | 262K |
| 支持功能 | reasoning、function calling、tools |
| 许可证 | Apache 2.0 |
| 上架 OpenRouter 时间 | 2026-04-03 |

---

## 为什么说它"可直接用"

- 有明确 slug：`google/gemma-4-26b-a4b-it:free`
- 当前可直接通过 OpenRouter 调用
- **MoE 架构高效**：25.2B 参数仅激活 3.8B，接近 31B 质量
- 支持图文视频多模态输入
- Apache 2.0 完全开源

---

## 适合马上试的场景

- 需要高效推理的任务
- 图文视频混合处理
- 长文档分析（262K 上下文）
- 边缘部署（激活参数小，适合资源受限环境）

---

## 与 Gemma 4 31B 的区别

| 对比项 | Gemma 4 26B A4B | Gemma 4 31B |
|-------|-----------------|-------------|
| 架构 | MoE (3.8B 激活) | Dense (30.7B) |
| 总参数 | 25.2B | 30.7B |
| 效率 | 更高 | 标准 |
| 质量 | 接近 31B | 基准 |

---

## 最终判断

> **Gemma 4 26B A4B 是 Gemma 4 系列中效率最高的选择。**

### 我的建议

- **现在就试**：如果你需要高效的多模态模型
- **边缘部署首选**：激活参数少，适合资源受限场景
- **与 31B 互补**：根据任务选择效率或绝对性能

## 信息来源说明

本文基于 OpenRouter API 直接获取的模型信息整理。

- 来源: https://openrouter.ai/google/gemma-4-26b-a4b-it:free
