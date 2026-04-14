# Open Agents 技术架构总结

## 相关地址

- 项目仓库：https://github.com/vercel-labs/open-agents
- README：https://github.com/vercel-labs/open-agents/blob/main/README.md
- 官方演示站：https://open-agents.dev/
- Vercel 部署入口：https://vercel.com/new/clone?repository-url=https://github.com/vercel-labs/open-agents

## 一句话判断

`vercel-labs/open-agents` 不是一个简单的聊天式 coding agent，而是一套 **运行在 Vercel 上的云端后台编程 Agent 参考架构**。

它最重要的点不在模型本身，而在这条链路：

```text
Web App -> Durable Agent Workflow -> Sandbox VM
```

也就是把“Prompt 到改代码”的过程拆成：

- 用户交互层
- 可持久化的 Agent 工作流层
- 独立执行环境层

---

## 1. 三层架构

### Web 层

负责：

- 登录与认证
- 会话管理
- Chat UI
- 流式展示 Agent 输出
- 启动 / 恢复 Agent run

这一层本质上是控制台与入口，不负责真正执行编程任务。

### Agent Workflow 层

负责：

- 多轮推理与工具调用
- 持久化 Agent 执行状态
- 长任务恢复
- 取消运行
- 管理 run 生命周期

这里的关键不是“调用一次模型”，而是把 Agent 建模成 **durable workflow**。

### Sandbox 层

负责：

- 文件系统操作
- shell 执行
- git 操作
- 启动 dev server
- 暴露 preview port
- snapshot / hibernate / resume

这一层是真正干活的远程工作机。

---

## 2. 最关键的设计：Agent 不在 Sandbox 里

README 里最重要的一句是：

> the agent is not the sandbox

这意味着：

- Agent runtime 不跑在 VM 里
- Sandbox 只是执行环境
- Agent 通过工具接口与 sandbox 交互

### 这带来的架构价值

#### 控制平面 / 执行平面分离

- Agent 负责决策与编排
- Sandbox 负责执行命令、改文件、跑服务

这是一种更成熟的云端 Agent 架构，而不是把所有东西塞进同一个容器进程。

#### 生命周期解耦

- workflow 可以持久化和恢复
- sandbox 可以独立 hibernate / resume
- 两者不必绑定在单个 HTTP 请求上

#### 更容易替换底层

未来理论上可以独立替换：

- 模型 provider
- workflow 引擎
- sandbox 实现

而不会整套系统一起重写。

---

## 3. 执行模型：不是 request-response，而是 durable workflow

它不是这种模式：

```text
请求进来 -> 同步跑 Agent -> 返回
```

而是：

1. chat 请求触发一个 workflow run
2. workflow 多步推进 agent 执行
3. 前端通过流观察 run 状态
4. 用户断线后可重新连接并恢复同一个 run

### 技术意义

#### 适合长任务

例如：

- clone repo
- 安装依赖
- 跑测试
- 修改多文件
- 起 dev server
- commit / PR

这些都天然不是一次请求能优雅承载的。

#### 支持恢复与取消

这让它更像“后台任务系统”，而不是一次性脚本。

---

## 4. Sandbox 架构

Sandbox 是整个系统的执行平面。

README 提到的当前特征包括：

- 使用 Vercel sandboxes
- 基于 base snapshot 恢复
- 开放端口 `3000`、`5173`、`4321`、`8000`
- 不活跃后自动 hibernate

### 这代表的设计取向

#### Sandbox 是可恢复工作空间

不是短命容器，而是带状态的执行环境。

#### Snapshot 是关键优化点

它可以带来：

- 更快启动
- 更一致环境
- 更稳定恢复

#### 明显面向真实开发任务

开放的端口配置说明它就是为 Next.js、Vite、Astro、通用本地服务预览而设计的。

---

## 5. GitHub 集成是主路径，不是附加功能

这个项目不仅是“能改代码”，还内建了：

- GitHub App 集成
- 私有仓库访问
- branch push
- PR 创建

也就是说，它的终点不是生成代码片段，而是进入真实的开发流程。

这让它更像：

- 云端 AI 开发协作者
- 后台 PR 生产器
- coding workflow automation layer

---

## 6. 工具系统的作用

当前 Agent 支持：

- file
- search
- shell
- task
- skill
- web

这说明它采用的是典型的 **tool-using agent** 架构。

关键在于：

- Agent 不直接拥有文件系统
- 它通过工具远程操作 sandbox
- 每一步都可以持久化、拆步推进

这和 durable workflow 很契合。

---

## 7. Repo 结构说明了它的边界划分

README 给出的 repo layout：

```text
apps/web         Next.js app, workflows, auth, chat UI
packages/agent   agent implementation, tools, subagents, skills
packages/sandbox sandbox abstraction and Vercel sandbox integration
packages/shared  shared utilities
```

这个拆法说明项目在边界上是清楚的：

- `apps/web`：用户交互与平台入口
- `packages/agent`：Agent 推理与编排
- `packages/sandbox`：执行环境抽象
- `packages/shared`：公共逻辑

这让它更适合作为“可 fork 的产品骨架”。

---

## 8. 部署要求反映了它不是轻量 demo

从 README 看，至少会涉及：

- PostgreSQL
- JWE / token encryption
- Vercel OAuth
- GitHub App
- 可选 Redis / KV
- 可选 ElevenLabs transcription

这说明它的真实形态是：

> 一个带数据库、认证、平台集成、执行环境和 GitHub 权限体系的 Agent 平台。

它不是单机 CLI，也不是一段 demo script。

---

## 9. 这个架构的优点

### 1. 适合后台 Agent

比同步调用更适合长任务、多步任务、可恢复任务。

### 2. 控制平面 / 执行平面分离

这是整套设计最成熟的地方之一。

### 3. 更接近真实产品

它已经覆盖：

- auth
- workflow
- sandbox
- GitHub
- preview
- streaming UI

### 4. 适合二次开发

README 也明确说了：这个项目是拿来 fork 和改造的，不是黑盒产品。

---

## 10. 架构代价

### 1. 系统复杂度高

你得同时理解：

- Next.js
- durable workflow
- sandbox orchestration
- OAuth
- GitHub App
- secret management

### 2. Vercel 绑定比较深

它虽然开源，但整体明显是围绕 Vercel 生态设计的。

### 3. 更像产品底座，不像最省事的个人工具

如果你只是想自己本地跑一个 coding agent，这套架构可能偏重。

---

## 最后的判断

如果只用一句话总结：

> **Open Agents 的真正价值，不在“会写代码”，而在“把 coding agent 做成了一个可持久化、可恢复、可接入 GitHub 工作流的云端执行系统”。**

如果你在看：

- 云端 coding agent
- durable agent workflow
- sandbox orchestration
- AI 与 GitHub 开发流结合

这个项目非常值得研究。

## 信息来源说明

本文基于 `vercel-labs/open-agents` 当前 README 信息整理，重点关注其技术架构，而不是产品宣传角度。