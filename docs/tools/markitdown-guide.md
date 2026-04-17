---
description: MarkItDown 是微软开源的文件转 Markdown 工具，支持 PDF、Word、PPT、Excel、HTML、图片 OCR 等格式，适合 RAG、知识库与 LLM 文档预处理。
keywords: MarkItDown, Markdown转换, PDF转Markdown, Word转Markdown, PPT转Markdown, Excel转Markdown, RAG工具, 文档预处理
date: 2026-04-17
---

# MarkItDown：把 PDF / Word / PPT / Excel 转成 Markdown 的轻量工具

## 相关地址

- 项目仓库：https://github.com/microsoft/markitdown
- README：https://github.com/microsoft/markitdown/blob/main/README.md
- PyPI：https://pypi.org/project/markitdown/
- MCP 包说明：https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp

## 先给结论

如果你经常要把 **PDF、Word、PPT、Excel、网页或图片内容喂给 LLM**，`microsoft/markitdown` 很值得装一个。

它的核心价值不是“高保真排版还原”，而是：

> **尽量保留文档结构，然后把内容稳定地转成适合 LLM 消费的 Markdown。**

对于这类场景，它比“直接抽纯文本”更好用：

- 做知识库入库
- 做 RAG 预处理
- 做文档总结 / 提取 / 问答
- 给 Agent 提供更干净的输入

## 快速判断

| 问题 | 快速判断 |
| --- | --- |
| 值不值得装 | 值得，尤其是你有大量办公文档要进 LLM 流程时 |
| 适不适合做知识库预处理 | 很适合 |
| 适不适合追求“版式还原” | 不适合，它重点是结构化文本，不是排版复刻 |
| 上手难不难 | 不难，CLI 一条命令就能用 |
| 要不要接进 Agent / RAG 流程 | 可以，甚至很适合做中间层工具 |

## 关键信息

| 项目 | 信息 |
| --- | --- |
| 名称 | MarkItDown |
| 仓库 | `microsoft/markitdown` |
| 定位 | 多格式文件转 Markdown |
| 维护方 | Microsoft / AutoGen 团队 |
| License | MIT |
| Python 要求 | `>=3.10` |
| 使用方式 | CLI、Python API、MCP Server |
| 适合场景 | RAG、知识库、文档预处理、Agent 输入清洗 |

## 支持什么格式

MarkItDown 的覆盖面相当广，常见可用的包括：

- PDF
- Word (`.docx`)
- PowerPoint (`.pptx`)
- Excel (`.xlsx` / `.xls`)
- HTML
- CSV / JSON / XML
- EPUB
- ZIP
- 图片
- 音频
- YouTube URL
- RSS / Wikipedia 等网页型内容

它并不是每种格式都默认装满依赖，而是采用 **按需安装** 的方式。

这点很实用：

- 只处理 PDF / DOCX / PPTX，可以只装对应依赖
- 想一步到位，也可以直接安装 `all`

## 为什么它适合 LLM 工作流

很多“文档转文本”工具的问题在于：

1. 只抽纯文本，结构全没了
2. 表格、标题、列表都乱掉
3. 给模型后，上下文可读性很差

MarkItDown 的方向更明确：

- 尽量保留标题层级
- 尽量保留列表、表格、链接等结构
- 输出 Markdown，而不是乱糟糟的文本块

这对 LLM 很重要，因为 Markdown 同时满足两件事：

- **足够接近纯文本，token 开销低**
- **又保留了结构，模型更容易理解上下文**

所以它很适合放在这条链路里：

```text
原始文件 -> MarkItDown -> Markdown -> 清洗/切块 -> Embedding / LLM / Agent
```

## 最短使用攻略

### 1. 安装

最省事的方式：

```bash
pip install 'markitdown[all]'
```

如果你只想装部分能力，也可以按需装：

```bash
pip install 'markitdown[pdf,docx,pptx]'
```

### 2. CLI 直接转换

```bash
markitdown file.pdf > output.md
```

或者指定输出文件：

```bash
markitdown file.pdf -o output.md
```

这已经够覆盖很多日常场景了。

### 3. Python 里调用

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("example.pdf")
print(result.text_content)
```

如果你要把它接进自己的脚本、RAG 流程、知识库流水线，这种方式最直接。

### 4. 需要图片 OCR / 视觉能力时

它还可以配合 LLM Vision 做 OCR 或图片描述。

典型用法：

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
)
result = md.convert("image.jpg")
print(result.text_content)
```

这对下面这些内容特别有用：

- 扫描版 PDF
- PPT 里的图片文字
- 文档中的截图内容
- 需要 OCR 的图片材料

## 什么时候优先用它

优先考虑 MarkItDown 的典型场景：

### 场景 1：做知识库入库

你有一堆：

- PDF 手册
- Word 方案文档
- PPT 汇报材料
- Excel 表格说明

想统一转成 Markdown 再丢进知识库或向量库，MarkItDown 很合适。

### 场景 2：给 Agent 准备输入材料

如果你希望 Agent 阅读文档后再行动，直接给原始 PDF/Docx 往往不稳定。

更稳的做法通常是：

```text
文档 -> MarkItDown -> Markdown -> Agent
```

这样更可控，也更容易调试。

### 场景 3：做 RAG 前处理

RAG 项目里，一个很常见的问题是：

- 原始文档格式多样
- 抽出来的文本质量不一致
- 切块前很难统一结构

MarkItDown 正好能承担“统一入口格式”的角色。

## 不要对它期待错的地方

它很好用，但不要期待错方向。

### 1. 它不是高保真排版还原工具

如果你的目标是：

- 尽可能还原原始页面布局
- 1:1 复刻视觉排版
- 输出给人直接阅读展示

那它不是最优解。

它更像是：

> 为机器理解做的文档结构提取工具。

### 2. 某些格式仍然依赖可选组件

比如 PDF、Office、OCR、音频转录这类能力，很多不是“裸装即全有”。

所以如果你遇到某个格式不能转，先看是不是少装了对应 extra，而不是直接判断它“不支持”。

### 3. 复杂文档也不可能百分百完美

尤其是：

- 扫描件
- 表格很多的 PDF
- 很重的视觉排版
- 混杂图片、公式、嵌入对象的文档

这类内容再强的转换器也可能需要后处理。

## 进阶用法：MCP Server

MarkItDown 现在还带了 MCP Server。

这意味着它不只是一个 CLI 工具，也可以作为 **LLM 应用的文档转换能力节点**。

简单理解就是：

- 你的 Claude Desktop / 其他 MCP 客户端
- 可以通过 MCP 调用 MarkItDown
- 直接把文件或 URI 转成 Markdown

如果你已经在做 Agent / MCP 工作流，这点很加分。

## 最后的建议

如果你只想记住一个判断，可以记这个：

> **只要你的目标是“把复杂文件变成适合 LLM 处理的 Markdown”，MarkItDown 基本都值得先试。**

尤其是这些场景，优先级很高：

- 文档喂给大模型前的预处理
- 知识库文档标准化
- RAG 数据清洗
- Agent 的外部材料输入统一化

而且它的门槛很低：

- 命令行可直接用
- Python 可嵌入
- 还有 MCP 版本可接工作流

这类工具很适合常备一个。

## 信息来源说明

本文基于 `microsoft/markitdown` 当前 README、包结构与源码目录整理，重点从“是否值得接进实际工作流”的角度总结，而不是做逐文件源码解读。