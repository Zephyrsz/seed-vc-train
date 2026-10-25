# Seed-VC 安装指南

## 📋 系统要求

### 最低配置
- **Python**: 3.8 - 3.11 (推荐 3.10)
- **内存**: 8GB RAM
- **存储**: 10GB 可用空间 (模型缓存)

### 推荐配置
- **Python**: 3.10
- **内存**: 16GB+ RAM
- **GPU**: NVIDIA GPU (6GB+ VRAM) 或 Mac M 系列
- **存储**: 20GB+ 可用空间

## 🚀 快速安装

### 方式 1: CUDA GPU (NVIDIA)

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements_complete.txt
```

### 方式 2: Mac M 系列 (Apple Silicon)

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements_complete_mac.txt
```

### 方式 3: 仅推理 (精简版)

```bash
pip install -r requirements_minimal.txt
```

### 方式 4: CPU Only

```bash
# 先编辑 requirements_complete.txt
# 删除或注释掉包含 --extra-index-url 的行

pip install -r requirements_complete.txt
```

## 📦 依赖文件说明

| 文件 | 用途 | 包含内容 |
|-----|------|---------|
| **requirements_complete.txt** | 完整功能 (CUDA) | 训练、推理、评估、GUI |
| **requirements_complete_mac.txt** | 完整功能 (Mac) | 适配 Apple Silicon |
| **requirements_minimal.txt** | 仅推理 | 最小依赖，只做推理 |
| requirements.txt | 原始依赖 | 项目原始文件 |
| requirements-mac.txt | 原始 Mac 依赖 | 项目原始文件 |

## 🔧 详细安装步骤

### Step 1: 安装系统依赖

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    ffmpeg \
    libsndfile1 \
    portaudio19-dev
```

#### macOS
```bash
# 安装 Homebrew (如果没有)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装依赖
brew install ffmpeg portaudio
```

#### Windows
```powershell
# 安装 ffmpeg
# 下载: https://www.gyan.dev/ffmpeg/builds/
# 添加到 PATH 环境变量
```

### Step 2: 创建 Python 环境

#### 使用 venv (推荐)
```bash
python -m venv seed-vc-env
source seed-vc-env/bin/activate  # Linux/Mac
# 或
seed-vc-env\Scripts\activate  # Windows
```

#### 使用 Conda
```bash
conda create -n seed-vc python=3.10
conda activate seed-vc
```

### Step 3: 安装 PyTorch

#### CUDA 11.8
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### CUDA 12.1
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### Mac (MPS)
```bash
pip install torch torchvision torchaudio
```

#### CPU Only
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Step 4: 安装其他依赖

```bash
pip install -r requirements_complete.txt
```

### Step 5: 验证安装

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
python -c "import librosa; print(f'Librosa: {librosa.__version__}')"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
```

## 🌍 国内镜像加速

### 使用清华镜像
```bash
pip install -r requirements_complete.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 使用阿里镜像
```bash
pip install -r requirements_complete.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 永久配置镜像
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 🐛 常见问题

### Q1: torch 安装失败
**A:**
```bash
# 先单独安装 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 再安装其他依赖 (跳过 torch)
pip install -r requirements_complete.txt --no-deps
pip install <其他包>
```

### Q2: soundfile 或 librosa 安装失败
**A:**
```bash
# Ubuntu/Debian
sudo apt-get install libsndfile1

# macOS
brew install libsndfile

# Windows: 下载预编译的轮子
pip install soundfile --only-binary :all:
```

### Q3: CUDA 版本不匹配
**A:**
```bash
# 检查 CUDA 版本
nvidia-smi

# 安装对应版本的 PyTorch
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Q4: Mac M 系列安装问题
**A:**
```bash
# 确保使用 ARM 原生 Python
which python
# 应该显示 /opt/homebrew/bin/python 或类似路径

# 如果不是，重新安装 Homebrew Python
brew install python@3.10

# 使用正确的 Python 创建环境
/opt/homebrew/bin/python3.10 -m venv venv
source venv/bin/activate
```

### Q5: 内存不足
**A:**
```bash
# 分批安装
pip install torch torchvision torchaudio
pip install transformers huggingface-hub
pip install librosa soundfile scipy
pip install -r requirements_complete.txt
```

### Q6: pyaudio 安装失败 (Mac)
**A:**
```bash
# 先安装 portaudio
brew install portaudio

# 指定路径安装
CFLAGS="-I/opt/homebrew/include" LDFLAGS="-L/opt/homebrew/lib" pip install pyaudio
```

## 🔍 验证完整性

运行以下脚本验证所有依赖是否正确安装：

```python
# verify_installation.py
import sys

required_packages = [
    'torch',
    'torchaudio',
    'librosa',
    'soundfile',
    'transformers',
    'accelerate',
    'einops',
    'gradio',
    'pydub',
]

print("=" * 60)
print("验证 Seed-VC 依赖安装")
print("=" * 60)

all_good = True
for package in required_packages:
    try:
        module = __import__(package)
        version = getattr(module, '__version__', 'unknown')
        print(f"✓ {package:20s} {version}")
    except ImportError:
        print(f"✗ {package:20s} 未安装")
        all_good = False

print("=" * 60)

# 检查设备
import torch
print(f"\n设备信息:")
print(f"  CUDA 可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"  CUDA 版本: {torch.version.cuda}")
    print(f"  GPU 数量: {torch.cuda.device_count()}")
    print(f"  GPU 名称: {torch.cuda.get_device_name(0)}")
print(f"  MPS 可用: {torch.backends.mps.is_available()}")

print("=" * 60)

if all_good:
    print("✅ 所有依赖安装成功!")
else:
    print("❌ 部分依赖缺失，请检查上述输出")
    sys.exit(1)
```

运行验证：
```bash
python verify_installation.py
```

## 📚 更多资源

- **项目文档**: [README.md](README.md)
- **快速开始**: [seed_vc_tools/QUICKSTART.md](seed_vc_tools/QUICKSTART.md)
- **架构详解**: [seed_vc_tools/ARCHITECTURE.md](seed_vc_tools/ARCHITECTURE.md)
- **原项目**: [Seed-VC GitHub](https://github.com/Plachtaa/seed-vc)

## 💡 推荐安装流程

**完整安装 (GPU)**:
```bash
# 1. 系统依赖
sudo apt-get install ffmpeg libsndfile1 portaudio19-dev

# 2. 创建环境
python -m venv venv
source venv/bin/activate

# 3. 安装 PyTorch (CUDA 12.1)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4. 安装其他依赖
pip install -r requirements_complete.txt

# 5. 验证
python verify_installation.py

# 6. 测试转换
python test_conversion.py
```

**精简安装 (仅推理)**:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements_minimal.txt
python test_conversion.py
```

---

安装成功后，就可以开始使用 Seed-VC 进行语音转换了！
