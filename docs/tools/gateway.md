# Hermes Gateway 配置

这页聚焦 Hermes 消息网关（gateway）的运行、安装、重启与平台接入。

## Gateway 能做什么

`hermes gateway` 用于管理消息网关，CLI 帮助说明它主要面向消息平台接入与运行管理。

查看帮助：

```bash
hermes gateway --help
```

## 常用子命令

| 命令 | 作用 |
|---|---|
| `hermes gateway run` | 前台运行 gateway |
| `hermes gateway start` | 启动已安装的后台服务 |
| `hermes gateway stop` | 停止后台服务 |
| `hermes gateway restart` | 重启 gateway |
| `hermes gateway status` | 查看状态 |
| `hermes gateway install` | 安装为后台服务 |
| `hermes gateway uninstall` | 卸载后台服务 |
| `hermes gateway setup` | 配置消息平台 |

## 1. 前台运行

在 WSL、Docker、Termux 这类环境中，帮助信息里明确建议优先使用前台运行：

```bash
hermes gateway run
```

## 2. 后台服务管理

如果已经把 gateway 安装成系统服务，可以用下面这些命令管理：

```bash
hermes gateway start
hermes gateway stop
hermes gateway restart
hermes gateway status
```

## 3. 平台接入配置

如果你要新增或调整消息平台接入，可以使用：

```bash
hermes gateway setup
```

这个入口更适合做平台侧配置，而不是直接手改后忘记校验。

## 4. 什么时候需要重启 Gateway

以下情况通常建议重启：

- 修改了 Hermes 的关键配置
- 调整了 provider / 模型设置后，希望让网关侧会话尽快使用新配置
- 修改了消息平台接入参数

对应命令：

```bash
hermes gateway restart
```

## 5. 一个常见操作流

| 场景 | 建议操作 |
|---|---|
| 首次配置消息平台 | `hermes gateway setup` |
| 本地调试网关 | `hermes gateway run` |
| 已安装成服务后启动 | `hermes gateway start` |
| 改完配置后生效 | `hermes gateway restart` |
| 怀疑网关异常 | `hermes gateway status` |

## 6. 最小命令清单

```bash
hermes gateway setup
hermes gateway run
hermes gateway status
hermes gateway restart
```
