---
description: Hermes Agent 自记忆 + 自训练接班人插件，Agent 边干活边带徒弟，自动微调更便宜的替换模型
keywords: Icarus, 自记忆, 自训练, 微调, 模型替换, fabric, Hermes Agent
date: 2026-04-20
---

# Icarus Plugin：Agent 边干活边带徒弟，退休计划已安排好

## 先给结论

Icarus Plugin 是 Hermes Agent 生态里**最热门的社区项目**（51 ⭐）。它做两件事：**自记忆**（Agent 的工作经验跨会话、跨平台共享）和**自训练接班人**（用 Agent 自己的工作历史微调更便宜的模型，评估通过后自动切换）。Agent 边干活边带徒弟，退休计划已经安排好了。

| 问题 | 快速判断 |
|------|---------|
| 能直接用吗？ | 能，插件安装后自动开始捕获 |
| 解决什么痛点？ | Agent 没有跨会话记忆 + 模型成本不可控 |
| 核心创新？ | 自训练循环：用自己的经验微调自己的替代品 |
| 成熟度？ | 最活跃，51 ⭐，4 钩子 11 工具 |
| 值不值得试？ | 重度 Hermes 用户必装 |

## 关键信息

| 字段 | 值 |
|------|-----|
| 仓库 | [esaradev/icarus-plugin](https://github.com/esaradev/icarus-plugin) |
| Stars | ~51 ⭐（5 个项目中最热门） |
| 语言 | Python + Bash |
| 分类 | 记忆 · 自训练模型替换 |
| 生态位置 | Hermes Atlas，获 Teknium 认可 |
| 父项目 | icarus-daedalus（Icarus Memory Protocol） |

## 记忆层：~/fabric/

Agent 的工作经验存储在 `~/fabric/` 目录——本地 Markdown 文件系统，带 YAML 前置元数据：

```yaml
---
agent: hermes
platform: telegram
timestamp: 2026-04-20T14:30:00
type: decision
tier: high
tags: [debugging, python, pytest]
summary: "Fixed test failure by patching mock path"
training_value: high  # ← 关键：决定是否进入训练数据
refs: [issue-42, pr-15]
---
```

### 条目链接

fabric 条目之间可以建立链接关系，形成 Agent 交互图：

| 链接类型 | 含义 |
|---------|------|
| `review_of` | 这条是对另一条的评审 |
| `revises` | 这条修订了另一条 |
| `assigned_to` | 这条任务分配给另一个 Agent |

### 检索排序

`fabric-retrieve.py` 使用 **7 个评分信号**进行排序：

关键词匹配、标签匹配、项目匹配、Agent 匹配、时效性、层级匹配、类型匹配 + 引用链

## 4 个生命周期钩子

| 钩子 | 触发时机 | 功能 |
|------|---------|------|
| `on_session_start` | 会话开始 | 加载最近 fabric 条目，注入为 Agent 上下文 |
| `on_session_end` | 会话结束 | 自动写会话摘要（仅 2+ 实质性交互时） |
| `post_llm_call` | LLM 调用后 | 实时检测决策和完成，写入 fabric |
| `pre_llm_call` | LLM 调用前 | 基于用户消息的查询感知检索 |

**关键**：`post_llm_call` 用正则实时检测决策和完成，自动写入 fabric——用户完全无感，Agent 就在积累经验。

## 11 个注册工具

| 工具 | 功能 |
|------|------|
| `fabric_write` | 写入条目，支持链接和 training_value |
| `fabric_curate` | 标注条目的训练价值 |
| `fabric_train` | 从 fabric 数据启动 Together AI 微调 |
| `fabric_train_status` | 查询微调进度，完成时更新模型注册表 |
| `fabric_models` | 列出所有训练模型及评估分数 |
| `fabric_switch_model` | 评估通过后激活替换模型 |
| `fabric_eval` | 评估候选模型 |
| `fabric_retrieve` | 检索相关记忆 |
| `fabric_read` | 读取特定条目 |
| `fabric_search` | 搜索记忆 |
| `fabric_list` | 列出条目 |

## 自训练循环：核心创新

这是 Icarus 最独特的地方——**Agent 用自己的工作经验训练自己的替代品**：

```
1. Agent 正常工作
   ↓
2. 钩子自动捕获高价值决策（training_value = high）
   ↓
3. fabric_train(suffix="my-agent-v2")
   → 导出训练对 → 上传 Together AI → 启动微调
   ↓
4. fabric_eval(candidate_model=...)
   → 评估微调模型
   ↓
5. fabric_switch_model(model_id=...)
   → 评估通过 → 切换到更便宜的模型
   ↓
6. 原模型设为 config.yaml 中的 fallback
```

### 训练数据质量过滤

不是所有经验都值得训练。Icarus 用 `training_value` 标签过滤：

| 模式 | 筛选标准 |
|------|---------|
| `high-precision` | 仅使用：高价值 + 已验证 + 有链接评审 + 结构化会话 + 有证据的完成条目 |
| `balanced` | 高价值 + 正常价值，排除低价值 |
| `all` | 全部条目（不推荐） |

### 成本优化效果

典型场景：Claude Sonnet（$3/MTok）做日常任务 → 微调 Qwen（几乎免费）处理同类任务 → 仅在复杂任务时 fallback 回 Claude。

## 典型用例

### 多 Agent 交接

```
Builder Agent → fabric_write(type="code-session", assigned_to="daedalus")
Reviewer Agent → on_session_start 看到 Builder 的条目
Reviewer Agent → 写链接评审 fabric_write(review_of=builder_entry_id)
```

### 跨平台记忆

- Slack 上做的决策 → Telegram 上可召回
- Discord 上的代码审查 → CLI 中可引用
- 所有平台共享同一个 `~/fabric/` 目录

### Obsidian 集成

fabric 条目是标准 Markdown 文件，可以直接在 Obsidian 中浏览和搜索 Agent 的记忆——这对知识管理重度用户非常友好。

## 为什么是插件而不是 MCP？

Icarus 需要**生命周期钩子**（自动记忆捕获）、**训练集成**和**模型生命周期管理**——这些 MCP 协议不提供。插件架构是正确的选择。

## 适合谁

- ✅ 重度 Hermes Agent 用户（积累最多经验，收益最大）
- ✅ 多 Agent 协作场景（Builder → Reviewer 交接）
- ✅ 模型成本敏感（想用便宜模型替代贵模型）
- ✅ Obsidian 用户（Agent 记忆直接在知识库中可见）
- ❌ 偶尔用 Agent 的用户（经验积累不够，训练数据不足）
- ❌ 没有 Together AI 账号的用户（微调功能需要）

## 相关地址

- **GitHub 仓库**：[esaradev/icarus-plugin](https://github.com/esaradev/icarus-plugin)
- **父项目**：[icarus-daedalus](https://github.com/esaradev/icarus-daedalus)（Icarus Memory Protocol）
- **Hermes Atlas**：[hermesatlas.com](https://hermesatlas.com)
- **上游项目**：[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **推文来源**：[@NFTCPS](https://x.com/nftcps/status/2046076635200553224)