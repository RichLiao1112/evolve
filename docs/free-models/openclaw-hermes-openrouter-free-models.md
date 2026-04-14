# OpenClaw 和 Hermes 接 OpenRouter 免费模型：最短配置法

## 先给结论

- **想最快跑起来：用 Hermes**
- **想接到 OpenClaw 链路：优先改 `targets`，不要只改 `openclaw-agents`**

---

## Hermes：最短配置

### 方式 1：直接交互式配置

```bash
hermes config set OPENROUTER_API_KEY sk-or-...
hermes model
```

然后在模型选择里：

- provider 选 `openrouter`
- model 选目标免费模型

### 方式 2：手动写 alias

编辑 `~/.hermes/config.yaml`：

```yaml
model_aliases:
  or-free:
    model: openrouter/elephant-alpha
    provider: openrouter
```

之后可直接切换：

```bash
/model or-free
```

### 配完后检查

```bash
hermes status
hermes doctor
```

---

## OpenClaw：最短配置思路

### 1. 优先改 `targets`

接口：

```text
PATCH /ai-settings/targets
```

思路：
- `provider` 设成 `openai`
- `model` 写 OpenRouter 模型 slug
- `base_url` 指向 `https://openrouter.ai/api/v1`
- `api_key` 用 OpenRouter key

示例请求体：

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

### 2. 配环境变量

```bash
X_HOME_DIGEST_AI_PROVIDER=openai
X_HOME_DIGEST_AI_MODEL=openrouter/elephant-alpha
X_HOME_DIGEST_OPENAI_BASE_URL=https://openrouter.ai/api/v1
X_HOME_DIGEST_OPENAI_API_KEY=sk-or-...
```

### 3. 不要只改 `openclaw-agents`

接口：

```text
PATCH /ai-settings/openclaw-agents
```

这个更适合改 OpenClaw 内部 agent 名称，例如：

```text
openclaw:docs
```

**它不等于已经把调用链路切成 OpenRouter。**

---

## 最短判断

- **只想快速用免费模型：Hermes**
- **想接业务链路：OpenClaw 改 `targets`**
- **只改 `openclaw-agents`：通常不够**

## 信息来源说明

本文基于当前可核对的本地工程实现整理，重点参考：

- `server/src/modules/ai-settings/ai-settings.types.ts`
- `server/src/modules/ai-settings/ai-settings.controller.ts`
- `server/src/modules/ai-runtime/providers/openai-compatible.provider.ts`
