# Hermes 命令速查

这页用于快速查找最常用的 Hermes CLI 命令，适合“我只记得大概功能，不想翻完整文档”的场景。

!!! abstract "使用建议"
    如果你已经知道要做什么，但忘了具体命令，可以先看这页；如果要看更完整的解释，再跳到对应专题页。

## 一页速览

| 场景 | 最常用命令 |
|---|---|
| 看整体状态 | `hermes status --all` |
| 跑健康检查 | `hermes doctor` |
| 选择模型 / provider | `hermes model` |
| 登录 provider | `hermes login --provider nous` |
| 查看凭证池 | `hermes auth list` |
| 查看配置 | `hermes config show` |
| 设置单个配置项 | `hermes config set <key> <value>` |
| 配置消息平台 | `hermes gateway setup` |
| 重启网关 | `hermes gateway restart` |
| 查看工具 | `hermes tools --summary` |
| 查看 MCP | `hermes mcp list` |
| 创建测试 profile | `hermes profile create test --clone` |
| 看日志 | `hermes logs errors -n 100` |
| 看会话 | `hermes sessions list` |

## 1. 状态与健康检查

```bash
hermes status --all
hermes status --deep
hermes doctor
hermes doctor --fix
```

适合：

- 不确定 Hermes 现在是否正常
- 想看 provider、gateway、平台接入状态
- 想让 Hermes 自动尝试修一些常见问题

## 2. 模型 / Provider / 凭证

```bash
hermes model
hermes login --provider nous
hermes login --provider openai-codex
hermes auth list
hermes auth add <provider>
hermes auth remove <provider> <index_or_id_or_label>
hermes auth reset <provider>
```

适合：

- 切换默认模型
- 给 provider 登录
- 管理 pooled credentials

参见：[Provider / 凭证配置](providers-and-credentials.md)

## 3. 配置文件管理

```bash
hermes config show
hermes config edit
hermes config set <key> <value>
hermes config path
hermes config env-path
hermes config check
hermes config migrate
```

常见示例：

```bash
hermes config set agent.reasoning_effort minimal
hermes config set display.tool_progress off
hermes config set compression.threshold 0.6
```

参见：[提速配置](performance.md)、[配置文件与维护](config-files-and-maintenance.md)

## 4. Gateway 与平台接入

```bash
hermes gateway setup
hermes gateway run
hermes gateway status
hermes gateway restart
hermes pairing list
hermes pairing approve <code>
hermes webhook list
hermes webhook test <name>
```

适合：

- 接入消息平台
- 重启 gateway
- 处理 pairing / webhook 问题

参见：[Gateway 配置](gateway.md)、[平台接入与消息入口](platform-integrations.md)

## 5. Tools / MCP

```bash
hermes tools --summary
hermes tools list --platform cli
hermes tools enable <tool_or_toolset>
hermes tools disable <tool_or_toolset>
hermes mcp list
hermes mcp add <name> ...
hermes mcp test <name>
hermes mcp configure
```

适合：

- 看某个平台能用哪些工具
- 接入新的 MCP server
- 测试 MCP server 是否可用

参见：[Tools 与 MCP 配置](tools-and-mcp.md)

## 6. Profiles / 多实例

```bash
hermes profile list
hermes profile create test --clone
hermes profile use test
hermes profile show test
hermes profile export test
hermes profile import <archive>
```

适合：

- 创建测试实例
- 切换默认 profile
- 导出 / 导入多实例配置

参见：[Profiles / 多实例管理](profiles.md)

## 7. 日志与会话

```bash
hermes logs
hermes logs errors -n 100
hermes logs gateway -n 100
hermes logs --since 1h
hermes logs -f
hermes sessions list
hermes sessions stats
hermes sessions browse
```

适合：

- 查 agent 报错
- 查 gateway 最近日志
- 看最近会话与历史记录

参见：[常见故障排查](troubleshooting.md)

## 8. 推荐的最小排查组合

### 配置没生效

```bash
hermes config show
hermes config path
hermes doctor
hermes gateway restart
```

### 平台不回消息

```bash
hermes status --all
hermes gateway status
hermes logs gateway -n 100
```

### provider 不可用

```bash
hermes model
hermes login --help
hermes auth list
hermes status --all
```

### MCP 工具不生效

```bash
hermes mcp list
hermes mcp test <name>
hermes tools list --platform cli
hermes logs --component tools
```
