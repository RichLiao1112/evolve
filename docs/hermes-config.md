# Hermes 配置总览

这个文档作为 Hermes 配置的总入口，用来汇总常见配置主题，并把内容拆分成更易维护的结构化页面。

!!! abstract "阅读地图"
    按主题查看：

    - [命令速查](hermes/command-cheatsheet.md)
    - [提速配置](hermes/performance.md)
    - [Provider / 凭证配置](hermes/providers-and-credentials.md)
    - [Gateway 配置](hermes/gateway.md)
    - [配置文件与维护](hermes/config-files-and-maintenance.md)
    - [平台接入与消息入口](hermes/platform-integrations.md)
    - [Tools 与 MCP 配置](hermes/tools-and-mcp.md)
    - [Profiles / 多实例管理](hermes/profiles.md)
    - [常见故障排查](hermes/troubleshooting.md)

<div class="sponsor-block sponsor-block--article sponsor-block--muted">
  <div class="sponsor-block__eyebrow">Article Sponsor Slot</div>
  <h3>文章页通用赞助位 · 适合与正文主题强相关的工具或服务</h3>
  <p>这是通用文章页版赞助位示例，适合插在正文开头之后，用于展示与当前主题高度相关的产品、API、服务或长期合作信息。</p>
  <div class="sponsor-block__chips">
    <span>文章页版</span>
    <span>通用复用</span>
    <span>主题相关优先</span>
  </div>
  <div class="sponsor-block__actions">
    <a href="site-info/contact/">联系合作</a>
    <a href="site-info/disclaimer/">查看披露说明</a>
  </div>
</div>

## 结构说明

为了避免把所有内容都堆在一个长页面里，Hermes 文档现在按主题拆成四类：

| 模块 | 适合什么时候看 | 页面 |
|---|---|---|
| 命令速查 | 想快速找命令、不想翻长文 | [命令速查](hermes/command-cheatsheet.md) |
| 提速配置 | 感觉 Hermes 回复慢、长会话变卡 | [提速配置](hermes/performance.md) |
| Provider / 凭证配置 | 切换模型提供方、登录、排查 token / credential | [Provider / 凭证配置](hermes/providers-and-credentials.md) |
| Gateway 配置 | 管理 gateway 的运行、重启与平台配置入口 | [Gateway 配置](hermes/gateway.md) |
| 配置文件与维护 | 找配置文件、检查配置、迁移配置 | [配置文件与维护](hermes/config-files-and-maintenance.md) |
| 平台接入与消息入口 | 处理 Feishu / Telegram / Discord / Weixin 等平台接入 | [平台接入与消息入口](hermes/platform-integrations.md) |
| Tools 与 MCP 配置 | 管理工具开关与外部 MCP server | [Tools 与 MCP 配置](hermes/tools-and-mcp.md) |
| Profiles / 多实例管理 | 隔离不同 Hermes 实例与配置 | [Profiles / 多实例管理](hermes/profiles.md) |
| 常见故障排查 | 快速排查状态、日志、doctor 与会话问题 | [常见故障排查](hermes/troubleshooting.md) |

## 快速开始

如果你只是想快速排查，建议按这个顺序：

1. 先想快速找命令：看 [命令速查](hermes/command-cheatsheet.md)
2. 速度问题：再看 [提速配置](hermes/performance.md)
3. 模型或 provider 问题：看 [Provider / 凭证配置](hermes/providers-and-credentials.md)
4. 消息平台接入问题：先看 [平台接入与消息入口](hermes/platform-integrations.md)，再看 [Gateway 配置](hermes/gateway.md)
5. 工具或 MCP 问题：看 [Tools 与 MCP 配置](hermes/tools-and-mcp.md)
6. 多实例隔离需求：看 [Profiles / 多实例管理](hermes/profiles.md)
7. 配置文件位置或升级兼容问题：看 [配置文件与维护](hermes/config-files-and-maintenance.md)
8. 不确定问题在哪：直接看 [常见故障排查](hermes/troubleshooting.md)

## 结构补充说明

现在 Hermes 文档已经从“单页记录”扩展成更完整的主题结构，后续更适合继续按专题增量维护，而不是把所有内容继续堆在一个页面里。
