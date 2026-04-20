#!/usr/bin/env python3
"""
检查所有文章页面是否都有分享组件
并生成报告
"""

import subprocess
import sys
from pathlib import Path

# 文章页面列表（相对于 docs 目录）
ARTICLE_PATHS = [
    # 报告
    "reports/open-agents-architecture-summary/",
    "reports/hermes-agent-advanced-guide/",
    "reports/hermes-agent-self-evolution/",
    "reports/multi-agent-virtual-company-fallacy/",
    "reports/ai-site-optimization-loop/",
    # 工具
    "tools/markitdown-guide/",
    # Hermes
    "hermes/command-cheatsheet/",
    "hermes/gateway/",
    "hermes/platform-integrations/",
    "hermes/config-files-and-maintenance/",
    "hermes/providers-and-credentials/",
    "hermes/profiles/",
    "hermes/tools-and-mcp/",
    "hermes/troubleshooting/",
    "hermes/performance/",
    # 免费模型
    "free-models/elephant-alpha/",
    "free-models/nemotron-3-super-120b-a12b-free/",
    "free-models/nemotron-3-nano-30b-a3b-free/",
    "free-models/gemma-4-31b-it-free/",
    "free-models/gemma-4-26b-a4b-it-free/",
    "free-models/qwen3-coder-480b-free/",
    "free-models/minimax-m2.5-free/",
    "free-models/llama-3.3-70b-instruct-free/",
    "free-models/gpt-oss-120b-free/",
    "free-models/gpt-oss-20b-free/",
    # 站点信息
    "site-info/about/",
    "site-info/contact/",
    "site-info/privacy-policy/",
    "site-info/disclaimer/",
    # 其他
    "hermes-config/",
]

BASE_URL = "https://evolve.liveppp.com"


def check_page(path: str) -> dict:
    """检查单个页面是否有分享组件"""
    url = f"{BASE_URL}/{path}"
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "10", url],
            capture_output=True,
            text=True,
            timeout=15
        )
        has_share = "share-section" in result.stdout
        return {
            "path": path,
            "url": url,
            "has_share": has_share,
            "status": "✅" if has_share else "❌ MISSING"
        }
    except subprocess.TimeoutExpired:
        return {"path": path, "url": url, "has_share": False, "status": "⏱️ TIMEOUT"}
    except Exception as e:
        return {"path": path, "url": url, "has_share": False, "status": f"💥 ERROR: {e}"}


def main():
    print("🔍 检查 Evolve 站点分享组件配置...\n")
    
    results = []
    for path in ARTICLE_PATHS:
        result = check_page(path)
        results.append(result)
        print(f"{result['status']} {path}")
    
    # 统计
    total = len(results)
    ok = sum(1 for r in results if r["has_share"])
    failed = total - ok
    
    print(f"\n{'='*60}")
    print(f"总计: {total} 个页面")
    print(f"✅ 正常: {ok} 个")
    print(f"❌ 异常: {failed} 个")
    
    if failed > 0:
        print(f"\n⚠️  以下页面缺少分享组件:")
        for r in results:
            if not r["has_share"]:
                print(f"   - {r['path']}")
        print(f"\n💡 提示: 分享组件通过主题模板全局添加，如果页面缺少可能是:")
        print("   1. 页面构建缓存问题，尝试重新部署")
        print("   2. 页面模板被覆盖，检查 overrides/main.html")
        return 1
    else:
        print(f"\n🎉 所有页面分享组件配置正常！")
        return 0


if __name__ == "__main__":
    sys.exit(main())
