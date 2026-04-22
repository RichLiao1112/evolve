# 拯救你的便宜 AI 模型

> 当你使用自建或第三方的低价/免费模型时，常会碰到 **返回内容混杂 markdown、reasoning，甚至是 HTML**，导致下游工具（如 Hermes、脚本、CI/CD）无法直接解析 JSON。
> 本文演示如何 **通过 Cloudflare Workers** 为任意模型 **构建一个纯 JSON‑only 代理**，并在 Hermes 中实现“一键调用”。

---

## 目录

1. [痛点回顾](#痛点回顾)
2. [解决思路](#解决思路)
3. [一步步实现](#一步步实现)
   - 3.1 初始化 Worker 项目
   - 3.2 编写转发逻辑（核心代码）
   - 3.3 添加 Cloudflare Secrets
   - 3.4 部署 & 验证
4. [在 Hermes 中使用](#在-hermes-中使用)
5. [安全访问控制（自定义 token）](#安全访问控制自定义-token)
6. [常见问题 & FAQ](#常见问题--faq)
7. [完整代码（供参考）](#完整代码一览)

---

## 痛点回顾

- **模型返回混合格式**
  - `content: null` + `reasoning` 字段
  - 结果被包在 ```markdown``` 或 HTML 页面中
- **调用方只能得到 `malformed_json`**，导致后续流程中断。
- **自行前端解析** 往往不可靠且难以维护。

> 以 **XF‑Coding**（`astron-code-latest`） 为例，直接请求 `https://maas-coding-api.cn-huabei-1.xf-yun.com/v2/chat/completions` 时，模型会把实际答案放在 `reasoning_content`，而 `content` 为 `null`。

---

## 解决思路

1. **在 Cloudflare Workers 中间层**，统一把所有请求转发至目标模型的真实 API。
2. **强制注入 `response_format`**（OpenAI‑compatible JSON schema），让支持的模型直接返回合法 JSON。
3. **若模型仍返回文字**，Worker 会 **从 `reasoning_content` 正则抽取期望字段**（如 ISO 时间），重新构造干净的 JSON。
4. **凭证** 使用 **Cloudflare Secrets**，安全且不泄露在代码中。
5. **错误报警**（可选） → 通过钉钉/飞书 webhook 实时通知。

这样，调用方（Hermes、脚本等）只需 **向 Worker 发一次请求**，即可得到 **纯 JSON**，根本上解决 “格式不符” 的问题。

---

## 一步步实现

### 3.1 初始化 Worker 项目
```bash
mkdir -p ~/cloudflare-workers && cd ~/cloudflare-workers
npx wrangler init --site false   # 生成最小化 Worker 项目
```
`wrangler.toml` 会自动生成，确保其中有 `main = "src/index.js"`。

### 3.2 编写转发逻辑（核心代码）
> **文件**：`src/index.js`
```javascript
export default {
  async fetch(request, env) {
    // -------------------------------------------------
    // 0️⃣ 访问凭证校验（自定义 token）
    // -------------------------------------------------
    const authHeader = request.headers.get("Authorization");
    if (!authHeader || authHeader !== `Bearer ${env.MY_PUBLIC_TOKEN}`) {
      return new Response(
        JSON.stringify({ error: "unauthorized", detail: "Invalid or missing token" }),
        { status: 401, headers: { "Content-Type": "application/json" } }
      );
    }

    // -------------------------------------------------
    // 1️⃣ 读取原始请求体（保持 JSON，后面会注入 response_format）
    // -------------------------------------------------
    const rawBody = await request.clone().text();
    console.log("[INFO] Received request", {
      method: request.method,
      url: request.url,
      bodyPreview: rawBody.slice(0, 200), // 防止日志太长
    });

    // -------------------------------------------------
    // 2️⃣ 基础 Provider 主机（只保留协议+主机，不要路径）
    // -------------------------------------------------
    const BASE_PROVIDER_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/v2";

    // -------------------------------------------------
    // 3️⃣ 拼接完整上游 URL（固定路径 /chat/completions，保留查询字符串）
    // -------------------------------------------------
    const incoming = new URL(request.url); // 客户端请求的 URL（仅用于取查询参数）
    const upstreamUrl = `${BASE_PROVIDER_URL}/chat/completions${incoming.search}`;
    console.log("[INFO] Forwarding to Provider endpoint", { upstreamUrl, method: request.method });

    // -------------------------------------------------
    // 4️⃣ 在请求体里强制要求 JSON‑only（response_format）
    // -------------------------------------------------
    let bodyObj;
    try { bodyObj = JSON.parse(rawBody); }
    catch (e) {
      return new Response(
        JSON.stringify({ error: "invalid_request_json", detail: e.message }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }
    bodyObj.response_format = {
      type: "json_schema",
      json_schema: { name: "any_object", schema: { type: "object", additionalProperties: true } },
    };

    // -------------------------------------------------
    // 5️⃣ 构造转发请求（使用 Secret 中的 API Key）
    // -------------------------------------------------
    const outgoingHeaders = new Headers(request.headers);
    outgoingHeaders.delete("Authorization");               // 移除可能的占位 token
    outgoingHeaders.set("Accept", "application/json"); // 明确要 JSON
    outgoingHeaders.set("Accept-Encoding", "identity"); // 禁用压缩
    outgoingHeaders.set("Authorization", `Bearer ${env.XF_CODING_KEY}`);
    console.log("[INFO] Using XF Coding key length", (env.XF_CODING_KEY?.length ?? 0));

    const upstreamRequest = new Request(upstreamUrl, {
      method: request.method,
      headers: outgoingHeaders,
      body: JSON.stringify(bodyObj),
    });

    // -------------------------------------------------
    // 6️⃣ 调用模型（XF‑Coding）
    // -------------------------------------------------
    let upstreamResp;
    let rawResp = "";
    try {
      upstreamResp = await fetch(upstreamRequest);
      rawResp = await upstreamResp.text();
    } catch (e) {
      console.error("[ERROR] Upstream fetch failed", e);
      if (env.FEISHU_WEBHOOK) {
        await fetch(env.FEISHU_WEBHOOK, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title: "Format‑Validator Upstream 错误", text: `Fetch 失败：${e.message || e}\nURL: ${upstreamUrl}` }),
        });
      }
      return new Response(JSON.stringify({ error: "upstream_fetch_failed", detail: e.message || String(e) }), { status: 502, headers: { "Content-Type": "application/json" } });
    }
    console.log("[INFO] Upstream response", { status: upstreamResp.status, snippet: rawResp.slice(0, 200) });

    // -------------------------------------------------
    // 7️⃣ 解析为干净 JSON
    // -------------------------------------------------
    let parsed = null;
    try { parsed = JSON.parse(rawResp); }
    catch (_) {
      const m = rawResp.match(/({[\s\S]*?})|(\[[\s\S]*?\])/);
      if (m) { try { parsed = JSON.parse(m[0]); } catch (_) {} }
    }

    // -------------------------------------------------
    // 8️⃣ fallback：从 reasoning_content 抽取 ISO 时间（若模型未返回 JSON）
    // -------------------------------------------------
    if (!parsed) {
      const reasonMatch = rawResp.match(/"reasoning_content":"([^\"]+)"/);
      if (reasonMatch) {
        const isoMatch = reasonMatch[1].match(/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z/);
        if (isoMatch) {
          const result = { utc_time: isoMatch[0] };
          return new Response(JSON.stringify(result), { status: 200, headers: { "Content-Type": "application/json" } });
        }
      }
    }

    // -------------------------------------------------
    // 9️⃣ 错误处理 & 报警（仍未解析为 JSON）
    // -------------------------------------------------
    if (!parsed) {
      if (env.FEISHU_WEBHOOK) {
        await fetch(env.FEISHU_WEBHOOK, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ title: "Format‑Validator JSON 解析错误", text: `上游返回（状态 ${upstreamResp.status}）无法解析为 JSON：\n\`\`\`\n${rawResp}\n\`\`\`` }),
        });
      }
      return new Response(JSON.stringify({ error: "malformed_json", original: rawResp, upstream_status: upstreamResp.status }), { status: 400, headers: { "Content-Type": "application/json" } });
    }

    // -------------------------------------------------
    // 🔟 成功返回干净 JSON
    // -------------------------------------------------
    return new Response(JSON.stringify(parsed), { status: upstreamResp.status, headers: { "Content-Type": "application/json" } });
  },
};
```

### 3.3 添加 Cloudflare Secrets
```bash
cd ~/cloudflare-workers
# 保存模型 API Key（在 XF‑Coding 控制台生成，确保具备 Chat 权限）
npx wrangler secret put XF_CODING_KEY
# 保存自定义访问 token（任意随机字符串）
npx wrangler secret put MY_PUBLIC_TOKEN
# 可选：飞书报警 webhook
npx wrangler secret put FEISHU_WEBHOOK
```
> **如果已有旧 Secret**，可以先 `npx wrangler secret delete <NAME>` 再重新写入。

### 3.4 部署 & 验证
```bash
cd ~/cloudflare-workers
npx wrangler deploy
```
部署成功后会显示类似：
```
https://format-validator.liaoxinyu1.workers.dev
Current Version ID: <uuid>
```

#### 手动 `curl` 验证
```bash
SERVICE="https://format-validator.liaoxinyu1.workers.dev"
curl -X POST "$SERVICE/v1/chat/completions" \
  -H "Authorization: Bearer <YOUR_PUBLIC_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
        "model":"astron-code-latest",
        "messages":[
          {"role":"system","content":"You must output ONLY valid JSON."},
          {"role":"user","content":"返回当前 UTC 时间的 ISO 格式。"}
        ],
        "max_tokens":30
      }'
