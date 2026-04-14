# OpenClaw 和 Hermes 怎么接 OpenRouter 免费模型

## 一句话结论

如果你想把 **OpenRouter 免费模型** 接进自己的日常工作流，`OpenClaw` 和 `Hermes` 的配置思路并不一样：

- **Hermes**：原生就把 `OpenRouter` 当成正式 provider，用起来更直接
- **OpenClaw**：更像是“项目内部 AI 路由层”，是否能接 OpenRouter，要看具体模块有没有走 **OpenAI-compatible** 通道

所以最实用的判断是：

> **想快速稳定地用上 OpenRouter 免费模型，Hermes 更顺手；想在 OpenClaw 体系里接入，需要先分清你改的是哪条业务链路。**

---

## 这篇文章解决什么问题

很多人看到 OpenRouter 上有免费模型，会自然想到两件事：

1. 我能不能把它接到现有 Agent 里？
2. 如果我同时在用 OpenClaw 和 Hermes，哪边更容易配？

这两个问题表面都叫“配置模型”，但底层其实不是同一类系统：

- **Hermes** 是一个通用 Agent 框架，本身就支持多 provider、多模型切换
- **OpenClaw** 在我当前使用的这套工程里，更接近一个业务项目内部的 AI 接入层，不同模块支持能力并不完全一致

因此，配置方式不能混着看。

---

## 先说结论：两者的难点完全不同

| 项目 | Hermes | OpenClaw |
| --- | --- | --- |
| 接 OpenRouter 免费模型的难度 | 低 | 中到高 |
| 是否原生支持多 provider | 是 | 看具体模块实现 |
| 是否适合快速切换免费模型试验 | 非常适合 | 只在部分链路适合 |
| 最常见配置入口 | `hermes model` / `config.yaml` / `.env` | 环境变量 + 项目内 AI settings API |
| 最容易踩的坑 | 只配了 key 没切 provider | 以为所有模块都能直接换 OpenRouter |

最核心的差异是：

- **Hermes 的问题是“怎么选和怎么切”**
- **OpenClaw 的问题是“这条链路到底支不支持 OpenAI-compatible provider”**

---

## Hermes：接 OpenRouter 免费模型，基本就是标准路径

Hermes 对 OpenRouter 的支持是正式能力，而不是旁路 hack。

从 Hermes 文档和当前工具状态看，最简单的配置路径通常是：

1. 配置 `OPENROUTER_API_KEY`
2. 切换 provider 到 `openrouter`
3. 选择一个免费模型 slug
4. 用 `hermes model` 或 `model_aliases` 做日常切换

### 最简单的做法

```bash
hermes config set OPENROUTER_API_KEY sk-or-...
hermes model
```

然后在交互式模型选择里：

- 选 provider：`openrouter`
- 再选你想试的免费模型

这是最适合大多数人的方式，因为：

- 不容易配错字段
- 对后续切换模型最友好
- 不需要先理解太多内部配置结构

### 如果你想把免费模型固定成常用入口

更工程化的做法是给它起一个 alias。

例如在 `~/.hermes/config.yaml` 里维护这样的配置：

```yaml
model_aliases:
  or-free:
    model: openrouter/elephant-alpha
    provider: openrouter
```

之后就可以直接：

```bash
/model or-free
```

或者在 CLI / gateway 里切过去。

### Hermes 为什么特别适合免费模型试验

因为 Hermes 的 provider 体系本来就是围绕“多模型切换”设计的，所以 OpenRouter 免费模型在它这里，不是“替代默认主路”的非常规玩法，而是很自然的一种模型来源。

这会带来几个直接好处：

- 试错成本低
- 切换速度快
- 可以把免费模型放进常备模型池
- 适合做轻量 Agent、长文档处理、网页总结、工具调用试验

所以如果你的目标是：

- 快速试多个免费模型
- 让同一个 Agent 随时切换模型
- 把 OpenRouter 当成长期模型来源之一

那 **Hermes 明显比 OpenClaw 更顺手**。

---

## Hermes 实操建议：免费模型怎么配得更稳

### 1. 不要只看“免费”，先看模型 slug 是否稳定

OpenRouter 免费模型常常会变。

你真正要检查的是：

- 模型 slug 有没有变
- provider 有没有缩减
- 免费状态是否还在
- 是否还能满足你需要的 context / output / tool support

### 2. 把“免费模型”当成分层模型池的一层

比较稳的用法不是“所有任务都上免费模型”，而是这样分层：

- **免费模型**：长文档初筛、公开资料总结、低敏任务、轻量 Agent
- **主力商业模型**：重要任务、高复杂推理
- **高隐私模型 / 本地模型**：敏感数据

这比只盯着价格更合理。

### 3. 如果是网关或多端场景，先确认当前 active provider

很多时候问题不是 key 没配，而是：

