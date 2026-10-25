#!/usr/bin/env python3
"""
快速批量转换 JSUT 数据集 - 模型只加载一次
"""

import os
import sys
import time
from pathlib import Path
from tqdm import tqdm

# 添加项目路径
sys.path.insert(0, '/Users/rgwei/pj/pj_audio/seed-vc')

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
    print("Seed-VC 快速批量音色转换 - JSUT 数据集")
    print("=" * 70)
    print()

    # 检查路径
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ 错误: 源目录不存在: {SOURCE_DIR}")
        return 1

    if not os.path.exists(TARGET_AUDIO):
        print(f"❌ 错误: 参考音频不存在: {TARGET_AUDIO}")
        return 1

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
    print("正在加载模型...")
    print()

    # 导入必要模块
    try:
        import torch
        import torchaudio
        import librosa
        import warnings
        warnings.filterwarnings('ignore')

        from inference import load_models

        # 创建参数对象
        class Args:
            def __init__(self):
                self.f0_condition = F0_CONDITION
                self.checkpoint = None
                self.config = None
                self.fp16 = FP16

        args = Args()

        # 加载模型（只加载一次）
        print("⏳ 加载模型中...")
        model, semantic_fn, f0_fn, vocoder_fn, campplus_model, to_mel, mel_fn_args = load_models(args)
        sr = mel_fn_args['sampling_rate']
        print("✓ 模型加载完成!")
        print()

    except Exception as e:
        print(f"❌ 模型加载失败: {str(e)}")
        return 1

    # 统计变量
    success_count = 0
    failed_count = 0
    skipped_count = 0
    start_time = time.time()

    print("=" * 70)
    print("开始转换...")
    print("=" * 70)
    print()

    # 加载目标音色一次
    try:
        print("⏳ 加载参考音色...")
        ref_audio = librosa.load(TARGET_AUDIO, sr=sr)[0]
        ref_audio_tensor = torch.tensor(ref_audio[:sr * 25]).unsqueeze(0).float()

        # 设备选择
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
        else:
            device = torch.device("cpu")

        ref_audio_tensor = ref_audio_tensor.to(device)
        print(f"✓ 参考音色加载完成 (设备: {device})")
        print()

    except Exception as e:
        print(f"❌ 参考音色加载失败: {str(e)}")
        return 1

    # 处理每个文件
    for idx, source_file in enumerate(tqdm(wav_files, desc="转换进度"), 1):
        source_name = source_file.stem
        output_name = f"{source_name}_converted.wav"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        # 检查是否已存在
        if os.path.exists(output_path):
            skipped_count += 1
            continue

        try:
            # 加载源音频
            source_audio = librosa.load(str(source_file), sr=sr)[0]
            source_audio_tensor = torch.tensor(source_audio).unsqueeze(0).float().to(device)

            # 重采样到 16kHz
            source_16k = torchaudio.functional.resample(source_audio_tensor, sr, 16000)
            ref_16k = torchaudio.functional.resample(ref_audio_tensor, sr, 16000)

            # 提取语义特征
            S_source = semantic_fn(source_16k)
            S_ref = semantic_fn(ref_16k)

            # 计算梅尔频谱
            mel_source = to_mel(source_audio_tensor)
            mel_ref = to_mel(ref_audio_tensor)

            # 提取音色特征
            feat_ref = torchaudio.compliance.kaldi.fbank(
                ref_16k,
                num_mel_bins=80,
                dither=0,
                sample_frequency=16000
            )
            feat_ref = feat_ref - feat_ref.mean(dim=0, keepdim=True)
            style_ref = campplus_model(feat_ref.unsqueeze(0))

            # 长度调节
            target_lengths = torch.LongTensor([int(mel_source.size(2) * LENGTH_ADJUST)]).to(device)
            target_ref_lengths = torch.LongTensor([mel_ref.size(2)]).to(device)

            cond, _, _, _, _ = model.length_regulator(
                S_source, ylens=target_lengths, n_quantizers=3, f0=None
            )
            prompt_cond, _, _, _, _ = model.length_regulator(
                S_ref, ylens=target_ref_lengths, n_quantizers=3, f0=None
            )

            # 拼接条件
            cat_condition = torch.cat([prompt_cond, cond], dim=1)

            # 扩散生成
            with torch.autocast(device_type=device.type, dtype=torch.float16 if FP16 else torch.float32):
                vc_target = model.cfm.inference(
                    cat_condition,
                    torch.LongTensor([cat_condition.size(1)]).to(device),
                    mel_ref, style_ref, None, DIFFUSION_STEPS,
                    inference_cfg_rate=CFG_RATE
                )
                vc_target = vc_target[:, :, mel_ref.size(-1):]

            # 声码器生成音频
            vc_wave = vocoder_fn(vc_target.float())[0]

            # 保存
            torchaudio.save(output_path, vc_wave.cpu(), sr)

            success_count += 1

        except Exception as e:
            tqdm.write(f"[{idx}/{total_files}] ✗ 失败: {source_name} - {str(e)[:50]}")
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
