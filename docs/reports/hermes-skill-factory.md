---
description: Hermes Agent 元技能插件，静默观察工作流，自动将重复模式转化为可复用 Skill，Agent 自己给自己造武器
keywords: Hermes Agent, Skill Factory, 元技能, 自动生成, 工作流, 自改进
date: 2026-04-20
---

# hermes-skill-factory：Agent 自己给自己造武器

## 先给结论

hermes-skill-factory 是一个**元技能（Meta-skill）插件**：它自己是一个 Skill，但它的职责是**观察你的工作流，自动把重复模式变成新的 Skill**。翻译一下就是"Hermes 自己给自己造武器"。每次你解决一个问题——搭建项目、调试代码、创建 PR——这个工作流不会再消失，而是被自动捕获为可复用的 Skill。

| 问题 | 快速判断 |
|------|---------|
| 能直接用吗？ | 能，安装后自动开始观察 |
| 解决什么痛点？ | 每次重复教 Agent 同样的工作流 |
| 核心创新？ | 元技能：一个创造技能的技能 |
| 成熟度？ | Beta，34 ⭐，已在 LobeHub 上架 |
| 值不值得试？ | 日常用 Hermes 的人必装 |

## 关键信息

| 字段 | 值 |
|------|-----|
| 仓库 | [Romanescu11/hermes-skill-factory](https://github.com/Romanescu11/hermes-skill-factory) |
| Stars | ~34 ⭐ |
| 语言 | Python |
| 分类 | 元技能 · 自动 Skill 生成 |
| 生态位置 | Hermes Atlas → Skills 类别，LobeHub Skills Marketplace |

## 三阶段架构

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────────┐
│   Observe   │ ──→ │   Detect    │ ──→ │  Propose & Generate  │
│  静默观察   │     │  模式检测   │     │   提议并生成 Skill   │
└─────────────┘     └─────────────┘     └──────────────────────┘
```

### 1. Observe（观察）

- 静默记录会话活动：命令、序列、方法
- **不打扰用户**，完全后台运行
- 维护一个本地活动日志

### 2. Detect（检测）

分析日志，识别三类模式：

| 模式类型 | 说明 | 示例 |
|---------|------|------|
| 重复动作 | 同样操作反复出现 | 每次都 `git add → commit → push` |
| 领域模式 | 特定领域的工作流 | Python 项目总是 venv → pip → pytest |
| Skill 空缺 | 现有 Skill 没覆盖的模式 | 调试循环没有对应 Skill |

### 3. Propose & Generate（提议与生成）

当触发条件满足时（自动检测到重复 / 用户手动请求），生成完整 Skill 包：

- **SKILL.md**：AI 指令，标准 Hermes Skill 格式（阶段、步骤、质量清单、真实会话示例）
- **plugin.py**：斜杠命令 + 钩子 + 工具注册的脚手架

## 六个斜杠命令

| 命令 | 功能 |
|------|------|
| `/skill-factory propose` | 分析当前会话，提议最佳工作流为 Skill |
| `/skill-factory list` | 显示本次会话生成的所有 Skill |
| `/skill-factory status` | 显示当前追踪的模式 |
| `/skill-factory queue` | 显示待提议的模式队列 |
| `/skill-factory save <name>` | 命名并保存最后提议的 Skill |
| `/skill-factory clear` | 清除当前会话追踪日志 |

## 安装

```bash
git clone https://github.com/Romanescu11/hermes-skill-factory.git
cp skills/skill-factory/SKILL.md ~/.hermes/skills/meta/skill-factory/SKILL.md
cp plugins/skill_factory.py ~/.hermes/plugins/skill_factory.py
hermes skills enable skill-factory
```

安装后 Skill Factory 自动开始观察，无需额外配置。

## 典型用例

| 场景 | 效果 |
|------|------|
| Python 环境搭建 | 自动捕获 venv/pip/conda 工作流为 Skill |
| Git PR 创建 | 把你反复用的 PR 创建模式变成一键 Skill |
| 测试→修复→提交循环 | 调试循环不再每次重新教 |
| 领域特定工作流 | 任何你重复做的任务模式 |
| "把这个存为 Skill" | 显式请求，把刚完成的工作流持久化 |

## 技术亮点

1. **自指系统**：Skill Factory 本身是一个 Skill，它教 Hermes 如何观察和提议——这是程序性元记忆
2. **双文件生成**：同时生成 SKILL.md（AI 指令）和 plugin.py（命令接口），开箱即用
3. **质量约束**：生成的 SKILL.md 必须遵循标准格式，含阶段、步骤、质量清单和真实示例
4. **插件脚手架**：`generate_plugin_py()` 创建可运行的 Python 插件骨架，含 `async def run_<skill_name>()` 处理器

## 适合谁

- ✅ 每天用 Hermes Agent 的人（积累最多，收益最大）
- ✅ 重复性工作流多的开发者
- ✅ 想让 Agent 越用越聪明的用户
- ❌ 偶尔用一次 Agent 的用户（观察数据不够，模式检测不出来）

## 相关地址

- **GitHub 仓库**：[Romanescu11/hermes-skill-factory](https://github.com/Romanescu11/hermes-skill-factory)
- **LobeHub Skills Marketplace**：已上架
- **Hermes Atlas**：[hermesatlas.com](https://hermesatlas.com)
- **上游项目**：[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- **推文来源**：[@NFTCPS](https://x.com/nftcps/status/2046076635200553224)