- key 已经在 `.env`
- 但 active provider 还停在别的模型上

所以配完之后，最好检查一次：

```bash
hermes status
hermes doctor
```

确认：

- OpenRouter key 已生效
- 当前 provider / model 已真的切过去

---

## OpenClaw：能不能接 OpenRouter，先别急着改，先分链路

OpenClaw 这边最容易误判的一点是：

> **不是所有看起来“在用 OpenClaw”的地方，都能直接切成 OpenRouter 免费模型。**

我当前这套工程里，相关代码已经明确区分了不同 AI target 和 provider：

- `provider` 支持：`openclaw`、`openai`、`codex`、`hermes`、`local`
- 各业务模块有自己的 target
- 配置来源有优先级：**DB 持久化配置 → 环境变量 → 默认值**

关键文件里已经能看到这些定义：

- `server/src/modules/ai-settings/ai-settings.types.ts`
- `server/src/modules/ai-settings/ai-settings.controller.ts`
- `server/src/modules/ai-runtime/providers/openai-compatible.provider.ts`

### 当前代码里最重要的现实结论

在这套 OpenClaw / research 项目实现里：

- `xHomeDigest` 这类链路，已经具备 **OpenAI-compatible** 调用能力
- 也就是说，它理论上可以直接接 OpenRouter
- 但不是每个模块都已经被抽象成统一的 OpenAI-compatible provider

所以如果你说“我要把 OpenClaw 配成 OpenRouter 免费模型”，必须先回答：

- 你要切的是 **哪一个 target**？
- 它走的是 `openclaw` provider 还是 `openai-compatible` provider？
- 当前模块是否真的支持 `provider=openai` 这条路径？

这一步不搞清楚，后面改环境变量往往改了也没效果。

---

## OpenClaw 当前最实用的接法：优先走 AI target，而不是只改 openclaw agent

在当前代码结构里，有两类接口非常容易让人混淆：

### 1. `openclaw-agents`

这个接口更像是在维护 OpenClaw agent 名称，例如：

- `openclaw:docs`
- 某个 OpenClaw 内部 agent 标识

适合改“OpenClaw provider 自己内部用哪个 agent”。

### 2. `targets`

这个接口才是真正的 **AI 路由配置入口**，因为它允许你设置：

- `provider`
- `model`
- `timeoutMs`
- `temperature`
- `fallbackProvider`
- `extra`

也就是说：

> 如果你要把某条业务链路切到 OpenRouter 免费模型，优先应该看 `PATCH /ai-settings/targets`，而不是只盯着 `PATCH /ai-settings/openclaw-agents`。

---

## OpenClaw 的推荐配置思路

### 场景一：你要改的是支持 OpenAI-compatible 的链路

这是最理想的情况。

当前代码里的 `openai-compatible.provider.ts` 明确会读这些配置：

- `X_HOME_DIGEST_OPENAI_API_KEY`
- `OPENAI_API_KEY`
- `X_HOME_DIGEST_OPENAI_BASE_URL`
- `OPENAI_BASE_URL`

并向：

```text
{baseUrl}/chat/completions
```

发起标准 OpenAI-compatible 请求。

这就意味着，如果你要让某条链路接 OpenRouter，核心思路是：

- provider 设成 `openai`
- model 写成 OpenRouter 的模型 slug
- `base_url` 指向 `https://openrouter.ai/api/v1`
- API key 用 OpenRouter key

例如从环境变量角度，可以这样理解：

```bash
X_HOME_DIGEST_AI_PROVIDER=openai
X_HOME_DIGEST_AI_MODEL=openrouter/elephant-alpha
X_HOME_DIGEST_OPENAI_BASE_URL=https://openrouter.ai/api/v1
X_HOME_DIGEST_OPENAI_API_KEY=sk-or-...
```

### 场景二：你改的是仍强依赖 OpenClawChatClient 的链路

这时候就不能想当然地把 model 改成 OpenRouter slug。

因为这类模块的真实问题不是“model 名不对”，而是：

- 调用路径没切
- provider 还是 `openclaw`
- 请求客户端仍然是 OpenClaw 专用实现

这类情况下，要么：

- 继续使用 OpenClaw provider 的 agent 模型名
- 要么先做代码层 provider 抽象，再接 OpenRouter

也就是说：

> **对 OpenClaw 而言，能不能接 OpenRouter，首先是架构问题，其次才是配置问题。**

---

## OpenClaw 的一个更稳做法：直接改 target 配置

如果你的项目已经把目标链路接入 `ai-settings/targets`，那么推荐从这条路入手。

从当前 DTO 定义来看，`PATCH /ai-settings/targets` 接受的是类似这样的对象：

```json
{
  "xHomeDigest": {
    "provider": "openai",
    "model": "openrouter/elephant-alpha",
    "timeoutMs": 120000,
    "temperature": 0.3
  }
}
```