```
**预期返回**（示例）：
```json
{ "utc_time": "2026-04-22T09:12:45Z" }
```
如果出现 `401 Unauthorized`，说明 token 未匹配，请检查 `MY_PUBLIC_TOKEN` 与请求头中的值是否一致。

---

## 在 Hermes 中使用
在本地的 **Hermes 配置文件**（`~/.hermes/config.yaml`）加入：
```yaml
xf-coding-plan:
  base_url: https://format-validator.liaoxinyu1.workers.dev   # 指向刚部署的 Worker
  api_key: placeholder    # 任意占位，Worker 已使用 Secret
  model: astron-code-latest
```
随后在 Herm​es 对话里直接发送：
```
/chat model:xf-coding-plan
{
  "model":"astron-code-latest",
  "messages":[
    {"role":"system","content":"You must output ONLY valid JSON."},
    {"role":"user","content":"返回当前 UTC 时间的 ISO 格式。"}
  ],
  "max_tokens":30
}
```
Hermes 会自动把请求路由到 Worker，得到 **干净的 JSON**，无需再手动清理。

---

## 安全访问控制（自定义 token）

### 为什么需要 token？
- **防止滥用**：Worker 公开在互联网，任何人都可以调用。如果不限制，可能会耗尽你的 XF‑Coding 配额或产生费用。
- **简单授权**：相比 OAuth、JWT，单纯的 **Bearer token** 实现最轻量，易于在脚本、Hermes、CI 中使用。

### 配置步骤
1. **在 Cloudflare Secrets 中写入 token**（上文已演示 `MY_PUBLIC_TOKEN`）。
2. **代码中会自动校验**：每次请求必须在 `Authorization` Header 中携带 `Bearer <token>`。
3. **调用方式**（示例）：
   ```bash
   curl -X POST https://format-validator.liaoxinyu1.workers.dev/v1/chat/completions \
        -H "Authorization: Bearer <YOUR_PUBLIC_TOKEN>" \
        -H "Content-Type: application/json" \
        -d '{...}'
   ```
4. **修改或撤销 token**：直接在 Cloudflare Dashboard 或使用 `npx wrangler secret put MY_PUBLIC_TOKEN` 覆盖即可，旧 token 立刻失效。

### 进阶安全（可选）
- **Rate Limiting**：在 Cloudflare Dashboard 为此 Worker 设置每分钟请求上限，防止暴力调用。
- **日志监控**：通过 `wrangler tail` 实时查看 `Using XF Coding key length` 与 `Upstream response` 日志，快速发现异常。
- **Webhook 报警**：如配置 `FEISHU_WEBHOOK`，当上游返回非 JSON 时会自动推送到钉钉/飞书，便于及时追踪。

---

## 常见问题 & FAQ
| 问题 | 解决办法 |
|------|----------|
| **返回 HTML 页面** | 检查 `upstreamUrl` 是否正确拼接为 `/chat/completions`。重新部署确保代码已更新。 |
| **401/403 Unauthorized** | 确认 `XF_CODING_KEY` 与 `MY_PUBLIC_TOKEN` 已正确写入 Cloudflare Secrets，且 token 与请求头匹配。 |
| **仍得到 `content: null`** | 模型可能不支持 `response_format`；Worker 会尝试从 `reasoning_content` 抽取时间。请在系统提示中更明确要求 `{"utc_time":"<ISO>"}`。 |
| **如何查看日志** | Dashboard → Workers → Logs，或 `npx wrangler tail` 实时追踪。 |
| **想限制访问** | 使用上述 token 方案，或在 Cloudflare Dashboard 添加 Rate Limiting。 |

---

## 完整代码一览（供参考）
> 文件路径：`~/cloudflare-workers/src/index.js`
```javascript
export default {
  async fetch(request, env) {
    // -------------------------------------------------
    // 0️⃣ 访问凭证校验（自定义 token）
    // -------------------------------------------------
    const authHeader = request.headers.get("Authorization");
    if (!authHeader || authHeader !== `Bearer ${env.MY_PUBLIC_TOKEN}`) {
      return new Response(
        JSON.stringify({ error: "unauthorized", detail: "Invalid or missing token" }),
        { status: 401, headers: { "Content-Type": "application/json" } }
      );
    }

    // -------------------------------------------------
    // 1️⃣ 读取原始请求体（保持 JSON，后面会注入 response_format）
    // -------------------------------------------------
    const rawBody = await request.clone().text();
    console.log("[INFO] Received request", { method: request.method, url: request.url, bodyPreview: rawBody.slice(0, 200) });

    // -------------------------------------------------
    // 2️⃣ 基础 Provider 主机（只保留协议+主机，不要路径）
    // -------------------------------------------------
    const BASE_PROVIDER_URL = "https://maas-coding-api.cn-huabei-1.xf-yun.com/v2";

    // -------------------------------------------------
    // 3️⃣ 拼接完整上游 URL（固定路径 /chat/completions，保留查询字符串）
    // -------------------------------------------------
    const incoming = new URL(request.url);
    const upstreamUrl = `${BASE_PROVIDER_URL}/chat/completions${incoming.search}`;
    console.log("[INFO] Forwarding to Provider endpoint", { upstreamUrl, method: request.method });

    // -------------------------------------------------
    // 4️⃣ 在请求体里强制要求 JSON‑only（response_format）
    // -------------------------------------------------
    let bodyObj;
    try { bodyObj = JSON.parse(rawBody); }
    catch (e) { return new Response(JSON.stringify({ error: "invalid_request_json", detail: e.message }), { status: 400, headers: { "Content-Type": "application/json" } }); }
    bodyObj.response_format = { type: "json_schema", json_schema: { name: "any_object", schema: { type: "object", additionalProperties: true } } };

    // -------------------------------------------------
    // 5️⃣ 构造转发请求（使用 Secret 中的 API Key）
    // -------------------------------------------------
    const outgoingHeaders = new Headers(request.headers);
    outgoingHeaders.delete("Authorization");
    outgoingHeaders.set("Accept", "application/json");
    outgoingHeaders.set("Accept-Encoding", "identity");
    outgoingHeaders.set("Authorization", `Bearer ${env.XF_CODING_KEY}`);
    console.log("[INFO] Using XF Coding key length", (env.XF_CODING_KEY?.length ?? 0));

    const upstreamRequest = new Request(upstreamUrl, { method: request.method, headers: outgoingHeaders, body: JSON.stringify(bodyObj) });

    // -------------------------------------------------
    // 6️⃣ 调用模型（XF‑Coding）
    // -------------------------------------------------
    let upstreamResp; let rawResp = "";
    try { upstreamResp = await fetch(upstreamRequest); rawResp = await upstreamResp.text(); }
    catch (e) {
      console.error("[ERROR] Upstream fetch failed", e);
      if (env.FEISHU_WEBHOOK) {
        await fetch(env.FEISHU_WEBHOOK, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title: "Format‑Validator Upstream 错误", text: `Fetch 失败：${e.message || e}\nURL: ${upstreamUrl}` }) });
      }
      return new Response(JSON.stringify({ error: "upstream_fetch_failed", detail: e.message || String(e) }), { status: 502, headers: { "Content-Type": "application/json" } });
    }
    console.log("[INFO] Upstream response", { status: upstreamResp.status, snippet: rawResp.slice(0, 200) });

    // -------------------------------------------------
    // 7️⃣ 解析为干净 JSON
    // -------------------------------------------------
    let parsed = null;
    try { parsed = JSON.parse(rawResp); }
    catch (_) { const m = rawResp.match(/({[\s\S]*?})|(\[[\s\S]*?\])/); if (m) { try { parsed = JSON.parse(m[0]); } catch (_) {} } }

    // -------------------------------------------------
    // 8️⃣ fallback：从 reasoning_content 抽取 ISO 时间（若模型未返回 JSON）
    // -------------------------------------------------
    if (!parsed) {
      const reasonMatch = rawResp.match(/"reasoning_content":"([^\"]+)"/);
      if (reasonMatch) { const isoMatch = reasonMatch[1].match(/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z/); if (isoMatch) { const result = { utc_time: isoMatch[0] }; return new Response(JSON.stringify(result), { status: 200, headers: { "Content-Type": "application/json" } }); } }
    }

    // -------------------------------------------------
    // 9️⃣ 错误处理 & 报警（仍未解析为 JSON）
    // -------------------------------------------------
    if (!parsed) {
      if (env.FEISHU_WEBHOOK) {
        await fetch(env.FEISHU_WEBHOOK, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title: "Format‑Validator JSON 解析错误", text: `上游返回（状态 ${upstreamResp.status}）无法解析为 JSON：\n\`\`\`\n${rawResp}\n\`\`\`` }) });
      }
      return new Response(JSON.stringify({ error: "malformed_json", original: rawResp, upstream_status: upstreamResp.status }), { status: 400, headers: { "Content-Type": "application/json" } });
    }

    // -------------------------------------------------
    // 🔟 成功返回干净 JSON
    // -------------------------------------------------
    return new Response(JSON.stringify(parsed), { status: upstreamResp.status, headers: { "Content-Type": "application/json" } });
  },
};
```
---

**祝你在使用低价模型时不再被格式问题困扰，安全、干净、快速地集成到 Hermes 与任何脚本中 🚀✨**