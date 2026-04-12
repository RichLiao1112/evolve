# Hermes Agent Self-Evolution 项目总结

## 项目概述

`hermes-agent-self-evolution` 是 Nous Research 开发的进化式自我改进系统，用于让 Hermes Agent 自动优化自己的技能、提示词和代码。

## 核心技术

1. **DSPy**：声明式语言模型编程框架
2. **GEPA**：Genetic-Pareto Prompt Evolution（遗传-帕累托提示进化）
3. **LLM-as-a-Judge**：用大模型评估输出质量

## 五阶段进化流程

### 1. Skills Evolution
- 自动优化 SKILL.md
- 改进技能描述、步骤与示例

### 2. Tools Evolution
- 优化工具 schema 和描述
- 改进参数说明与调用提示

### 3. Prompts Evolution
- 优化系统提示词
- 改进上下文组织策略

### 4. Code Evolution
- 用 Darwinian Evolver 自动优化实现代码
- 在测试与约束下迭代代码质量

### 5. Monitor Loop
- 持续收集指标
- 自动触发下一轮优化

## 项目结构

```text
hermes-agent-self-evolution/
├── evolution/
│   ├── core/
│   ├── skills/
│   ├── tools/
│   ├── prompts/
│   ├── code/
│   └── monitor/
├── datasets/
└── tests/
```

## 关键特性

- 自动数据集生成
- 多维度适应度评估
- Benchmark gate 防回归
- 自动生成 PR 与对比指标
- 约束验证（长度、兼容性、测试）

## 适用价值

这个项目的价值在于让 AI Agent 不仅能执行任务，还能在真实使用反馈中不断自我改进，形成持续进化闭环。
