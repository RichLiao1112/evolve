---
hide:
  - toc
---

<div class="hero-panel">
  <p class="hero-eyebrow">Public reports · technical notes · research snapshots</p>
  <h1>Evolve</h1>
  <p class="hero-lead">
    一个适合外部传播的公开发布站，专门承载项目总结、技术方案、研究笔记与 AI 生成的可分享内容。这里的项目标题统一使用 Evolve 风格展示。
  </p>
  <div class="hero-actions">
    <a class="md-button md-button--primary" href="#latest-reports">查看最新报告</a>
    <a class="md-button" href="https://github.com/RichLiao1112/evolve" target="_blank" rel="noopener">访问 GitHub 仓库</a>
  </div>
</div>

<div class="summary-strip">
  <div>
    <span>站点定位</span>
    <strong>公开报告发布</strong>
  </div>
  <div>
    <span>阅读方式</span>
    <strong>摘要 + 链接</strong>
  </div>
  <div>
    <span>发布方式</span>
    <strong>Markdown → GitHub → Pages</strong>
  </div>
</div>

## 最新报告 { #latest-reports }

<div class="report-grid">
  <a class="report-card" href="reports/hermes-agent-self-evolution/">
    <div class="report-card__meta">项目总结 · AI Agent</div>
    <h3>Hermes Agent Self-Evolution 项目总结</h3>
    <p>重新解读这个项目：它不是在线自我改写的“活体 Agent”，而是一个面向 Hermes Agent 的离线优化与评测流水线。</p>
    <div class="report-card__tags">
      <span>DSPy</span>
      <span>GEPA</span>
      <span>LLM-as-a-Judge</span>
    </div>
  </a>

  <a class="report-card" href="reports/ai-site-optimization-loop/">
    <div class="report-card__meta">方案设计 · 网站增长</div>
    <h3>AI 持续优化网站闭环方案</h3>
    <p>从数据采集、AI 分析、自动改代码到灰度上线，搭建一个可持续运行的网站优化闭环。</p>
    <div class="report-card__tags">
      <span>PostHog</span>
      <span>Sentry</span>
      <span>Playwright</span>
    </div>
  </a>
</div>

## 这个站适合发什么

<div class="topic-grid">
  <div class="topic-card">
    <h3>项目总结</h3>
    <p>把一个项目的背景、方法、关键结果和可复用经验整理成可外发的文档。</p>
  </div>
  <div class="topic-card">
    <h3>技术方案</h3>
    <p>适合沉淀架构设计、自动化流程、部署策略和系统演进方向。</p>
  </div>
  <div class="topic-card">
    <h3>研究笔记</h3>
    <p>适合发布模型研究、工具评估、方案对比和阶段性洞察。</p>
  </div>
  <div class="topic-card">
    <h3>公开分享内容</h3>
    <p>适合从长文中抽出一版“可对外传播”的版本，用于群分享和沉淀链接资产。</p>
  </div>
</div>

## 发布节奏

1. 本地编写 Markdown。
2. 推送到 GitHub 仓库。
3. GitHub Actions 自动发布到 `evolve.liveppp.com`。
4. 对外渠道默认发送：**摘要 + evolve 链接**。

> 长内容放站点，群里只发摘要和入口，这样传播更轻、沉淀更稳。
