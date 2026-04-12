# Hermes 配置总览

这个文档作为 Hermes 配置的总入口，用来汇总常见配置主题，并把内容拆分成更易维护的结构化页面。

!!! abstract "阅读地图"
    按主题查看：

    - [提速配置](hermes/performance.md)
    - [Provider / 凭证配置](hermes/providers-and-credentials.md)
    - [Gateway 配置](hermes/gateway.md)
    - [配置文件与维护](hermes/config-files-and-maintenance.md)

## 结构说明

为了避免把所有内容都堆在一个长页面里，Hermes 文档现在按主题拆成四类：

| 模块 | 适合什么时候看 | 页面 |
|---|---|---|
| 提速配置 | 感觉 Hermes 回复慢、长会话变卡 | [提速配置](hermes/performance.md) |
| Provider / 凭证配置 | 切换模型提供方、登录、排查 token / credential | [Provider / 凭证配置](hermes/providers-and-credentials.md) |
| Gateway 配置 | 对接 Feishu / Telegram / Discord 等消息网关 | [Gateway 配置](hermes/gateway.md) |
| 配置文件与维护 | 找配置文件、检查配置、迁移配置 | [配置文件与维护](hermes/config-files-and-maintenance.md) |

## 快速开始

如果你只是想快速排查，建议按这个顺序：

1. 速度问题：先看 [提速配置](hermes/performance.md)
2. 模型或 provider 问题：看 [Provider / 凭证配置](hermes/providers-and-credentials.md)
3. 消息平台接入问题：看 [Gateway 配置](hermes/gateway.md)
4. 配置文件位置或升级兼容问题：看 [配置文件与维护](hermes/config-files-and-maintenance.md)

## 后续扩展建议

后续如果 Hermes 文档继续增加，可以继续按下面方向补充：

- 平台接入实战（例如 Feishu / Telegram / Discord 分页）
- MCP / tools 配置
- profiles / multi-instance 管理
- 常见故障排查
