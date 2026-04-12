# Hermes 配置文件与维护

这页聚焦 Hermes 配置文件位置、查看方式，以及配置检查与迁移命令。

## 配置管理入口

查看帮助：

```bash
hermes config --help
```

当前可见的子命令包括：

- `show`
- `edit`
- `set`
- `path`
- `env-path`
- `check`
- `migrate`

## 1. 查看当前配置

```bash
hermes config show
```

适合用来确认当前配置是否已经生效。

## 2. 编辑配置文件

```bash
hermes config edit
```

适合在需要一次性调整多个配置项时使用。

## 3. 直接设置单个配置项

```bash
hermes config set <key> <value>
```

例如：

```bash
hermes config set agent.reasoning_effort minimal
```

## 4. 查看配置文件与环境变量文件路径

```bash
hermes config path
hermes config env-path
```

这两个命令适合解决：

- 不确定 Hermes 到底在读哪个配置文件
- 不确定 `.env` 放在哪
- 想先定位文件再做备份或排查

## 5. 配置检查

```bash
hermes config check
```

适合在升级后或怀疑配置缺项时执行。

## 6. 配置迁移

```bash
hermes config migrate
```

适合在 Hermes 新版本引入新配置项后做同步更新。

## 7. 推荐维护习惯

| 动作 | 建议频率 | 对应命令 |
|---|---|---|
| 看当前值是否正确 | 改配置后立即 | `hermes config show` |
| 定位配置文件 | 排查时 | `hermes config path` |
| 看 `.env` 路径 | provider / token 排查时 | `hermes config env-path` |
| 检查配置缺项 | 升级后 | `hermes config check` |
| 同步新配置项 | 升级后 | `hermes config migrate` |

## 8. 建议的排查顺序

当你怀疑“改了配置但没生效”时，可以按下面顺序处理：

1. `hermes config show`
2. `hermes config path`
3. `hermes config env-path`
4. `hermes config check`
5. 必要时执行 `hermes gateway restart`
