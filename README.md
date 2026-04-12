# evolve

一个公开分享仓库，用于发布可公开传播的：

- 项目总结
- 技术方案
- 架构设计
- 研究笔记
- AI 生成的分享内容

站点使用 **MkDocs Material** 构建，并计划发布到：

- GitHub Pages
- 自定义域名：`https://evolve.liveppp.com`

## 本地预览

```bash
cd ~/Projects/evolve
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
mkdocs serve
```

## 构建

```bash
source .venv/bin/activate
mkdocs build
```
