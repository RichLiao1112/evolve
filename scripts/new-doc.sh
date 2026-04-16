#!/bin/bash
# 新建 SEO 优化文档的便捷脚本

# 用法: ./scripts/new-doc.sh <类型> <文件名>
# 类型: free-model, hermes, report, default
# 示例: ./scripts/new-doc.sh free-model qwen3-235b

TYPE=$1
FILENAME=$2

if [ -z "$TYPE" ] || [ -z "$FILENAME" ]; then
    echo "用法: ./scripts/new-doc.sh <类型> <文件名>"
    echo ""
    echo "类型选项:"
    echo "  free-model  - 免费模型文章 (保存到 docs/free-models/)"
    echo "  hermes      - Hermes 配置文档 (保存到 docs/hermes/)"
    echo "  report      - 技术报告 (保存到 docs/reports/)"
    echo "  default     - 默认文档 (保存到 docs/)"
    echo ""
    echo "示例:"
    echo "  ./scripts/new-doc.sh free-model qwen3-235b"
    exit 1
fi

# 确定目录和模板
case $TYPE in
    free-model)
        DIR="docs/free-models"
        TEMPLATE="scripts/template-free-model.md"
        ;;
    hermes)
        DIR="docs/hermes"
        TEMPLATE="scripts/template-default.md"
        ;;
    report)
        DIR="docs/reports"
        TEMPLATE="scripts/template-default.md"
        ;;
    default)
        DIR="docs"
        TEMPLATE="scripts/template-default.md"
        ;;
    *)
        echo "错误：未知类型 '$TYPE'"
        exit 1
        ;;
esac

# 确保目录存在
mkdir -p "$DIR"

# 生成文件路径
FILEPATH="$DIR/$FILENAME.md"

# 检查文件是否已存在
if [ -f "$FILEPATH" ]; then
    echo "错误：文件已存在: $FILEPATH"
    exit 1
fi

# 获取当前日期
DATE=$(date +%Y-%m-%d)

# 从文件名生成标题（将连字符替换为空格，首字母大写）
TITLE=$(echo "$FILENAME" | sed 's/-/ /g' | sed 's/\b\w/\u&/g')

# 复制模板并替换变量
if [ -f "$TEMPLATE" ]; then
    sed -e "s/{{title}}/$TITLE/" \
        -e "s/{{date}}/$DATE/" \
        -e "s/{{description}}/待填写：文章描述/" \
        -e "s/{{keywords}}/待填写：关键词1, 关键词2/" \
        -e "s/{{summary}}/待填写：一句话总结/" \
        "$TEMPLATE" > "$FILEPATH"
else
    # 如果没有模板，创建基本结构
    cat > "$FILEPATH" << EOF
---
description: 待填写：文章描述（50-160字）
keywords: 待填写：关键词1, 关键词2, 关键词3
date: $DATE
---

# $TITLE

## 先给结论

待填写：一句话总结

---

## 正文内容

EOF
fi

echo "✅ 已创建: $FILEPATH"
echo ""
echo "💡 下一步:"
echo "  1. 编辑文件，填写 description 和 keywords"
echo "  2. 运行 'python scripts/auto-seo.py' 自动优化（可选）"
echo "  3. 在 mkdocs.yml 中添加导航链接"
