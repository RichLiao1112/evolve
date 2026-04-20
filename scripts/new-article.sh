#!/bin/bash
# 创建新文章并自动配置分享所需的前置元数据

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_FILE="$SCRIPT_DIR/templates/article-template.md"

default_date=$(date +%Y-%m-%d)

show_usage() {
    echo "用法: $0 <文章路径> [标题]"
    echo ""
    echo "示例:"
    echo "  $0 reports/my-new-article.md \"我的新文章标题\""
    echo "  $0 free-models/new-model.md \"New Model - 免费模型 - 2026-01-01\""
    echo ""
    echo "注意: 文章路径相对于 docs/ 目录"
}

if [ $# -lt 1 ]; then
    show_usage
    exit 1
fi

article_path="$1"
title="${2:-$(basename "$article_path" .md)}"
full_path="$SCRIPT_DIR/../docs/$article_path"

# 检查文件是否已存在
if [ -f "$full_path" ]; then
    echo "❌ 文件已存在: $full_path"
    exit 1
fi

# 创建目录
mkdir -p "$(dirname "$full_path")"

# 从模板创建文件，替换变量
sed -e "s/文章标题/$title/g" \
    -e "s/YYYY-MM-DD/$default_date/g" \
    -e "s/文章描述（50-160字，用于分享卡片和SEO）/请填写文章描述/g" \
    "$TEMPLATE_FILE" > "$full_path"

echo "✅ 已创建文章: $full_path"
echo ""
echo "📝 下一步:"
echo "   1. 编辑文件: $full_path"
echo "   2. 完善 description 和 keywords（用于分享卡片）"
echo "   3. 更新 mkdocs.yml 添加导航"
echo "   4. 更新 docs/index.md 添加首页卡片（如需要）"
echo ""
echo "💡 分享组件会自动显示，无需额外配置"
