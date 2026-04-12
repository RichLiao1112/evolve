# Evolve

> 一个公开分享仓库，用于发布可对外传播的技术内容。

## 📚 内容定位

本仓库承载以下类型的公开内容：

- **项目总结**：背景、方法、关键结果与可复用经验
- **技术方案**：架构设计、自动化流程、部署策略
- **研究笔记**：模型研究、工具评估、方案对比
- **公开分享**：从长文提炼的“可传播”版本

🔗 **在线站点**: [https://evolve.liveppp.com](https://evolve.liveppp.com)

---

## 🛠️ 技术栈

- **静态站点生成器**: [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- **部署平台**: GitHub Pages + 自定义域名
- **持续集成**: GitHub Actions

---

## 🚀 本地开发

### 环境准备

```bash
cd ~/Projects/evolve
```

### 创建虚拟环境

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 本地预览

```bash
mkdocs serve
```

访问 `http://127.0.0.1:8000` 查看效果。

### 构建生产版本

```bash
mkdocs build
```

构建产物位于 `site/` 目录。

---

## 📤 部署流程

### 1. 本地编写

在 `docs/` 目录下创建或编辑 Markdown 文件。

### 2. 提交更改

```bash
git add .
git commit -m "feat: 添加新报告或更新内容"
```

### 3. 推送到 GitHub

```bash
git push origin main
```

### 4. 自动部署

GitHub Actions 会自动触发构建并部署到：
- **GitHub Pages**: `https://richliao1112.github.io/evolve`
- **自定义域名**: `https://evolve.liveppp.com`

---

## 📝 内容规范

### 文件结构

```
docs/
├── index.md              # 首页
├── reports/              # 报告目录
│   ├── report-name.md    # 具体报告
│   └── ...
├── assets/
│   └── images/           # 图片资源
│       ├── logo-nav.png  # 导航栏 Logo
│       ├── evolve-logo.jpg # 首页吉祥物
│       └── arch/         # 架构图
└── stylesheets/
    └── extra.css         # 自定义样式
```

### 报告命名规范

- 使用小写字母和连字符：`my-awesome-report.md`
- 在 `mkdocs.yml` 的 `nav` 部分注册
- 文件名与导航标题保持一致

### 对外分享原则

- **长内容放站点**：详细技术内容放在 Evolve 网站
- **群里发链接**：在聊天渠道只发送摘要 + 链接
- **保持简洁**：首页只展示报告卡片，点击查看详情

> 传播更轻，沉淀更稳。

---

## 🎨 自定义

### 修改站点主题

编辑 `mkdocs.yml` 中的 `theme` 配置：

```yaml
theme:
  name: material
  language: zh
  palette:
    - scheme: default
      primary: blue grey
      accent: indigo
```

### 添加自定义样式

在 `docs/stylesheets/extra.css` 中添加 CSS 规则。

### 更换 Logo

- **导航栏 Logo**: `docs/assets/images/logo-nav.png` (50x50)
- **首页吉祥物**: `docs/assets/images/evolve-logo.jpg` (180px 宽)

---

## 🤝 贡献指南

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-content`)
3. 提交更改 (`git commit -m 'Add amazing content'`)
4. 推送到分支 (`git push origin feature/amazing-content`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证。内容可自由传播，但请保留署名。

---

**维护者**: RichLiao1112  
**最后更新**: 2026-04-12
