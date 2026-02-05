#!/usr/bin/env python3
"""
实际图片生成测试
"""
import asyncio
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from image_generation_master import run


async def test_blt_provider():
    """测试柏拉图平台"""
    print("🧪 测试柏拉图平台 (nano-banana)")
    print("   提示: 一只可爱的橘猫坐在窗台上\n")

    result = await run({
        "prompt": "一只可爱的橘猫坐在窗台上，阳光透过窗户洒在它身上",
        "provider": "blt",
        "model": "nano-banana",
        "size": "1024x1024"
    })

    if result["success"]:
        print(f"✅ 成功！生成了 {len(result['images'])} 张图片")
        for i, url in enumerate(result["images"], 1):
            print(f"   图片 {i}: {url}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result["success"]


async def test_grsai_provider():
    """测试 GrsAI 平台"""
    print("\n🧪 测试 GrsAI 平台 (nano-banana-pro)")
    print("   提示: 壮丽的山川河流，水墨画风格\n")

    result = await run({
        "prompt": "壮丽的山川河流，水墨画风格",
        "provider": "grsai",
        "model": "nano-banana-pro",
        "aspect_ratio": "16:9"
    })

    if result["success"]:
        print(f"✅ 成功！生成了 {len(result['images'])} 张图片")
        for i, url in enumerate(result["images"], 1):
            print(f"   图片 {i}: {url}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result["success"]


async def test_auto_provider():
    """测试自动选择供应商"""
    print("\n🧪 测试自动选择供应商")
    print("   提示: 未来科技城市，赛博朋克风格\n")

    result = await run({
        "prompt": "未来科技城市，赛博朋克风格，霓虹灯光",
        "model": "flux-pro",
        "size": "1024x1024"
    })

    if result["success"]:
        print(f"✅ 成功！")
        print(f"   使用的供应商: {result['provider']}")
        print(f"   使用的模型: {result['model']}")
        print(f"   生成了 {len(result['images'])} 张图片")
        for i, url in enumerate(result["images"], 1):
            print(f"   图片 {i}: {url}")
    else:
        print(f"❌ 失败: {result['message']}")

    return result["success"]


async def main():
    """运行测试"""
    print("=" * 60)
    print("图像生成大师 - 实际生成测试")
    print("=" * 60)
    print("\n⚠️  注意: 此测试会调用真实API并消耗额度")
    print("   按 Ctrl+C 取消\n")
    print("=" * 60 + "\n")

    try:
        # 测试柏拉图平台
        # blt_success = await test_blt_provider()

        # 测试 GrsAI 平台
        # grsai_success = await test_grsai_provider()

        # 测试自动选择
        # auto_success = await test_auto_provider()

        print("💡 提示: 取消注释上面的代码来运行实际测试")

    except KeyboardInterrupt:
        print("\n\n⚠️  测试已取消")
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
