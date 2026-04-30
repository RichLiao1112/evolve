---
description: Warp 终端的 Rich Input 功能详解 —— 为 CLI 编程 Agent 提供的增强输入层，支持 @ 文件引用、语音输入、IDE 风格编辑和 Slash Commands。
keywords: Warp, Rich Input, CLI Agent, Claude Code, Codex, 终端工具, 编程效率
date: 2026-04-30
---

# Warp Rich Input 使用指南

Warp 是一个现代化终端，它的 **Rich Input** 功能为 CLI 编程 Agent 提供了一层增强输入界面。

如果你正在用 Claude Code、Codex、OpenCode 等 CLI Agent 写代码，Rich Input 能显著改善输入体验。

## 相关地址

- **Warp 官网**: https://www.warp.dev
- **Warp 文档**: https://docs.warp.dev

---

## Rich Input 是什么

一句话：

> Rich Input = 给 CLI 编程 Agent 用的增强版输入框 / Prompt 编辑器。

它不是模型能力本身，而是 Warp 在终端里为受支持的三方 CLI Agent 提供的一层更舒服的输入界面。

开启后，你的工作流变成：

1. 你在 Warp 的 Rich Input 编辑器里输入 prompt；
2. 用 `@` 关联文件、目录、上下文；
3. 提交后，Warp 把内容传递给当前正在运行的 CLI Agent；
4. 对 Agent 来说，就像你在它的原生输入位置打了一段 prompt。

```
Warp Rich Input = 三方 CLI Agent 前面的增强输入层
```

实际执行任务的仍然是下面跑的 Agent：运行 Claude Code 就提交给 Claude Code，运行 Codex 就提交给 Codex，运行 OpenCode 就提交给 OpenCode。

!!! note "关于上下文传递"
    普通文本 prompt 可以近似理解为原样传递。但 `@` 文件、图片、slash command、skills 等富上下文，Warp 会做额外处理，将上下文整理、注入或转换成对应 Agent 能理解的形式后再提交。

---

## 核心能力

### IDE 风格的 Prompt 编辑

相比普通终端输入，Rich Input 更像一个小型编辑器：

| 能力 | 说明 |
|------|------|
| 多行输入 | 适合写长需求、调试说明 |
| 自动换行 | 不用手动管行宽 |
| 鼠标定位 / 选文本 | 终端里也能用鼠标了 |
| 复制 / 剪切 / 粘贴 | 标准编辑操作 |
| 撤销 | `Ctrl-Z` 有效 |
| 按词移动光标 | `Ctrl-Left` / `Ctrl-Right` |
| Vim keybindings | 对 Vim 用户友好 |

适合编写较长的需求、调试说明、代码审查说明、重构任务描述等。

### @ 引用文件、目录和上下文

Rich Input 支持通过 `@` 引用上下文，可以引用：

- **文件**：`@src/components/Button.tsx`
- **目录**：`@src/api`
- **代码符号**：函数、类、接口
- **终端输出块**：之前的命令输出
- **Warp Drive 对象**：workflows、notebooks、rules

这是最常用的功能，后面有专门章节详解。

### 语音输入

Rich Input 支持语音输入，可以直接口述 prompt 而不用手动打字。

### Slash Commands / Skills

通过 `/` 可以调出：

- 保存过的 prompts
- Skills
- Warp Drive 内容
- 与当前 Agent 相关的命令

运行 Claude Code 时，Warp 会展示与 Claude Code 相关的 skills 或命令。

### Agent 工具栏

Rich Input 通常和 Warp 底部的 agent utility bar 配合使用。从工具栏中可以：

- 打开 Rich Input
- 查看文件
- 查看代码变更
- 管理当前 agent session

---

## 打开与关闭

### 打开 Rich Input

**方式一：快捷键**

```
Ctrl-G
```

快捷键可以在 `Settings > Keyboard shortcuts` 中修改，搜索 `Rich Input`。

