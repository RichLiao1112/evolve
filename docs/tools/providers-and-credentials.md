# Hermes Provider / 凭证配置

这页聚焦 Hermes 的模型提供方选择、登录方式与凭证池管理。

## 适用场景

| 需求 | 建议命令 |
|---|---|
| 交互式选择默认 provider 和 model | `hermes model` |
| 走 OAuth 登录某个 provider | `hermes login --provider <provider>` |
| 管理 pooled credentials | `hermes auth add/list/remove/reset` |
| 查看当前配置文件位置 | `hermes config path` |
| 查看 `.env` 位置 | `hermes config env-path` |

## 1. 选择默认 Provider 和模型

最直接的入口是：

```bash
hermes model
```

这个命令用于**交互式选择默认 inference provider 和默认模型**。

## 2. Provider 登录

Hermes 提供了 `login` 命令用于认证 provider。

查看帮助：

```bash
hermes login --help
```

当前 CLI 帮助里可见的 provider 选项是：

```bash
hermes login --provider nous
hermes login --provider openai-codex
```

如果你不想自动打开浏览器，可以加：

```bash
hermes login --provider nous --no-browser
```

## 3. 凭证池（pooled credentials）管理

如果需要为某个 provider 管理多组凭证，可以使用 `hermes auth`。

### 查看帮助

```bash
hermes auth --help
```

### 常用命令

```bash
hermes auth list
```

```bash
hermes auth add <provider>
```

```bash
hermes auth remove <provider> <index_or_id_or_label>
```

```bash
hermes auth reset <provider>
```

## 4. 配置文件与 `.env` 路径

如果你不确定 Hermes 的配置文件或环境变量文件放在哪里，可以直接查：

```bash
hermes config path
hermes config env-path
```

这样比手动猜目录更稳妥。

## 5. 推荐整理方式

可以把 provider / 凭证相关操作分成三层理解：

| 层级 | 作用 | 典型命令 |
|---|---|---|
| 默认模型选择 | 决定平时优先用哪个 provider / model | `hermes model` |
| 登录认证 | 为某个 provider 建立认证状态 | `hermes login ...` |
| 凭证池管理 | 管理多组 provider 凭证 | `hermes auth ...` |

## 6. 常见排查顺序

当遇到“模型不能用”“provider 切不过去”“凭证状态不对”时，建议按这个顺序排查：

1. 先执行 `hermes model`，确认默认 provider / model 是否选对
2. 再执行 `hermes login --help` 或对应登录命令，确认认证方式
3. 如果用了凭证池，再执行 `hermes auth list`
4. 必要时查看配置文件位置：`hermes config path`、`hermes config env-path`

## 7. 最小命令清单

```bash
hermes model
hermes login --provider nous
hermes auth list
hermes config path
hermes config env-path
```
