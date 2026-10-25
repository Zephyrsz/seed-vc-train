#!/usr/bin/env python3
"""
测试单个文件转换 - 验证配置
"""

import os
import sys

# 添加项目路径
sys.path.insert(0, '/Users/rgwei/pj/pj_audio/seed-vc')

# 配置参数
SOURCE_FILE = "/Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav/BASIC5000_0001.wav"
TARGET_AUDIO = "/Users/rgwei/pj/pj_audio/seed-vc/seed_vc_tools/refer_audio/ninja.mp3"
OUTPUT_DIR = "/Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav_new"

print("=" * 70)
print("Seed-VC 单文件转换测试")
print("=" * 70)
print()

# 检查文件
print("📝 检查输入文件...")
print(f"  源文件: {SOURCE_FILE}")
print(f"  存在: {os.path.exists(SOURCE_FILE)}")
print(f"  参考音色: {TARGET_AUDIO}")
print(f"  存在: {os.path.exists(TARGET_AUDIO)}")
print()

if not os.path.exists(SOURCE_FILE):
    print("❌ 源文件不存在!")
    sys.exit(1)

if not os.path.exists(TARGET_AUDIO):
    print("❌ 参考音频不存在!")
    sys.exit(1)

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"📂 输出目录: {OUTPUT_DIR}")
print()

# 测试转换
print("⏳ 开始转换测试...")
print()

try:
    from inference import main as inference_main

    class Args:
        def __init__(self):
            self.source = SOURCE_FILE
            self.target = TARGET_AUDIO
            self.output = OUTPUT_DIR
            self.diffusion_steps = 30
            self.length_adjust = 1.0
            self.inference_cfg_rate = 0.7
            self.f0_condition = False
            self.auto_f0_adjust = False
            self.semi_tone_shift = 0
            self.checkpoint = None
            self.config = None
            self.fp16 = True

    args = Args()
    inference_main(args)

    print()
    print("=" * 70)
    print("✅ 转换测试成功!")
    print("=" * 70)
    print()
    print("请检查输出文件:")
    print(f"  {OUTPUT_DIR}/")
    print()
    print("如果质量满意，可以运行批量转换:")
    print("  python batch_convert_jsut_fast.py")
    print()

except Exception as e:
    print()
    print("=" * 70)
    print("❌ 转换失败!")
    print("=" * 70)
    print(f"错误: {str(e)}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)
