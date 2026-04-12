# Hermes Profiles / 多实例管理

这页聚焦 Hermes profile 的创建、切换、导入导出，以及多实例隔离使用方式。

## Profiles 是什么

`hermes profile` 用于管理多个隔离的 Hermes 实例配置。

查看帮助：

```bash
hermes profile --help
```

当前可见的子命令包括：

- `list`
- `use`
- `create`
- `delete`
- `show`
- `alias`
- `rename`
- `export`
- `import`

## 1. 查看当前有哪些 Profile

```bash
hermes profile list
```

适合先了解当前机器上有哪些独立实例。

## 2. 创建新 Profile

```bash
hermes profile create <profile_name>
```

根据帮助，创建时常见选项包括：

| 参数 | 作用 |
|---|---|
| `--clone` | 复制当前 active profile 的 `config.yaml`、`.env`、`SOUL.md` |
| `--clone-all` | 完整复制当前 active profile 的全部状态 |
| `--clone-from <source>` | 从指定 profile 复制 |
| `--no-alias` | 不创建 wrapper script |

这意味着创建 profile 时通常有三种策略：

| 策略 | 适合场景 |
|---|---|
| 纯新建 | 想从零开始 |
| `--clone` | 想沿用配置但不复制全部状态 |
| `--clone-all` | 想快速复制一个几乎完整的实例 |

## 3. 切换默认 Profile

```bash
hermes profile use <profile_name>
```

帮助中说明它会设置 sticky default profile，也就是后续默认使用这个 profile。

## 4. 查看单个 Profile 详情

```bash
hermes profile show <profile_name>
```

适合确认某个 profile 的具体信息。

## 5. 重命名、删除、导入导出

```bash
hermes profile rename <old> <new>
hermes profile delete <profile_name>
hermes profile export <profile_name>
hermes profile import <archive>
```

这些操作适合用于：

- 统一命名
- 清理废弃 profile
- 迁移到另一台机器
- 备份某个可用实例

## 6. 适合怎么用多 Profile

可以把 profile 理解成几类典型隔离环境：

| 类型 | 用途 |
|---|---|
| 日常主实例 | 日常聊天和默认自动化 |
| 测试实例 | 验证新 provider / 新配置 |
| 平台专用实例 | 某个平台或某类 webhook 独立运行 |
| 实验实例 | 测试 MCP、插件、工具组合 |

## 7. 推荐操作流

如果你想安全测试新配置，推荐这样做：

1. `hermes profile create test --clone`
2. `hermes profile use test`
3. 调整 provider / tools / gateway 配置
4. 验证没问题后，再决定是否迁回主 profile

## 8. 最小命令清单

```bash
hermes profile list
hermes profile create test --clone
hermes profile use test
hermes profile show test
hermes profile export test
```
