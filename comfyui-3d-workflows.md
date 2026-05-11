# ComfyUI 3D 游戏素材 & 动画影视制作完全指南

---

## 一、核心插件安装

### 必装节点包

| 插件 | ⭐ | 功能 | 安装 |
|------|----|------|------|
| **ComfyUI-3D-Pack** | 3.7k | 3D模型生成/编辑 (3DGS/NeRF/Mesh) | Manager搜索安装 |
| **AnimateDiff-Evolved** | 3.4k | 文/图→视频动画 | Manager |
| **VideoHelperSuite** | 1.6k | 视频加载/合成/输出 | Manager |
| **SUPIR** | 2.2k | 视频超分辨率 | Manager |
| **Frame-Interpolation** | 1k | AI补帧(RIFE/ FILM) | Manager |
| **ControlNet-Aux** | 必备 | Canny/Depth/OpenPose等预处理 | Manager |
| **IPAdapter Plus** | 必备 | 图像风格迁移/参考 | Manager |
| **Manager** | 必备 | 一键安装/管理所有节点 | 内置 |

### 一键安装命令

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/MrForExample/ComfyUI-3D-Pack
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
git clone https://github.com/Fannovel16/ComfyUI-Frame-Interpolation
git clone https://github.com/kijai/ComfyUI-SUPIR
cd ComfyUI-3D-Pack && pip install -r requirements.txt
# 下载模型到 ComfyUI/models/
# AnimateDiff模型: huggingface.co/guoyww/animatediff
# ControlNet模型: huggingface.co/lllyasviel/ControlNet-v1-1
```

---

## 二、3D 游戏素材生成工作流

### 2.1 单图→3D模型 (TripoSR / Zero123++)

```
工作流:
[Load Image] → [Remove BG] → [TripoSR/Zero123] → [3D Mesh Output]

节点链:
Image → Background Removal → TripoSR MultiView → Mesh Reconstruction → Save Mesh (OBJ/GLB)

输出: 带纹理的3D模型，可直接导入 Blender/Unity/Godot
```

**TripoSR 配置**:
- 输入: 512×512 白底物体图
- 贴图分辨率: 1024 (推荐) / 2048
- 多视角采样: 6视角 (前后左右上下)

### 2.2 PBR 材质生成

```
工作流:
[Load Image] → [IPAdapter] → [SDXL/SD3] → [PBR Material]

材质参数:
├── BaseColor: 固有色贴图
├── Normal: 法线贴图
├── Roughness: 粗糙度
└── Metallic: 金属度

Prompt: "seamless PBR material, tileable, diffuse map only, 
         stone texture, high quality, game ready"
```

### 2.3 角色概念→3D角色

```
角色立绘 → [ControlNet Depth] → [Multi-View Diffusion] 
         → [TripoSR per view] → [Mesh Fusion] → 完整3D角色

分步:
1. SD生成角色正面/背面/侧面三视图
2. 每视图TripoSR生成角度模型
3. 3D Pack合并为统一Mesh
4. Blender清理+绑定
```

### 2.4 批量道具/图标生成

```
[Text List] → [SDXL Batch] → [Background Remover] → [Auto Crop]
→ 道具贴图集 (Sprite Sheet)

示例Prompt:
"game item icon, top-down view, potion bottle, fantasy style, 
 white background, centered, game asset, 512x512"
```

---

## 三、动画制作工作流

### 3.1 AnimateDiff 文→视频

```
工作流:
[CLIP Text Encode] → [AnimateDiff Loader] → [KSampler] → [AnimateDiff Combine] → [VHS Video Combine]

关键节点:
├── AnimateDiff Loader: 加载运动模块 (mm_sd15_v2.safetensors)
├── AnimateDiff Context Options: 控制运动幅度(context_length=16)
├── AnimateDiff Sampler: 时域一致采样
└── VHS Video Combine: 合成视频输出

参数建议:
- 帧数: 16-32帧 (2-4秒@8fps)
- 分辨率: 512×512 或 768×512
- Context Length: 16 (平衡质量/显存)
- 运动强度: 0.8-1.2
```

### 3.2 图生视频 (SVD / Img2Vid)

```
[Load Image] → [SVD Loader] → [SVD Sampler] → [Video Combine]

