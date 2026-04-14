# OpenClaw 智能体模型配置：最短改法

## 先给结论

如果你这里要放的是 **OpenClaw 这个智能体本身的模型配置**，那应优先看：

```text
GET /ai-settings/openclaw-agents
PATCH /ai-settings/openclaw-agents
```

而不是先看 `targets`。

---

## 读取当前配置

接口：

```text
GET /ai-settings/openclaw-agents
```

会返回这些 OpenClaw 智能体位：

- `xReportDocs`
- `xReportRednote`
- `xHomeDigest`
- `xueqiuReviewAnalysis`

这些字段对应的就是 OpenClaw 智能体模型名。

---

## 修改 OpenClaw 智能体模型

接口：

```text
PATCH /ai-settings/openclaw-agents
```

请求体示例：

```json
{
  "xReportDocs": "openclaw:docs",
  "xReportRednote": "openclaw:docs",
  "xHomeDigest": "openclaw:docs",
  "xueqiuReviewAnalysis": "openclaw:docs"
}
```

如果你只改一个，就只传一个字段：

```json
{
  "xHomeDigest": "openclaw:docs"
}
```

---

## 环境变量兜底

如果数据库里没有持久化配置，会按环境变量 / 默认值回退。

相关环境变量包括：

```bash
OPENCLAW_DOCS_MODEL=openclaw:docs
OPENCLAW_RENOTE_MODEL=openclaw:docs
OPENCLAW_REVIEW_ANALYSIS_MODEL=openclaw:docs
X_HOME_DIGEST_AI_MODEL=openclaw:docs
```

当前代码里的优先级是：

- **DB 持久化配置**
- **环境变量**
- **默认值**

---

## `targets` 是干什么的

```text
PATCH /ai-settings/targets
```

这个接口更偏 **AI 路由配置**，可同时改：

- `provider`
- `model`
- `timeoutMs`
- `temperature`

所以：

- **如果你要改 OpenClaw 智能体模型名，用 `openclaw-agents`**
- **如果你要改整条 AI 调用链路的 provider/model，用 `targets`**

---

## 最短判断

- **改 OpenClaw 智能体模型名** → `PATCH /ai-settings/openclaw-agents`
- **改 AI 路由 / provider** → `PATCH /ai-settings/targets`
- **只看当前值** → `GET /ai-settings/openclaw-agents`

## 信息来源说明

本文基于当前可核对的本地工程实现整理，重点参考：

- `server/src/modules/ai-settings/ai-settings.types.ts`
- `server/src/modules/ai-settings/ai-settings.controller.ts`
- `server/src/modules/ai-settings/dto/openclaw-agents.dto.ts`
- `server/src/modules/ai-settings/ai-settings.service.ts`