**方式二：点击按钮**

受支持的 CLI Agent 运行时，Warp 底部 Agent 工具栏会出现 Rich Input 按钮，点击即可。

### 关闭 Rich Input

**临时关闭**：按 `Esc`。

**关闭自动弹出**（推荐）：

进入 `Settings > Agents > Third party CLI agents`，关闭：

- `Auto show/hide based on agent status`
- `Auto open on session start`

这样 Rich Input 基本不会主动打扰你。

**隐藏底部按钮**：右键底部 agent utility bar，移除 Rich Input chip。

---

## 使用 @ 引用上下文

这是 Rich Input 最有价值的功能。

### 基本用法

在 Rich Input 中输入 `@`，Warp 会弹出上下文菜单。继续输入关键词过滤，选中后插入引用 token。

### 引用文件

```
请阅读 @src/components/Button.tsx，帮我解释这个组件的状态逻辑。
```

```
请参考 @package.json 和 @src/main.ts，判断这个项目的启动流程。
```

### 引用目录

```
请基于 @src/api 目录，找出用户登录接口相关代码。
```

```
请阅读 @src/components 目录，帮我总结组件结构，并指出是否有重复组件可以合并。
```

### 引用代码符号

```
请解释 @main 的调用链。
```

Warp 会找到匹配的 `main()` 函数，并带上行号作为上下文。适合精准分析某个函数、类或接口。

### 引用终端输出块

如果之前运行过 `cargo clippy`，可以写：

```
请根据 @cargo clippy 的报错帮我修复问题。
```

不需要手动复制整段日志，Warp 会把相关输出块作为上下文。

### 引用 Warp Drive 对象

`@` 还可以引用 Warp Drive 里的：

- **Workflows**：保存过的命令或脚本
- **Notebooks**：文档、说明、可执行笔记
- **Rules**：可复用的规则和约束

### @ 使用注意事项

| 要点 | 说明 |
|------|------|
| 搜索基于 Git 仓库根目录 | 即使在子目录中，也能引用仓库内任意位置的文件 |
| 遵守 `.gitignore` | 被忽略的文件不会出现在搜索结果里 |
| 不需要提前索引 | Git 仓库中的文件搜索直接可用 |
| 非受支持 Agent 体验不完整 | 普通 CLI（如 Hermes）可能无法触发完整的 Rich Input 能力 |

---

## 推荐 Prompt 模板

### 分析文件

```
请阅读 @文件路径，解释它的核心逻辑，并指出可能的风险点。
```

### 分析目录

```
请阅读 @目录路径，总结这个模块的职责、核心文件和主要调用关系。
```

### 修复报错

```
请根据 @报错输出块，定位问题原因，并给出最小修改方案。
```

### 代码审查

```
请基于 @相关文件，做一次代码审查，重点关注：
1. 类型安全；
2. 异常处理；
3. 边界条件；
4. 可维护性。
```

### 重构建议

```
请阅读 @相关目录，判断是否存在重复逻辑，并给出重构建议。不要直接修改代码，先给方案。
```

---

## 常用操作速查

| 操作 | 快捷键 / 路径 |
|------|--------------|
| 打开 Rich Input | `Ctrl-G` 或底部工具栏按钮 |
| 关闭当前输入框 | `Esc` |
| 引用文件/目录 | 输入 `@` 后搜索选择 |
| 关闭自动弹出 | `Settings > Agents > Third party CLI agents` |
| 修改快捷键 | `Settings > Keyboard shortcuts`，搜索 Rich Input |

---

## 一句话总结

Warp Rich Input 是三方 CLI Agent 前面的增强输入层：你在 Rich Input 里写 prompt、用 `@` 关联文件和上下文，Warp 再把处理后的输入提交给正在运行的 CLI Agent。编辑体验更好，上下文管理更方便，Agent 执行逻辑不变。
