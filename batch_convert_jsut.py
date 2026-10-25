#!/usr/bin/env python3
"""
批量转换 JSUT 数据集到指定音色
"""

import os
import sys
import subprocess
from pathlib import Path
from tqdm import tqdm
import time

# 配置参数
SOURCE_DIR = "/Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav"
TARGET_AUDIO = "/Users/rgwei/pj/pj_audio/seed-vc/seed_vc_tools/refer_audio/ninja.mp3"
OUTPUT_DIR = "/Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav_new"

# 转换参数
DIFFUSION_STEPS = 30
LENGTH_ADJUST = 1.0
CFG_RATE = 0.7
F0_CONDITION = False
FP16 = True

def main():
    """主函数"""
    print("=" * 70)
    print("Seed-VC 批量音色转换 - JSUT 数据集")
    print("=" * 70)
    print()

    # 检查路径
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ 错误: 源目录不存在: {SOURCE_DIR}")
        sys.exit(1)

    if not os.path.exists(TARGET_AUDIO):
        print(f"❌ 错误: 参考音频不存在: {TARGET_AUDIO}")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 获取所有 WAV 文件
    wav_files = sorted(list(Path(SOURCE_DIR).glob("*.wav")))
    total_files = len(wav_files)

    print(f"📁 源目录: {SOURCE_DIR}")
    print(f"🎤 参考音色: {TARGET_AUDIO}")
    print(f"📂 输出目录: {OUTPUT_DIR}")
    print(f"📊 文件数量: {total_files} 个")
    print(f"⚙️  参数配置:")
    print(f"   - diffusion_steps: {DIFFUSION_STEPS}")
    print(f"   - cfg_rate: {CFG_RATE}")
    print(f"   - length_adjust: {LENGTH_ADJUST}")
    print(f"   - f0_condition: {F0_CONDITION}")
    print(f"   - fp16: {FP16}")
    print()
    print("=" * 70)
    print()

    # 统计变量
    success_count = 0
    failed_count = 0
    skipped_count = 0
    start_time = time.time()

    # 处理每个文件
    for idx, source_file in enumerate(tqdm(wav_files, desc="转换进度"), 1):
        source_name = source_file.stem
        output_name = f"{source_name}_converted.wav"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        # 检查是否已存在
        if os.path.exists(output_path):
            tqdm.write(f"[{idx}/{total_files}] ⊘ 跳过 (已存在): {source_name}")
            skipped_count += 1
            continue

        try:
            # 构建命令
            cmd = [
                "python", "inference.py",
                "--source", str(source_file),
                "--target", TARGET_AUDIO,
                "--output", OUTPUT_DIR,
                "--diffusion-steps", str(DIFFUSION_STEPS),
                "--length-adjust", str(LENGTH_ADJUST),
                "--inference-cfg-rate", str(CFG_RATE),
                "--f0-condition", str(F0_CONDITION),
                "--fp16", str(FP16),
            ]

            # 执行转换
            result = subprocess.run(
                cmd,
                cwd="/Users/rgwei/pj/pj_audio/seed-vc",
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                # 检查输出文件是否生成
                # inference.py 会生成特定格式的文件名
                generated_files = list(Path(OUTPUT_DIR).glob(f"vc_{source_name}_*"))
                if generated_files:
                    # 重命名为标准格式
                    os.rename(generated_files[0], output_path)
                    tqdm.write(f"[{idx}/{total_files}] ✓ 成功: {source_name}")
                    success_count += 1
                else:
                    tqdm.write(f"[{idx}/{total_files}] ✗ 失败: {source_name} (未生成输出)")
                    failed_count += 1
            else:
                error_msg = result.stderr[:100] if result.stderr else "未知错误"
                tqdm.write(f"[{idx}/{total_files}] ✗ 失败: {source_name} - {error_msg}")
                failed_count += 1

        except subprocess.TimeoutExpired:
            tqdm.write(f"[{idx}/{total_files}] ✗ 超时: {source_name}")
            failed_count += 1
        except Exception as e:
            tqdm.write(f"[{idx}/{total_files}] ✗ 错误: {source_name} - {str(e)}")
            failed_count += 1

    # 输出统计结果
    elapsed_time = time.time() - start_time

    print()
    print("=" * 70)
    print("转换完成!")
    print("=" * 70)
    print(f"✓ 成功: {success_count} 个")
    print(f"✗ 失败: {failed_count} 个")
    print(f"⊘ 跳过: {skipped_count} 个")
    print(f"━ 总计: {total_files} 个")
    print(f"⏱  总耗时: {elapsed_time / 60:.1f} 分钟")
    if success_count > 0:
        print(f"⚡ 平均速度: {elapsed_time / success_count:.1f} 秒/文件")
    print("=" * 70)

    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
