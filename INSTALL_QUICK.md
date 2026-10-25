# 快速安装指南

## ❌ 遇到错误了？

如果你看到这个错误：
```
ERROR: Invalid requirement: '"""': Expected package name at the start of dependency specifier
```

说明使用了错误的 requirements 文件。

## ✅ 正确的安装方法

### 选项 1: 最简单 - 即用版本（推荐）

```bash
pip install -r requirements_ready.txt
```

### 选项 2: 完整版本

```bash
pip install -r requirements_clean.txt
```

### 选项 3: 使用原项目文件

```bash
pip install -r requirements.txt
```

### 选项 4: 手动安装核心依赖

```bash
# 1. PyTorch
pip install torch torchvision torchaudio

# 2. 音频处理
pip install librosa==0.10.2 soundfile==0.12.1 scipy==1.13.1 pydub==0.25.1

# 3. Transformers
pip install transformers==4.46.3 huggingface-hub

# 4. 其他核心
pip install accelerate numpy==1.26.4 einops==0.8.0 munch==4.0.0 tqdm pyyaml

# 5. 编解码
pip install descript-audio-codec==1.0.0

# 6. 模型库
pip install modelscope==1.18.1 funasr==1.1.5
```

## 📋 文件对比

| 文件名 | 用途 | 推荐 |
|--------|------|------|
| **requirements_ready.txt** | 即用版，最精简 | ⭐⭐⭐⭐⭐ |
| **requirements_clean.txt** | 完整功能版 | ⭐⭐⭐⭐ |
| **requirements.txt** | 原项目文件 | ⭐⭐⭐ |
| requirements_complete.txt | 带详细注释 | ⭐⭐⭐ |
| requirements_minimal.txt | 仅推理用 | ⭐⭐⭐ |

## 🚀 完整安装流程

```bash
# 1. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 2. 升级 pip
pip install --upgrade pip

# 3. 安装依赖（选择一个）
pip install -r requirements_ready.txt

# 4. 验证安装
python verify_installation.py

# 5. 测试转换
python test_conversion.py
```

## 🌍 国内用户加速

```bash
# 使用清华镜像
pip install -r requirements_ready.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或阿里镜像
pip install -r requirements_ready.txt -i https://mirrors.aliyun.com/pypi/simple/
```

## 🐛 常见问题

### Q: 哪个文件最好用？
**A:** 推荐使用 `requirements_ready.txt`，它最精简且经过优化。

### Q: 安装很慢怎么办？
**A:** 使用国内镜像源（见上方）。

### Q: 某个包安装失败？
**A:**
```bash
# 跳过失败的包，继续安装其他
pip install -r requirements_ready.txt --no-deps

# 然后单独安装失败的包
pip install <package-name>
```

### Q: PyTorch 要特定版本？
**A:**
```bash
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CPU only
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## ✅ 验证成功

运行验证脚本：
```bash
python verify_installation.py
```

看到这个就成功了：
```
✅ 所有必需依赖已正确安装，可以开始使用 Seed-VC!
```

## 📞 需要帮助？

- 详细安装指南: [INSTALLATION.md](INSTALLATION.md)
- 快速开始: [seed_vc_tools/QUICKSTART.md](seed_vc_tools/QUICKSTART.md)
- 验证脚本: `python verify_installation.py`

---

**推荐命令（一键安装）：**
```bash
pip install -r requirements_ready.txt && python verify_installation.py
```
