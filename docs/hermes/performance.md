# Hermes 提速配置

这页聚焦 Hermes 的响应速度优化，适合在感觉“回复偏慢”“会话越聊越卡”时优先排查。

!!! abstract "阅读建议"
    如果只想先快速提速，优先调整：

    1. `agent.reasoning_effort`
    2. `display.tool_progress`
    3. `compression.threshold`

## 一页速查

| 配置项 | 推荐值 | 主要作用 | 适用场景 |
|---|---|---|---|
| `agent.reasoning_effort` | `minimal` | 降低推理强度，通常最明显提速 | 大多数日常问答 |
| `agent.reasoning_effort` | `none` | 进一步追求速度 | 简单任务、容忍回答质量下降 |
| `display.tool_progress` | `off` | 减少界面过程播报 | 不需要持续看工具执行过程 |
| `compression.threshold` | `0.6` | 更早压缩长会话上下文 | 长对话越来越慢 |

## 1. 降低 reasoning 强度

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

## 2. 关闭 tool progress 过程播报

如果不需要在界面里持续看到工具执行过程，可以关闭：

```bash
hermes config set display.tool_progress off
```

说明：

- 这个配置主要改善使用体感和界面噪音
- 对模型实际推理耗时帮助不如 reasoning 配置明显，但通常也值得一起调整

## 3. 提前压缩长上下文

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

## 修改后如何验证

建议按下面顺序验证：

1. 开一个新会话，观察首条回复速度
2. 再连续提几个需要工具调用的问题，观察体感差异
3. 如果是长对话场景，再验证多轮后的响应速度是否改善

## 当前已记录的提速结论

- 优先改 `agent.reasoning_effort`
- 其次可关掉 `display.tool_progress`
- 长会话场景下可把 `compression.threshold` 调低
- 如果还嫌慢，优先换更快模型
