# Hermes 平台接入与消息入口

这页聚焦 Hermes 通过消息平台接入的常用入口，适合处理 Feishu、Telegram、Discord、Weixin 等平台相关操作。

!!! abstract "阅读地图"
    平台接入相关排查，通常按这个顺序：

    1. 看总状态：`hermes status --all`
    2. 配置网关：`hermes gateway setup`
    3. 管理用户配对：`hermes pairing ...`
    4. 管理 webhook：`hermes webhook ...`
    5. 查日志：`hermes logs gateway`

## 当前 CLI 能看到的相关能力

从 `hermes status --all` 与 CLI 帮助来看，当前 Hermes 环境里常见的平台包括：

- Telegram
- Discord
- Feishu
- Weixin
- WhatsApp（CLI 帮助中可见专用命令）

## 1. 先看整体状态

排查平台接入问题时，最先执行：

```bash
hermes status --all
```

这个命令可以帮助你快速看见：

- 哪些消息平台已经配置
- gateway 是否正在运行
- 当前模型 / provider 是否正常
- 是否存在明显缺失项

## 2. 配置消息平台

最直接的入口是：

```bash
hermes gateway setup
```

适合用在这些场景：

| 场景 | 建议操作 |
|---|---|
| 首次接入新平台 | `hermes gateway setup` |
| 已配置但想重做平台设置 | `hermes gateway setup` |
| 改完配置想生效 | `hermes gateway restart` |

## 3. 运行与重启 Gateway

平台接入通常依赖 gateway 正常运行：

```bash
hermes gateway status
hermes gateway restart
```

如果你在本地前台调试，也可以直接：

```bash
hermes gateway run
```

## 4. 配对授权（pairing）

如果你的接入流程涉及用户授权 / pairing code，可以使用：

```bash
hermes pairing --help
```

当前可见的子命令有：

```bash
hermes pairing list
hermes pairing approve <code>
hermes pairing revoke <user>
hermes pairing clear-pending
```

适用理解：

| 命令 | 用途 |
|---|---|
| `hermes pairing list` | 查看待审批和已批准用户 |
| `hermes pairing approve ...` | 批准配对码 |
| `hermes pairing revoke ...` | 撤销某个用户访问 |
| `hermes pairing clear-pending` | 清空待处理配对请求 |

## 5. Webhook 订阅

如果你的平台接入依赖事件驱动 webhook，可以使用：

```bash
hermes webhook --help
```

当前可见的子命令有：

```bash
hermes webhook subscribe
hermes webhook list
hermes webhook remove
hermes webhook test
```

推荐理解方式：

| 场景 | 命令 |
|---|---|
| 新增订阅 | `hermes webhook subscribe` |
| 查看当前订阅 | `hermes webhook list` |
| 删除订阅 | `hermes webhook remove` |
| 验证 webhook 路由是否通 | `hermes webhook test` |

## 6. 平台问题的最小排查流

当出现“消息没进来”“平台不回消息”“接入状态异常”时，可以先跑这一组：

```bash
hermes status --all
hermes gateway status
hermes logs gateway -n 100
```

如果涉及重新配置：

```bash
hermes gateway setup
hermes gateway restart
```

## 7. 最小命令清单

```bash
hermes status --all
hermes gateway setup
hermes gateway status
hermes pairing list
hermes webhook list
hermes logs gateway -n 100
```
