# Hermes 常见故障排查

这页聚焦 Hermes 的通用排查命令，适合用于“为什么不能用”“为什么平台不回”“为什么配置没生效”这类问题。

!!! abstract "最小排查四件套"
    大多数问题可以先从下面四个命令开始：

    ```bash
    hermes status --all
    hermes doctor
    hermes logs errors -n 100
    hermes logs gateway -n 100
    ```

## 1. 看整体状态

```bash
hermes status --all
```

如果想做更深入检查：

```bash
hermes status --deep
```

适合回答这些问题：

- provider 是否已登录
- API key 是否存在
- gateway 是否运行
- 哪些消息平台已配置

## 2. 跑健康检查

```bash
hermes doctor
```

如果想让 Hermes 尝试自动修复：

```bash
hermes doctor --fix
```

适合在以下场景优先执行：

- 初次安装后发现不工作
- 升级后出现异常
- 配置改动较多，不确定问题在哪

## 3. 查日志

```bash
hermes logs --help
```

根据 CLI 帮助，常见查看方式包括：

```bash
hermes logs
hermes logs errors
hermes logs gateway
hermes logs --since 1h
hermes logs --component tools
hermes logs -f
```

推荐理解方式：

| 场景 | 建议命令 |
|---|---|
| 看最近 agent 行为 | `hermes logs` |
| 看报错 | `hermes logs errors -n 100` |
| 看网关异常 | `hermes logs gateway -n 100` |
| 看最近一小时 | `hermes logs --since 1h` |
| 跟踪实时日志 | `hermes logs -f` |

## 4. 会话排查

如果问题和某个历史会话有关，可以使用：

```bash
hermes sessions --help
```

当前可见子命令包括：

- `list`
- `export`
- `delete`
- `prune`
- `stats`
- `rename`
- `browse`

常用入口：

```bash
hermes sessions list
hermes sessions stats
hermes sessions browse
```

## 5. 针对不同问题的建议顺序

### 配置没生效

1. `hermes config show`
2. `hermes config path`
3. `hermes doctor`
4. `hermes gateway restart`

### 平台不回消息

1. `hermes status --all`
2. `hermes gateway status`
3. `hermes logs gateway -n 100`
4. 必要时 `hermes gateway restart`

### provider / 凭证异常

1. `hermes model`
2. `hermes login --help`
3. `hermes auth list`
4. `hermes status --all`

### MCP / tools 不可用

1. `hermes mcp list`
2. `hermes mcp test <name>`
3. `hermes tools list --platform cli`
4. `hermes logs --component tools`

## 6. 最小命令清单

```bash
hermes status --all
hermes doctor
hermes logs errors -n 100
hermes logs gateway -n 100
hermes sessions stats
```
