---
description: 多 Agent 软件工程指挥器，结构化记忆 + Plan-Approve-Execute 三阶段 + 跨 Agent 交接，让 Hermes 能打持久战
keywords: Maestro, 多 Agent, 编排, Plan-Approve-Execute, Beads, UKI, Codex, Claude Code
date: 2026-04-20
---

# Maestro：多 Agent 持久战的指挥官

## 先给结论

Maestro 是一个**本地优先的多 Agent 软件工程指挥器**。一个 CLI、一个磁盘状态模型，就能让 Codex、Claude Code、Gemini 这些异构 Agent 有序协作——结构化记忆、人工审批门、跨 Agent 交接全都有。Hermes Agent 从此能打持久战，不再是短跑选手。

| 问题 | 快速判断 |
|------|---------|
| 能直接用吗？ | 能，CLI 工具，npm/bun 安装 |
| 解决什么痛点？ | 多 Agent 协作无结构，长任务不可恢复 |
| 核心创新？ | Beads 结构化记忆 + UKI 状态编码 |
| 成熟度？ | v1.6.1，25 ⭐，TypeScript 实现 |
| 值不值得试？ | 多 Agent 工作流必看 |

## 关键信息

| 字段 | 值 |
|------|-----|
| 仓库 | [ReinaMacCredy/maestro](https://github.com/ReinaMacCredy/maestro) |
| Stars | ~25 ⭐ |
| Forks | 3-4 |
| 语言 | TypeScript |
| 版本 | v1.6.1 |
| 分类 | 编排 · 多 Agent 协作框架 |
| 生态位置 | Hermes Atlas → Skills 类别 |

## 核心架构

### 工作组织模型

```
Mission（任务）
  ├── Track 1（并行工作流 A）
  │     ├── Bead 1（细粒度任务单元）
  │     ├── Bead 2
  │     └── Bead 3
  ├── Track 2（并行工作流 B）
  │     ├── Bead 4
  │     └── Bead 5
  └── Track 3（并行工作流 C）
        └── Bead 6
```

- **Mission**：顶层任务目标
- **Track**：并行工作流，生命周期 `pending → picked-up → completed`
- **Bead**：最小任务单元，携带可观测、可恢复的状态

### Plan-Approve-Execute 三阶段

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│   Plan   │ ──→ │ Approve  │ ──→ │ Execute  │
│  设计/规格 │     │  人工审批  │     │   实施    │
└──────────┘     └──────────┘     └──────────┘
```

- **Plan**：Agent 生成设计方案和规格
- **Approve**：**人工审批门**，人在回路中
- **Execute**：审批通过后执行实施

### 跨 Agent 交接

支持 Codex、Claude Code、Gemini 之间的结构化交接：

```
交接返回值：
├── 交接 ID
├── 检测到的 Agent/会话身份
├── 当前状态
└── UKI 压缩状态字符串
```

**UKI（Universal Key Index）v5.4** 是 Maestro 的状态编码格式，把工作流上下文压缩成一个字符串：

```
MODE-execute |CURRENT_STATE-execute_in_progress |SESSION_CORE-handoff_real_example |CAUSAL_DRIVERS-NONE |DIVERGENCES-NONE |MAESTRO_RE...
```

支持无状态重建工作流上下文——任何 Agent 拿到 UKI 字符串就能恢复到正确的执行状态。

## 关键特性

### 1. Mission Control TUI

只读终端仪表盘，实时可视化当前 Maestro 状态：

```bash
maestro mission-control --preview --size 120x40 --format plain
```

### 2. 面试驱动规划

通过 `/planning` 命令启动，先通过用户访谈搭建项目上下文，再执行实施。避免 Agent 在不了解项目全貌的情况下盲目开工。

### 3. Preflight Protocol（Phase 0）

多会话感知协议，在实施前运行，建立上下文并防止状态冲突。当你有多个 Agent 同时工作时，这个协议确保它们不会踩到彼此的脚。

### 4. PSM（并行会话管理器）

基于 **git worktrees + tmux** 的隔离开发会话：

- 每个会话在独立的 git worktree 中工作
- 通过 tmux 管理多个终端
- 所有状态存储在 `~/.maestro-psm/`

### 5. 内置 Skills

| Skill | 用途 |
|-------|------|
| `orchestrator` | 编排协调 |
| `review` | 代码审查 |
| `brainstorming` | 头脑风暴 |
| `simplify` | 简化重构 |
| `visual` | 可视化 |
| `research` | 调研 |
| `setup` | 项目初始化 |
| `psm` | 并行会话管理 |
| `release` | 发布管理 |
| `revert` | 回滚 |

## 技术栈

- **运行时**：Bun（现代 JS/TS 工具链）
- **提交规范**：Conventional Commits（`feat(scope):`, `fix(scope):`）
- **测试**：完整测试套件 + TUI 单元测试
- **配套 NPM 包**：`@reinamaccredy/oh-my-opencode`

## 适合谁

- ✅ 多 Agent 软件工程（Codex + Claude Code + Gemini 混编）
- ✅ 长时间编码任务需要结构化记忆和可恢复性
- ✅ 团队协作需要人工审批门
- ✅ 跨 Agent 交接场景（不同 Agent 处理不同阶段）
- ❌ 单 Agent 简单任务（杀鸡用牛刀）
- ❌ 不熟悉 TypeScript/Bun 的团队

## 相关地址

- **GitHub 仓库**：[ReinaMacCredy/maestro](https://github.com/ReinaMacCredy/maestro)
- **NPM 包**：`@reinamaccredy/oh-my-opencode`
- **Hermes Atlas**：[hermesatlas.com](https://hermesatlas.com)
- **上游项目**：[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **推文来源**：[@NFTCPS](https://x.com/nftcps/status/2046076635200553224)