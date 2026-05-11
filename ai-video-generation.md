# AI 视频生成模型完全指南

---

## 一、开源视频生成模型对比

| 模型 | 机构 | ⭐ | 时长 | 分辨率 | 显存 | 架构 |
|------|------|-----|------|--------|------|------|
| **Diffusers** | HuggingFace | 33.5k | — | — | — | 统一扩散框架 |
| **LTX-Video** | Lightricks | 10.2k | 5秒 | 768×512 | 12GB | DiT Transformer |
| **AnimateDiff** | 社区 | 10k+ | 16-32帧 | 512 | 8GB | SD + Motion Module |
| **SVD** | Stability AI | — | 14-25帧 | 576×1024 | 16GB | UNet 时空 |
| **CogVideoX** | 清华 | 8k+ | 6秒 | 720×480 | 20GB | 3D VAE + Transformer |
| **Mochi 1** | Genmo | — | 5秒 | 480p | 24GB+ | Asymmetric VAE |
| **Pyramid Flow** | 北大 | — | 10秒 | 768 | 16GB | 金字塔流匹配 |
| **Open-Sora** | 社区 | 20k+ | 16秒 | 512 | 24GB+ | 类Sora架构 |

## 二、LTX-Video 详解

**核心特点**：
- DiT (Diffusion Transformer) 架构，替代 UNet
- 支持文生视频 + 图生视频
- 5秒长视频，24fps
- 12GB显存即可运行
- ComfyUI原生支持

**ComfyUI 使用**:
```
[CLIP Text Encode] → [LTX-Video Loader] → [LTX-Video Sampler] → [VHS Video Combine]
```

## 三、视频生成技术路线

### UNet 路线 (AnimateDiff/SVD)
```
SD UNet + 时域注意力层 → 帧间一致性
优点: 生态成熟，ControlNet兼容
缺点: 显存随帧数增长
```

### DiT 路线 (LTX-Video/Sora)
```
纯Transformer处理时空patch
优点: 可扩展性强，理解力好
缺点: 训练成本高
```

### 3D VAE 路线 (CogVideoX)
```
3D卷积VAE压缩时空维度
优点: 压缩率高
缺点: 解码质量损失
```

## 四、视频后期增强管线

```
生成(512p低帧率)
    ↓
[SUPIR/RealESRGAN] 空间放大 → 1080p/4K
    ↓
[RIFE/FILM] 时域插帧 → 24/30/60fps
    ↓
[Color Grading] 调色 → 电影级
```

## 五、游戏开发中的应用

| 应用 | 方案 | 效果 |
|------|------|------|
| 过场动画 | LTX-Video + RIFE 补帧 | 低成本CG |
| 技能特效 | AnimateDiff + ControlNet | 粒子/魔法 |
| 环境氛围 | SVD img2vid | 动态背景 |
| 角色展示 | AnimateDiff + OpenPose | 360度展示 |
| UI动效 | AnimateDiff lite | 界面特效 |