再配合环境变量：

```bash
X_HOME_DIGEST_OPENAI_BASE_URL=https://openrouter.ai/api/v1
X_HOME_DIGEST_OPENAI_API_KEY=sk-or-...
```

这样更符合当前代码设计，也比“继续把所有东西都塞进 openclaw agent 名称”更清晰。

---

## OpenClaw 和 Hermes 的配置哲学，其实正好相反

这是我觉得最值得讲清楚的一点。

### Hermes 的思路

Hermes 更像一个通用模型编排器：

- provider 是一等公民
- 模型切换是常规操作
- OpenRouter 是正式支持的模型来源
- 免费模型很适合成为模型池的一层

所以在 Hermes 里，你考虑的是：

- 这模型值不值得进我的常备模型池？
- 这个 provider 适合哪些任务？
- 是否要给它起 alias？

### OpenClaw 的思路

OpenClaw 在当前这套项目里，更像业务系统里的 AI 调度层：

- 不是所有模块都同等抽象
- provider 能力依赖具体实现
- 配置是按 target 分散到不同业务链路里的
- “切模型”有时不是单纯改一个字符串，而是切一条调用路径

所以在 OpenClaw 里，你优先考虑的是：

- 这条链路走的到底是什么 provider adapter？
- 这条链路是否已经支持 OpenAI-compatible？
- 应该改 target 配置，还是得改代码？

---

## 如果你的目标只是“尽快把免费模型跑起来”

我的建议非常直接：

### 先上 Hermes

因为它更适合：

- 快速试模型
- 快速切 provider
- 快速验证“这个免费模型值不值得长期用”

### 再决定是否把它纳入 OpenClaw 链路

当你已经在 Hermes 里验证过某个免费模型确实靠谱，再考虑：

- 哪些 OpenClaw 业务链路值得接进去
- 是不是只接 `xHomeDigest` 就够了
- 有没有必要做更统一的 OpenAI-compatible provider 抽象

这是一个更省时间的顺序。

因为很多人会反过来做：

- 先在 OpenClaw 里折腾半天接入
- 结果最后发现模型本身并不适合自己的任务

这会浪费很多工程时间。

---

## 我会怎么选

如果我现在要把 OpenRouter 免费模型接进自己的系统，我会这样做：

### 路线 A：快速试验

直接用 Hermes：

- 配 `OPENROUTER_API_KEY`
- 切 provider 到 `openrouter`
- 选免费模型
- 跑几类真实任务压测

### 路线 B：业务链路接入

先确认 OpenClaw 某条链路是否支持 OpenAI-compatible：

- 如果支持：改 `targets`，配 OpenRouter base URL + key
- 如果不支持：先别硬配，先决定要不要抽象 provider

### 路线 C：长期配置

把验证通过的免费模型放进：

- Hermes 的常备模型池
- OpenClaw 里少数真正适合低成本运行的链路

而不是一次性把所有模块都切过去。

---

## 最后的判断

如果只用一句话概括这篇文章，我会这样说：

> **Hermes 配 OpenRouter 免费模型，主要是产品级配置问题；OpenClaw 配 OpenRouter 免费模型，主要是工程级架构问题。**

这两者看起来都叫“接模型”，但复杂度根本不是一个量级。

因此最实用的策略是：

1. 先在 Hermes 里把免费模型跑通、跑明白
2. 再把真正合适的模型接进 OpenClaw 的具体业务链路
3. 对 OpenClaw，优先改 `targets`，不要只盯着 `openclaw-agents`

这样你会少走很多弯路。

---

## 快速参考

| 问题 | 我的建议 |
| --- | --- |
| 想最快用上 OpenRouter 免费模型 | 先用 Hermes |
| 想在 Hermes 里长期保留免费模型入口 | 用 `model_aliases` |
| 想在 OpenClaw 里切到 OpenRouter | 先确认该模块是否支持 OpenAI-compatible |
| OpenClaw 应优先改哪类配置 | 优先看 `ai-settings/targets` |
| `openclaw-agents` 适合干什么 | 更适合改 OpenClaw provider 内部 agent 名称 |
| 要不要把所有 OpenClaw 模块都切到免费模型 | 不建议，先按链路分层验证 |

## 信息来源说明

本文基于当前可核对的本地工程实现与配置文档整理，重点包括：

- Hermes 文档与配置能力（`OPENROUTER_API_KEY`、`hermes model`、`model_aliases`）
- OpenClaw / research 项目中的 AI target 与 provider 定义
- `server/src/modules/ai-settings/ai-settings.types.ts`
- `server/src/modules/ai-settings/ai-settings.controller.ts`
- `server/src/modules/ai-runtime/providers/openai-compatible.provider.ts`

因此，本文更适合作为 **当前工程现实下的配置指南与架构判断**，而不是脱离上下文的通用产品宣传文案。
