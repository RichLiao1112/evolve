# NVIDIA Nemotron 3 Nano 30B A3B - 免费模型 - 2026-02

## 先给结论

**256K 超长上下文，高效 MoE，当前免费。**

如果你只有 20 秒，可以直接看这张表：

| 问题 | 快速判断 |
| --- | --- |
| 现在免费吗 | 是，OpenRouter 当前显示输入/输出都是 `0` |
| 能直接用吗 | 能，直接用 `nvidia/nemotron-3-nano-30b-a3b:free` |
| 值不值得试 | 值得，256K 上下文在免费模型中罕见 |
| 适不适合高敏任务 | NVIDIA 官方，相对可信 |
| 要不要长期保留 | 长上下文任务首选 |

---

## 关键信息

| 项目 | 当前信息 |
| --- | --- |
| 模型名 | NVIDIA Nemotron 3 Nano 30B A3B |
| OpenRouter slug | `nvidia/nemotron-3-nano-30b-a3b:free` |
| OpenRouter 页面 | https://openrouter.ai/nvidia/nemotron-3-nano-30b-a3b:free |
| 当前是否免费 | 是 |
| 架构 | MoE（30B 参数，3B 激活） |
| 模态 | text → text |
| 上下文窗口 | **256K** |
| 支持功能 | reasoning、function calling、tools |
| 上架 OpenRouter 时间 | 2026-02 |

---

## 为什么说它"可直接用"

- 有明确 slug：`nvidia/nemotron-3-nano-30b-a3b:free`
- 当前可直接通过 OpenRouter 调用
- **256K 超长上下文**，免费模型中罕见
- MoE 架构高效（30B 参数仅激活 3B）
- NVIDIA 官方模型，质量有保障

---

## 适合马上试的场景

- 超长文档处理
- 大代码库分析
- 多轮对话保留大量历史
- Agent 长上下文任务

---

## 与 Nemotron 3 Super 120B 的区别

| 对比项 | Nano 30B | Super 120B |
|-------|----------|------------|
| 总参数 | 30B | 120B |
| 激活参数 | 3B | 12B |
| 上下文 | 256K | 262K |
| 定位 | 高效、边缘 | 高性能 |
| 免费版 | ✓ | ✓ |

---

## 最终判断

> **Nemotron 3 Nano 是免费模型中长上下文任务的性价比之选。**

### 我的建议

- **现在就试**：如果你需要 256K 上下文
- **长上下文首选**：比 Super 更轻量，上下文一样大
- **边缘部署友好**：激活参数仅 3B

## 信息来源说明

本文基于 OpenRouter API 直接获取的模型信息整理。

- 来源: https://openrouter.ai/nvidia/nemotron-3-nano-30b-a3b:free
