---
description: Hermes Agent 安全加固 fork，集成 DeepMind CaMeL 双 LLM 信任边界架构，从结构上杜绝 prompt 注入攻击
keywords: Hermes Agent, CaMeL, prompt 注入, 安全, 双 LLM, P-LLM, Q-LLM
date: 2026-04-20
---

# hermes-agent-camel：用 CaMeL 双 LLM 架构让 Agent 不再翻车

## 先给结论

hermes-agent-camel 是 Hermes Agent 的安全加固 fork，核心改动是把 DeepMind 的 **CaMeL（Capabilities with Middleware for Efficient LLM）** 信任边界架构塞进了 Agent 运行循环。效果：prompt 注入攻击从结构上被阻断，不是靠过滤、不是靠扫描，是**数据流本身就不允许攻击发生**。

| 问题 | 快速判断 |
|------|---------|
| 能直接用吗？ | 能，fork 自 Hermes Agent 主线，功能完整 |
| 解决什么痛点？ | 生产环境不敢上 Agent，怕 prompt 注入 |
| 安全性如何？ | 结构性保证，比概率性防御强一个量级 |
| 有没有已知漏洞？ | 有，分支引导攻击（Branch Steering）仍可能绕过 |
| 值不值得试？ | 生产环境必看，个人玩可暂缓 |

## 关键信息

| 字段 | 值 |
|------|-----|
| 仓库 | [nativ3ai/hermes-agent-camel](https://github.com/nativ3ai/hermes-agent-camel) |
| Stars | ~12 ⭐ |
| 语言 | Python |
| 上游 | NousResearch/hermes-agent（57K+ ⭐） |
| 分类 | 安全 · CaMeL 信任边界 |
| 生态位置 | Hermes Atlas → Security 类别 |

## 核心架构：双 LLM 分离

传统 Hermes Agent 用**单 LLM 循环**，安全靠容器隔离和命令审批——都是事后措施。hermes-agent-camel 改成**双 LLM 架构**：

```
用户请求
  ↓
P-LLM（特权 LLM）→ 生成控制流计划（伪 Python）
  ↓
CaMeL 解释器 → 逐步执行计划
  ↓（遇到不受信数据）
Q-LLM（隔离 LLM）→ 处理外部数据
  ↓
输出被隔离为类型化变量，永远不回流到 P-LLM
```

### P-LLM vs Q-LLM

| 角色 | 职责 | 能看到什么 |
|------|------|-----------|
| **P-LLM** | 生成计划、控制流程 | 只看可信数据，永远不看外部输入 |
| **Q-LLM** | 处理不受信数据 | 可以看外部数据，但输出被隔离 |

关键：Q-LLM 的输出**填充类型化变量**，但**永远不直接影响 P-LLM 的决策**。即使 Q-LLM 被 prompt 注入攻破，攻击者也无法控制 Agent 的行为流程。

## CaMeL 解释器

解释器是整个安全保证的核心引擎：

1. **数据流图追踪**：实时追踪每个变量的来源和传播路径
2. **能力标记**：每个变量携带安全能力标签，操作被能力门控
3. **策略执行**：未授权的数据外泄或权限提升会被结构性阻止

## 已知局限：分支引导攻击

研究论文（arXiv:2601.09923）指出 CaMeL 架构仍可能受**分支引导攻击**影响：

- 恶意环境胁迫 Q-LLM 返回特定数据
- 这些数据迫使执行进入攻击者选择的合法计划分支
- 不是直接注入，而是通过"合法路径"间接控制

**应对**：这不是 CaMeL 独有的问题，所有 Agent 安全架构都面临类似挑战。CaMeL 至少把攻击面从"任意注入"缩小到"分支引导"，已经是结构性进步。

## 生态关联

hermes-agent-camel 是 nativ3ai 安全套件的一部分：

| 项目 | 职责 |
|------|------|
| **hermes-agent-camel** | 运行时信任边界（Agent 循环内） |
| **clawshield** | 运行时安全层 |
| **hermes-payguard** | 支付安全（资金流动、审批、支付通道） |

这种拆分比单体方案更干净：安全策略执行（CaMeL）和金融护栏（PayGuard）各管各的。

## 适合谁

- ✅ 要在生产环境部署自主 Agent 的团队
- ✅ 金融/交易类 Agent 工作流
- ✅ 企业环境需要结构性安全保证
- ❌ 个人用户日常使用（安全需求没那么高）
- ❌ 不理解 CaMeL 论文就上生产（至少读一遍原理）

## 相关地址

- **GitHub 仓库**：[nativ3ai/hermes-agent-camel](https://github.com/nativ3ai/hermes-agent-camel)
- **上游项目**：[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **CaMeL 论文**：DeepMind - Capabilities with Middleware for Efficient LLM
- **分支引导攻击论文**：arXiv:2601.09923
- **Hermes Atlas**：[hermesatlas.com](https://hermesatlas.com)
- **推文来源**：[@NFTCPS](https://x.com/nftcps/status/2046076635200553224)