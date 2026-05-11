# AI 绘画与模型微调高级技术

---

## 一、LoRA 训练完全指南

### 1.1 LoRA 原理

```
原始权重矩阵 W (d×k)
LoRA分解: W' = W + B×A
其中B(d×r), A(r×k), r<<min(d,k)

参数量: d×k → r×(d+k)，通常减少99%+
```

### 1.2 Kohya SS 训练流程

```bash
# 环境
pip install torch torchvision xformers
git clone https://github.com/bmaltais/kohya_ss
cd kohya_ss && pip install -r requirements.txt

# 数据集准备
dataset/
├── 10_luna/           # 10张重复训练
│   ├── img001.png
│   └── img001.txt     # 标签文件(可选)
└── 5_style/           # 5张风格参考
```

**关键参数**:
| 参数 | 推荐值 | 说明 |
|------|--------|------|
| Network Rank (r) | 8-32 | 越高越精细,越大 |
| Network Alpha | rank/2 或 rank | 学习率缩放 |
| Learning Rate | 5e-5 ~ 1e-4 | SDXL用更低 |
| Batch Size | 1-4 | 显存限制 |
| Epochs | 5-20 | 10张图×10epoch=100步 |
| Resolution | 512(SD1.5)/1024(SDXL) | 匹配基模型 |
| Optimizer | AdamW8bit/DAdaptation | 8bit省显存 |

### 1.3 训练数据口诀

```
质量>数量: 10张高质量 > 100张低质量
多样性: 不同角度/光照/表情/背景
一致性: 同一角色/风格
分辨率: 训练分辨率 = 推理分辨率
标注: 触发词 + 详细描述
```

---

## 二、Stable Diffusion 生态

### 2.1 模型版本演进

| 模型 | 分辨率 | 参数量 | 特点 |
|------|--------|--------|------|
| SD1.5 | 512 | 860M | 生态最丰富,ControlNet完善 |
| SD2.1 | 768 | 860M | 深度图强,但社区不如1.5 |
| SDXL | 1024 | 2.6B | 细节更好,双CLIP |
| SD3/3.5 | 1024 | 8B | MMDiT架构,文字理解飞跃 |
| Flux.1 | 1024 | 12B | 文字/手指质量天花板 |
| SD3.5 Large | 1024 | 8B | 开源,宽松许可 |

### 2.2 ControlNet 全家桶

| ControlNet | 输入 | 控制内容 | 应用 |
|-----------|------|---------|------|
| **Canny** | 边缘图 | 结构/轮廓 | 线稿上色,风格迁移 |
| **Depth** | 深度图 | 空间关系 | 3D场景一致,pose迁移 |
| **OpenPose** | 骨骼 | 人体姿态 | 角色动作控制 |
| **IPAdapter** | 参考图 | 风格/人脸 | 角色一致性 |
| **Tile** | 分块 | 细节增强 | 放大时保持细节 |
| **Lineart** | 线稿 | 精确线条 | 动漫上色 |
| **Inpaint** | 遮罩 | 局部重绘 | 修复/换装/换背景 |
| **Shuffle** | 随机种子 | 构图迁移 | 参考构图重生成 |
| **Reference** | 参考图 | 整体风格 | 类似图生成 |
| **InstantID** | 人脸图 | 人脸保持 | 角色一致性最优 |

---

## 三、视频生成

### 3.1 主流视频模型

| 模型 | 时长 | 分辨率 | 开源 | 显存 |
|------|------|--------|------|------|
| AnimateDiff | 16-32帧 | 512 | ✅ | 8GB |
| SVD | 14-25帧 | 576×1024 | ✅ | 16GB |
| I2VGen-XL | 16帧 | 768 | ✅ | 16GB |
| CogVideoX | 6秒 | 720×480 | ✅ | 20GB |
| Sora(OpenAI) | 60秒 | 1080p | ❌ | API |
| Kling | 10秒 | 1080p | ❌ | API |
| Runway Gen-3 | 10秒 | 1080p | ❌ | Web |

### 3.2 视频生成 ComfyUI 工作流

```
文→视频: [CLIP] → [AnimateDiff Loader] → [KSampler] → [AnimateDiff Combine] → [Video Out]

图→视频: [Load Image] → [SVD Loader] → [SVD Sampler] → [Frame Interpolation(RIFE)] → [Video Out]

增强: [SUPIR Upscale] → [FILM Frame Interpolation] → 4K 60fps
```

---

## 四、AI 3D 生成

### 4.1 图像→3D

| 模型 | 速度 | 质量 | 格式 |
|------|------|------|------|
| TripoSR | 0.5秒 | ⭐⭐⭐ | GLB |
| Zero123++ | 30秒 | ⭐⭐⭐⭐ | 多视角图 |
| LGM | 5秒 | ⭐⭐⭐⭐ | 高斯泼溅 |
| InstantMesh | 1秒 | ⭐⭐⭐ | Mesh |
| Stable Zero123 | 60秒 | ⭐⭐⭐⭐ | 多视角图 |
| Unique3D | 30秒 | ⭐⭐⭐⭐⭐ | 高精度Mesh |

### 4.2 工作流

```
[Load Image] → [Remove BG] → [TripoSR] → [Save Mesh GLB]
    ↓ 或
[Load Image] → [Zero123++] → [Multi-View Images] → [3D Reconstruction]
    ↓ 导入
Blender → 清理/绑定/动画 → 游戏引擎
```

---

## 五、Stable Diffusion 在游戏中的应用

### 5.1 资产生成管线

```
概念图:   SDXL + 风格LoRA → 角色概念/场景概念
图标:     SD1.5 + 白底LoRA → 批量道具图标
背景:     SDXL + ControlNet Depth → 无缝场景
UI:       SD1.5 + 特定Prompt → 按钮/边框/面板
纹理:     SD2.1 Deep模型 → 法线+高度+粗糙度贴图
精灵帧:   AnimateDiff + ControlNet → 角色动画帧序列
```

### 5.2 必装模型推荐

```
基础:
  AnythingV5 — 动漫风格天花板
  CounterfeitV3 — 精致二次元
  DreamShaper XL — 写实/半写实
  
LoRA:
  Detail Tweaker — 增强细节
  Add More Details — 增加复杂度
  epi_noiseoffset — 改善光照
  
ControlNet:
  Canny + Depth + OpenPose + IPAdapter (四件套)
```

---

## 六、资源索引

| 平台 | URL |
|------|-----|
| CivitAI | civitai.com — 最大模型/LoRA社区 |
| HuggingFace | huggingface.co — 模型托管 |
| Kohya SS | github.com/bmaltais/kohya_ss |
| ComfyUI | github.com/comfyanonymous/ComfyUI |
| ControlNet | github.com/lllyasviel/ControlNet |
| AnimateDiff | github.com/guoyww/animatediff |
| TripoSR | huggingface.co/stabilityai/TripoSR |
