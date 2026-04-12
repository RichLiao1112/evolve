# Hermes 配置记录

这个文档用于统一记录 Hermes 相关的常用配置、调优项和维护备注，后续有新的 Hermes 设置也继续补在这里。

## 响应速度优化

如果感觉 Hermes 回复偏慢，优先检查和调整下面这些配置。

### 1. 降低 reasoning 强度

当前最影响响应速度的配置之一是 `agent.reasoning_effort`。

推荐优先尝试：

```bash
hermes config set agent.reasoning_effort minimal
```

如果更追求速度，也可以进一步改成：

```bash
hermes config set agent.reasoning_effort none
```

说明：
- `minimal`：通常是速度和质量的较好平衡
- `none`：更快，但复杂问题的回答质量可能下降

### 2. 关闭 tool progress 过程播报

如果不需要在界面里持续看到工具执行过程，可以关闭：

```bash
hermes config set display.tool_progress off
```

说明：
- 这个配置主要改善使用体感和界面噪音
- 对模型实际推理耗时帮助不如 reasoning 配置明显，但通常也值得一起调整

### 3. 提前压缩长上下文

如果是“会话越聊越慢”，可以降低压缩阈值：

```bash
hermes config set compression.threshold 0.6
```

说明：
- 当前阈值过高时，长会话会携带更多历史上下文
- 降低阈值后，Hermes 会更早做上下文压缩，从而减少后续请求负担

## 推荐组合

日常使用可以先试这一组：

```bash
hermes config set agent.reasoning_effort minimal
hermes config set display.tool_progress off
hermes config set compression.threshold 0.6
```

## 模型层面的提速

如果做完上面几项还是觉得慢，可以进一步考虑：

```bash
hermes model
```

切换到更快的模型，通常会比单纯调显示项更有效。

## 修改后生效建议

如果当前是通过 gateway / Feishu / Telegram 等方式使用 Hermes，改完配置后建议重启服务：

```bash
hermes gateway restart
```

如果只是本地 CLI，也可以直接开启新会话验证效果。

## 当前已记录的提速结论

- 优先改 `agent.reasoning_effort`
- 其次可关掉 `display.tool_progress`
- 长会话场景下可把 `compression.threshold` 调低
- 如果还嫌慢，优先换更快模型
