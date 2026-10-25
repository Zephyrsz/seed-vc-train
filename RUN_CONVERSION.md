# 批量转换 JSUT 数据集到 ninja 音色

## 📋 任务配置

- **参考音色**: `seed_vc_tools/refer_audio/ninja.mp3` (15.3秒)
- **源目录**: `/Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav`
- **输出目录**: `/Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav_new`
- **文件数量**: 5000 个 WAV 文件

## 🚀 执行方式

### 方式 1: 使用快速批量脚本（推荐，模型只加载一次）

```bash
cd /Users/rgwei/pj/pj_audio/seed-vc
python batch_convert_jsut_fast.py
```

**优点**：
- ✅ 模型只加载一次，速度最快
- ✅ 内存占用稳定
- ✅ 实时进度显示
- ✅ 自动跳过已转换文件

**预计时间**:
- GPU (CUDA): ~2-3 小时
- GPU (MPS): ~3-5 小时
- CPU: ~10-15 小时

---

### 方式 2: 使用标准批量脚本

```bash
cd /Users/rgwei/pj/pj_audio/seed-vc
python batch_convert_jsut.py
```

**特点**：
- 每个文件独立处理
- 更好的错误隔离
- 内存自动释放

---

### 方式 3: 使用 seed_vc_tools 工具包

```bash
cd /Users/rgwei/pj/pj_audio/seed-vc

python seed_vc_tools/scripts/batch_convert.py \
    --source-dir /Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav \
    --target seed_vc_tools/refer_audio/ninja.mp3 \
    --output-dir /Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav_new \
    --pattern "*.wav" \
    --diffusion-steps 30 \
    --cfg-rate 0.7 \
    --skip-existing
```

---

## ⚙️ 参数说明

当前配置：
- `diffusion_steps`: 30 (标准质量)
- `cfg_rate`: 0.7 (音色相似度控制)
- `length_adjust`: 1.0 (保持原速)
- `f0_condition`: False (普通语音转换)

### 如果需要调整：

**提高质量** (但速度变慢):
```python
DIFFUSION_STEPS = 40  # 从 30 改为 40
CFG_RATE = 0.8        # 从 0.7 改为 0.8
```

**加快速度** (但质量下降):
```python
DIFFUSION_STEPS = 20  # 从 30 改为 20
```

编辑对应的 Python 文件即可修改参数。

---

## 📊 预期结果

转换完成后，`wav_new` 目录将包含：
```
wav_new/
├── BASIC5000_0001_converted.wav
├── BASIC5000_0002_converted.wav
├── BASIC5000_0003_converted.wav
...
└── BASIC5000_5000_converted.wav
```

所有音频将转换为 ninja.mp3 的音色。

---

## 🔍 监控进度

### 查看实时进度
脚本会显示：
```
转换进度: 45%|████████████████              | 2250/5000 [1:23:45<1:32:15, 29.8it/s]
```

### 查看已完成数量
```bash
ls /Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav_new/*.wav | wc -l
```

### 中断后续继续
脚本会自动跳过已存在的文件，可以随时中断后重新运行。

---

## 🛠️ 故障排查

### 如果遇到 CUDA 内存不足
编辑脚本，降低批处理或使用 CPU：
```python
device = torch.device("cpu")  # 强制使用 CPU
```

### 如果某些文件失败
脚本会继续处理其他文件，失败的文件会记录在日志中。

### 检查输出质量
随机抽样检查几个文件：
```bash
# 播放原始文件
play /Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav/BASIC5000_0001.wav

# 播放转换后文件
play /Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav_new/BASIC5000_0001_converted.wav
```

---

## ⏱️ 时间估算

基于 5000 个文件：

| 设备 | 单文件耗时 | 总耗时估算 |
|-----|-----------|-----------|
| RTX 3090 | ~1-2秒 | 1.5-3 小时 |
| RTX 3060 | ~2-3秒 | 3-5 小时 |
| M1/M2 Mac | ~3-5秒 | 4-7 小时 |
| CPU (16核) | ~10-15秒 | 14-20 小时 |

---

## 📝 完成后检查

```bash
# 统计转换成功数量
echo "转换成功: $(ls /Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav_new/*.wav 2>/dev/null | wc -l) / 5000"

# 检查文件大小合理性
du -sh /Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav_new/

# 随机抽样播放检查质量
ls /Users/rgwei/pj/datasets/tr_datasets/jp_audio_train/jsut_ver1.1/basic5000/wav_new/*.wav | shuf | head -5
```

---

## 🎯 推荐执行步骤

1. **先测试小批量** (确认质量)：
   ```bash
   # 只转换前 10 个文件测试
   # 修改脚本中的 wav_files[:10]
   ```

2. **确认质量满意后，执行全量转换**：
   ```bash
   python batch_convert_jsut_fast.py
   ```

3. **挂后台运行** (长时间任务):
   ```bash
   nohup python batch_convert_jsut_fast.py > conversion.log 2>&1 &

   # 查看进度
   tail -f conversion.log
   ```

---

## 📞 需要帮助？

- 查看详细架构: `seed_vc_tools/ARCHITECTURE.md`
- 参数调优指南: `seed_vc_tools/README.md`
- 常见问题: `seed_vc_tools/QUICKSTART.md`
