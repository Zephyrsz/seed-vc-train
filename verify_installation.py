#!/usr/bin/env python3
"""
验证 Seed-VC 依赖安装
"""

import sys
from importlib.metadata import version, PackageNotFoundError

# 必需的包
REQUIRED_PACKAGES = {
    'torch': '核心深度学习框架',
    'torchaudio': '音频处理框架',
    'librosa': '音频分析库',
    'soundfile': '音频文件读写',
    'transformers': 'Transformer 模型',
    'accelerate': '训练加速',
    'einops': '张量操作',
    'pydub': '音频格式转换',
    'numpy': '科学计算',
    'scipy': '科学计算',
}

# 可选的包
OPTIONAL_PACKAGES = {
    'gradio': 'Web UI',
    'sounddevice': '实时音频',
    'resemblyzer': '声音嵌入',
    'jiwer': '评估指标',
    'modelscope': '模型库',
}

def get_package_version(package_name):
    """获取包版本"""
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None

def check_package(package_name, description):
    """检查单个包"""
    ver = get_package_version(package_name)
    if ver:
        print(f"  ✓ {package_name:20s} {ver:15s} - {description}")
        return True
    else:
        print(f"  ✗ {package_name:20s} {'未安装':15s} - {description}")
        return False

def main():
    """主函数"""
    print("=" * 80)
    print("Seed-VC 依赖验证")
    print("=" * 80)
    print()

    # 检查 Python 版本
    py_version = sys.version.split()[0]
    print(f"Python 版本: {py_version}")

    py_major, py_minor = sys.version_info[:2]
    if py_major == 3 and 8 <= py_minor <= 11:
        print("  ✓ Python 版本符合要求 (3.8-3.11)")
    else:
        print("  ⚠️  Python 版本不在推荐范围 (3.8-3.11)")
    print()

    # 检查必需包
    print("必需的包:")
    print("-" * 80)
    required_ok = 0
    required_total = len(REQUIRED_PACKAGES)

    for package, desc in REQUIRED_PACKAGES.items():
        if check_package(package, desc):
            required_ok += 1

    print()
    print(f"必需包: {required_ok}/{required_total} 安装")
    print()

    # 检查可选包
    print("可选的包:")
    print("-" * 80)
    optional_ok = 0
    optional_total = len(OPTIONAL_PACKAGES)

    for package, desc in OPTIONAL_PACKAGES.items():
        if check_package(package, desc):
            optional_ok += 1

    print()
    print(f"可选包: {optional_ok}/{optional_total} 安装")
    print()

    # 检查 PyTorch 和设备
    print("=" * 80)
    print("设备信息:")
    print("-" * 80)

    try:
        import torch

        print(f"PyTorch 版本: {torch.__version__}")
        print()

        # CUDA
        cuda_available = torch.cuda.is_available()
        print(f"CUDA 可用: {cuda_available}")
        if cuda_available:
            print(f"  CUDA 版本: {torch.version.cuda}")
            print(f"  cuDNN 版本: {torch.backends.cudnn.version()}")
            print(f"  GPU 数量: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
                props = torch.cuda.get_device_properties(i)
                print(f"    显存: {props.total_memory / 1e9:.1f} GB")

        # MPS (Mac)
        mps_available = torch.backends.mps.is_available()
        print(f"MPS 可用 (Mac): {mps_available}")

        # CPU
        print(f"CPU 线程数: {torch.get_num_threads()}")

        # 推荐设备
        if cuda_available:
            device = "cuda"
            device_name = torch.cuda.get_device_name(0)
        elif mps_available:
            device = "mps"
            device_name = "Apple Silicon"
        else:
            device = "cpu"
            device_name = "CPU"

        print()
        print(f"✓ 推荐使用设备: {device} ({device_name})")

    except ImportError:
        print("✗ PyTorch 未安装")
        print()

    print("=" * 80)

    # 测试基本功能
    print()
    print("基本功能测试:")
    print("-" * 80)

    all_tests_passed = True

    # 测试音频加载
    try:
        import librosa
        import numpy as np

        # 创建测试音频
        test_audio = np.random.randn(16000)

        print("  ✓ Librosa 音频处理")
    except Exception as e:
        print(f"  ✗ Librosa 测试失败: {str(e)}")
        all_tests_passed = False

    # 测试 Transformers
    try:
        from transformers import AutoFeatureExtractor
        print("  ✓ Transformers 模型加载")
    except Exception as e:
        print(f"  ✗ Transformers 测试失败: {str(e)}")
        all_tests_passed = False

    # 测试 PyTorch
    try:
        import torch
        test_tensor = torch.randn(2, 3)
        print("  ✓ PyTorch 张量操作")
    except Exception as e:
        print(f"  ✗ PyTorch 测试失败: {str(e)}")
        all_tests_passed = False

    print()
    print("=" * 80)

    # 最终结果
    print()
    if required_ok == required_total and all_tests_passed:
        print("✅ 所有必需依赖已正确安装，可以开始使用 Seed-VC!")
        print()
        print("下一步:")
        print("  1. 测试单文件转换: python test_conversion.py")
        print("  2. 批量转换: python batch_convert_jsut_fast.py")
        print("  3. 查看文档: seed_vc_tools/QUICKSTART.md")
        return 0
    else:
        print("❌ 部分依赖缺失或测试失败")
        print()
        if required_ok < required_total:
            print(f"缺少 {required_total - required_ok} 个必需的包，请运行:")
            print("  pip install -r requirements_complete.txt")
        print()
        print("如需帮助，请查看: INSTALLATION.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