SVD (Stable Video Diffusion):
- 输入: 单张起始帧
- 输出: 14/25帧视频 (576×1024)
- 运动程度: motion_bucket_id=127 (越大越剧烈)
- 帧率: 6-30 FPS
```

### 3.3 ControlNet 精确控制动画

```
[Reference Image] → [ControlNet Canny/Depth/OpenPose]
                   → [AnimateDiff] → 受控动画

ControlNet 类型:
├── Canny: 边缘控制 (建筑/场景)
├── Depth: 深度控制 (3D场景一致性)
├── OpenPose: 骨骼控制 (角色动作)
├── Lineart: 线稿控制 (动画风格)
└── Tile: 分块增强 (细节保持)
```

### 3.4 视频增强流程

```
生成视频(低分辨率512×512) → [SUPIR/ESRGAN Upscale] → [Frame Interpolation(RIFE)] 
→ 高分辨率+高帧率视频

效果:
- 512×512 → 2048×2048 (4倍放大)
- 8fps → 24fps (3倍插帧)
- 去噪+锐化+细节增强
```

---

## 四、游戏资产完整管线

### 4.1 角色管线

```
SD/SD3 生成角色概念
    ↓
Multi-View Diffusion 三视图
    ↓
TripoSR 3D重建
    ↓
Blender 清理+绑定
    ↓
AnimateDiff 生成角色动画预览
    ↓
导入游戏引擎
```

### 4.2 场景/建筑管线

```
SD生成场景概念图
    ↓
ControlNet Depth 提取深度图
    ↓
3D Pack Depth→Mesh 生成3D场景
    ↓
Blender 细化+贴图烘焙
    ↓
导入游戏引擎
```

### 4.3 UI/图标管线

```
SDXL批量生成UI元素
    ↓
Remove Background 去背景
    ↓
Auto Crop + Resize
    ↓
Sprite Atlas 打包
```

---

## 五、影视制作工作流

### 5.1 短片制作流程

```
1. 故事板生成: SD → 关键帧图像序列
2. 帧间动画: AnimateDiff → 场景动画片段
3. 角色动画: ControlNet OpenPose → 角色动作
4. 视频合成: VHS → 片段拼接
5. 增强: SUPIR放大 + RIFE补帧 + 调色
```

### 5.2 风格迁移

```
实拍视频 → [ControlNet Canny/Depth] → [IPAdapter] → 风格化视频

应用:
- 真人→动画风格
- 现代→赛博朋克
- 白天→夜晚
- 手绘风格转换
```

### 5.3 口型同步

```
[音频] → [Whisper 转文本] → [文字驱动面部动画] → 叠加到角色视频

工具: SadTalker, Wav2Lip (ComfyUI节点)
```

---

## 六、关键参数速查

### SD模型选择

| 用途 | 推荐模型 | 分辨率 |
|------|---------|--------|
| 角色概念 | SDXL / SD3 | 1024×1024 |
| 3D转纹理 | SD1.5 + ControlNet | 512×512 |
| 动画 | SD1.5动画微调模型 | 512×512 |
| 道具/图标 | SDXL | 1024×1024 |
| PBR材质 | SD2.1 深度模型 | 512×512 |

### 显存管理

| 操作 | 显存占用 | 建议 |
|------|---------|------|
| SD1.5+AnimateDiff(16帧) | ~8GB | RTX 3070+ |
| SDXL | ~12GB | RTX 4070+ |
| TripoSR | ~4GB | 6GB+ |
| SUPIR 4x放大 | ~10GB | 12GB+ |
| Frame Interpolation | ~2GB | 任何 |

---

## 七、工作流模板结构

```
ComfyUI 控制台 → 加载 Workflow JSON

游戏角色工作流:
[Text] → [CLIP] → [SDXL] → [BgRemove] → [TripoSR] → [Mesh Save]

游戏动画工作流:
[Image] → [AnimateDiff] → [ControlNet] → [Video Out]

影视制作工作流:
[Video Load] → [ControlNet] → [IPAdapter] → [SUPIR] → [RIFE] → [Video Save]
```

---

*基于 2026-05-11 GitHub 最新数据*
