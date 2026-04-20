# Hermes Tools 与 MCP 配置

这页聚焦 Hermes 的工具开关、平台级工具配置，以及 MCP（Model Context Protocol）服务器接入。

## 1. Tools 配置能做什么

`hermes tools` 用于按平台管理可用工具。

查看帮助：

```bash
hermes tools --help
```

CLI 帮助中可见的能力包括：

- `list`
- `enable`
- `disable`
- 无子命令时进入交互式配置 UI

## 2. 查看某个平台启用了哪些工具

```bash
hermes tools list --platform cli
```

也可以换成其他平台名查看。

如果只想快速看概要：

```bash
hermes tools --summary
```

## 3. 启用或禁用工具

```bash
hermes tools enable <tool_or_toolset>
hermes tools disable <tool_or_toolset>
```

CLI 帮助里的说明有两个关键点：

| 类型 | 示例 |
|---|---|
| 内建 toolset | `web`、`memory` |
| MCP 工具 | `github:create_issue` 这类 `server:tool` 形式 |

这意味着 Hermes 的工具来源可以分成两层：

| 层级 | 说明 |
|---|---|
| 内建工具 | Hermes 自带的通用工具集 |
| MCP 工具 | 来自外部 MCP server 的扩展工具 |

## 4. MCP 能做什么

`hermes mcp` 用于管理 MCP server 连接，也可以把 Hermes 自己暴露成 MCP server。

查看帮助：

```bash
hermes mcp --help
```

当前可见的子命令包括：

- `serve`
- `add`
- `remove`
- `list`
- `test`
- `configure`

## 5. 添加 MCP Server

```bash
hermes mcp add <name>
```

根据帮助，添加时支持这些常见方式：

| 参数 | 用途 |
|---|---|
| `--url` | 接 HTTP / SSE 类型 MCP 服务 |
| `--command` | 通过 stdio 命令接入 |
| `--args` | 给 stdio 命令传参数 |
| `--auth oauth` / `--auth header` | 指定认证方式 |
| `--preset` | 使用预设 |
| `--env KEY=VALUE` | 给 stdio server 注入环境变量 |

## 6. 测试 MCP Server 连通性

```bash
hermes mcp test <name>
```

接入完新 MCP server 后，建议第一时间测试，避免只是“配置写进去了”，但实际并不可用。

## 7. 查看与调整 MCP 配置

```bash
hermes mcp list
hermes mcp configure
```

建议理解为：

| 命令 | 作用 |
|---|---|
| `hermes mcp list` | 看当前有哪些 MCP server 已配置 |
| `hermes mcp configure` | 调整工具选择或配置细节 |
| `hermes mcp remove <name>` | 删除不再使用的 MCP server |

## 8. 一个推荐操作流

如果你要新增一个外部 MCP 工具源，建议按这个顺序：

1. `hermes mcp add <name> ...`
2. `hermes mcp test <name>`
3. `hermes mcp list`
4. `hermes tools list --platform cli`
5. 必要时再 `hermes tools enable ...`

## 9. 最小命令清单

```bash
hermes tools --summary
hermes tools list --platform cli
hermes mcp list
hermes mcp add <name> ...
hermes mcp test <name>
hermes mcp configure
```
