#!/bin/bash
###############################################################################
# 图像生成大师 - Shell 脚本
# 
# 使用方法：
#   ./generate.sh "提示词" [选项]
# 
# 示例：
#   ./generate.sh "一只可爱的橘猫"
#   ./generate.sh "赛博朋克城市" --model flux-pro --size 1024x1024
#   ./generate.sh "风景画" --aspect-ratio 16:9 --n 2
###############################################################################

# 默认值
MODEL=""
PROVIDER=""
SIZE=""
ASPECT_RATIO=""
N=1
IMAGE_URLS=""

# 检查是否提供了提示词
if [ -z "$1" ]; then
    echo "❌ 错误: 必须提供提示词"
    echo ""
    echo "使用方法: $0 \"提示词\" [选项]"
    echo ""
    echo "选项:"
    echo "  --model <模型名>        指定模型 (如: nano-banana, flux-pro)"
    echo "  --provider <供应商>     指定供应商 (blt/grsai)"
    echo "  --size <尺寸>          图片尺寸 (如: 1024x1024)"
    echo "  --aspect-ratio <比例>  宽高比 (如: 16:9, 9:16)"
    echo "  --n <数量>            生成数量 (默认: 1)"
    echo "  --image-url <URL>      参考图片 URL (图生图)"
    echo ""
    echo "示例:"
    echo "  $0 \"一只可爱的橘猫\""
    echo "  $0 \"赛博朋克城市\" --model flux-pro --size 1024x1024"
    echo "  $0 \"风景画\" --aspect-ratio 16:9 --n 2"
    exit 1
fi

PROMPT="$1"
shift

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL="$2"
            shift 2
            ;;
        --provider)
            PROVIDER="$2"
            shift 2
            ;;
        --size)
            SIZE="$2"
            shift 2
            ;;
        --aspect-ratio)
            ASPECT_RATIO="$2"
            shift 2
            ;;
        --n)
            N="$2"
            shift 2
            ;;
        --image-url)
            IMAGE_URLS="$2"
            shift 2
            ;;
        -h|--help)
            echo "图像生成大师 - Shell 脚本"
            echo ""
            echo "使用方法: $0 \"提示词\" [选项]"
            echo ""
            echo "选项:"
            echo "  --model <模型名>        指定模型 (如: nano-banana, flux-pro)"
            echo "  --provider <供应商>     指定供应商 (blt/grsai)"
            echo "  --size <尺寸>          图片尺寸 (如: 1024x1024)"
            echo "  --aspect-ratio <比例>  宽高比 (如: 16:9, 9:16)"
            echo "  --n <数量>            生成数量 (默认: 1)"
            echo "  --image-url <URL>      参考图片 URL (图生图)"
            echo ""
            echo "示例:"
            echo "  $0 \"一只可爱的橘猫\""
            echo "  $0 \"赛博朋克城市\" --model flux-pro --size 1024x1024"
            echo "  $0 \"风景画\" --aspect-ratio 16:9 --n 2"
            exit 0
            ;;
        *)
            echo "❌ 错误: 未知参数 '$1'"
            echo "使用 '$0 --help' 查看帮助"
            exit 1
            ;;
    esac
done

# 构建 JSON 输入
JSON_INPUT="{\"prompt\": \"$PROMPT\""

if [ -n "$MODEL" ]; then
    JSON_INPUT="$JSON_INPUT, \"model\": \"$MODEL\""
fi

if [ -n "$PROVIDER" ]; then
    JSON_INPUT="$JSON_INPUT, \"provider\": \"$PROVIDER\""
fi

if [ -n "$SIZE" ]; then
    JSON_INPUT="$JSON_INPUT, \"size\": \"$SIZE\""
fi

if [ -n "$ASPECT_RATIO" ]; then
    JSON_INPUT="$JSON_INPUT, \"aspect_ratio\": \"$ASPECT_RATIO\""
fi

if [ "$N" -gt 1 ]; then
    JSON_INPUT="$JSON_INPUT, \"n\": $N"
fi

if [ -n "$IMAGE_URLS" ]; then
    JSON_INPUT="$JSON_INPUT, \"image_urls\": [\"$IMAGE_URLS\"]"
fi

JSON_INPUT="$JSON_INPUT }"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 调用 Python 代码
cd "$SCRIPT_DIR/.." || exit 1

python3 -c "
import asyncio
import sys
import json
sys.path.insert(0, '.')
from image_generation_master.skill import run_sync

try:
    result = run_sync($JSON_INPUT)
    print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    print(json.dumps({
        'success': False,
        'images': [],
        'provider': None,
        'model': None,
        'message': f'执行错误: {str(e)}'
    }, ensure_ascii=False, indent=2))
    sys.exit(1)
"

exit_code=$?

# 如果成功，显示友好的输出
if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✅ 生成完成！"
fi

exit $exit_code
