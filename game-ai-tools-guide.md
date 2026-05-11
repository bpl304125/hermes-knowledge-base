# 游戏 AI 工具集成指南 — DeepMotion / Suno / Stable Audio / ElevenLabs

---

## 一、DeepMotion — 视频转 3D 动画

### 1.1 概览
视频/摄像头 → AI 分析人体姿态 → 输出 3D 骨骼动画 (FBX/BVH/GLB)

### 1.2 接入流程

```bash
# 1. 注册 https://deepmotion.com
# 2. 获取 API Key (Dashboard → Settings → API)

API_KEY="your_api_key"
API_URL="https://api.deepmotion.com/v1"

# 3. 上传视频生成动画
curl -X POST "$API_URL/animate" \
  -H "Authorization: Bearer $API_KEY" \
  -F "video=@my_dance.mp4" \
  -F "format=fbx" \
  -F "smoothing=medium"

# 4. 下载结果 → 导入 Blender/Unity/Godot
```

### 1.3 工作流集成

```
手机拍摄动作 → DeepMotion 生成动画 → FBX 下载
                                           ↓
                                    Blender 清理/循环编辑
                                           ↓
                                    Unity/Godot 导入动画控制器
                                           ↓
                                    游戏角色播放
```

### 1.4 免费替代方案

| 工具 | 方式 | 输出 | 限制 |
|------|------|------|------|
| Plask | 视频→3D | FBX/GLB | 免费层每月60秒 |
| Rokoko Vision | 单摄像头 | FBX/BVH | 免费 |
| Move.ai | 多手机 | FBX/BVH | 有限免费 |
| Mixamo | 手动上传角色 | 自动绑定+动画 | Adobe账号免费 |

### 1.5 动画文件格式转换

```bash
# FBX → GLTF (Blender Python)
blender --background --python - << 'EOF'
import bpy
bpy.ops.import_scene.fbx(filepath="animation.fbx")
bpy.ops.export_scene.gltf(filepath="animation.glb")
EOF

# BVH → FBX (用 Blender)
# 在线: https://vrm.dev 等转换工具
```

---

## 二、Suno — AI 音乐生成

### 2.1 接入方式

```
方式1: Web界面 (suno.com) — 最快
方式2: API (suno-api 第三方) — 可编程
方式3: 开源客户端 (github.com/gcui-art/suno-api)
```

### 2.2 游戏音乐 Prompt 模板

```
赛博朋克BGM:
"cyberpunk electronic, dark synthwave, 128bpm, driving bass,
neon atmosphere, futuristic, instrumental, looping, game background"

战斗音乐:
"epic orchestral battle, fast tempo 140bpm, powerful drums,
brass section, strings, heroic, instrumental, loopable"

休闲BGM:
"lofi chill, 85bpm, warm piano, soft beats, relaxing,
cozy atmosphere, instrumental, seamless loop"

8-bit 像素风:
"chiptune 8-bit, retro game music, upbeat, 150bpm,
nostalgic, NES style, instrumental, loopable"
```

### 2.3 Suno 工作流

```
1. Suno生成 → 下载 MP3
2. Audacity 编辑: 裁剪首尾 → 无缝循环 → 淡入淡出
3. 压缩: OGG Vorbis q5 (游戏用)
4. 导入引擎 → AudioManager 播放

循环裁剪技巧:
- 找相似波形点作为首尾
- 交叉淡入淡出消除接缝
- 目标: 2-4分钟循环段
```

### 2.4 免费音乐生成工具对比

| 工具 | 免费额度 | 质量 | 循环友好 |
|------|---------|------|---------|
| Suno | 5首/天 | ⭐⭐⭐⭐⭐ | 需手动编辑 |
| Udio | 有限 | ⭐⭐⭐⭐⭐ | 需手动编辑 |
| Mubert | 25首/月 | ⭐⭐⭐ | 天生循环 |
| AIVA | 3首/月 | ⭐⭐⭐⭐ | MIDI导出 |
| Beatoven | 15分钟/月 | ⭐⭐⭐ | 可调时长 |
| Soundraw | 有限 | ⭐⭐⭐ | 参数可调 |

---

## 三、Stable Audio — AI 音效/氛围生成

### 3.1 接入

```
网址: https://stableaudio.com
API: 通过 Stability AI API (platform.stability.ai)

特点:
- 文本→音乐/音效/氛围
- 支持时长控制(最长90秒)
- 开源模型: Stable Audio Open
```

### 3.2 游戏音效 Prompt

```
打击音效:
"heavy impact, punch, low thud, game sfx, short, 2 seconds"

魔法音效:
"magical sparkle, ethereal, rising pitch, fantasy sfx, 3 seconds"

环境氛围:
"dark forest ambience, wind, leaves rustling, crickets,
continuous, seamless loop, 30 seconds"

机械音效:
"robot servo, mechanical movement, sci-fi, futuristic,
clean, short, 1 second"

爆炸:
"large explosion, deep bass rumble, debris, destruction,
powerful, game sfx, 5 seconds"
```

### 3.3 音效批处理脚本

```python
# 批量生成游戏音效
import requests, json, time

API_KEY = "sk-your-key"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

sfx_requests = [
    {"prompt": "sword slash, sharp, metallic", "duration": 2},
    {"prompt": "bow arrow shoot, whoosh", "duration": 1},
    {"prompt": "coin collect, magical ding", "duration": 1},
    {"prompt": "door open, heavy wood creak", "duration": 3},
    {"prompt": "victory fanfare, triumphant", "duration": 5},
]

for sfx in sfx_requests:
    resp = requests.post(
        "https://api.stability.ai/v2beta/stable-audio/generate",
        headers=HEADERS,
        json={"prompt": sfx["prompt"], "duration": sfx["duration"]}
    )
    # 保存生成的音效...
```

---

## 四、ElevenLabs — AI 语音/配音

### 4.1 接入

```
网址: https://elevenlabs.io
API: api.elevenlabs.io
免费: 1万字符/月

能力:
- 文本→语音 (多语言/多音色)
- 语音克隆 (上传样本)
- 语音设计 (描述→生成新音色)
- 音效生成 (文本→音效)
```

### 4.2 游戏配音 Prompt

```
角色类型:
- 老者智者: "wise old man, deep, slow, mystical, chinese"
- 少年英雄: "young hero, determined, energetic, chinese"
- 反派Boss: "deep, evil, powerful, echoing, chinese"
- 机器人: "robotic, mechanical, monotone, chinese"
- 精灵: "ethereal, light, playful, chinese"
```

### 4.3 配音集成脚本

```python
import requests

API_KEY = "your_elevenlabs_key"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # 或自定义音色ID

def generate_dialogue(text, output_path="dialogue.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    resp = requests.post(url, headers=headers, json=data)
    with open(output_path, "wb") as f:
        f.write(resp.content)
    return output_path

# 批量生成NPC对话
dialogues = {
    "merchant_greeting": "欢迎光临！来看看我的新货吧！",
    "quest_giver": "勇士，请帮我找回丢失的护符...",
    "boss_taunt": "哈哈哈，你是不可能打败我的！",
}
for name, text in dialogues.items():
    generate_dialogue(text, f"{name}.mp3")
```

### 4.4 AI 音效生成 (ElevenLabs Sound Effects)

```python
# 文本描述 → 音效 (无需语音)
def generate_sfx(description, output_path="sfx.mp3"):
    url = "https://api.elevenlabs.io/v1/sound-generation"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    data = {
        "text": description,
        "duration_seconds": 3  # 最大22秒
    }
    resp = requests.post(url, headers=headers, json=data)
    with open(output_path, "wb") as f:
        f.write(resp.content)

# 示例
generate_sfx("sword clashing with sparks", "sword_clash.mp3")
generate_sfx("footsteps on gravel", "footsteps_gravel.mp3")
generate_sfx("magic portal opening", "portal.mp3")
```

---

## 五、完整工具链

```
游戏音频/动画全流程:

动作捕捉:
  手机拍摄 → DeepMotion/Plask → FBX → Blender精修 → 引擎

背景音乐:
  Suno/Udio → MP3下载 → Audacity循环编辑 → OGG压缩 → 引擎

音效:
  Stable Audio/11Labs SFX → 批量生成 → 音频引擎集成

配音:
  ElevenLabs → 多角色音色 → 文本批量转语音 → 引擎对话系统

氛围:
  Stable Audio → 30-90秒循环 → 环境音轨 → AudioManager分层
```

---

## 六、免费额度汇总

| 工具 | 免费额度 | 够用吗 |
|------|---------|--------|
| DeepMotion | 每月有限 | 几个动画够用 |
| Plask | 60秒/月 | 原型够用 |
| Suno | 5首/天 | 充足 |
| Udio | 有限 | 充足 |
| Stable Audio | 20生成/月 | 关键音效 |
| ElevenLabs | 1万字符/月 | 少量对话 |
| Mubert | 25首/月 | BGM专精 |
| AIVA | 3首/月 | 高质量BGM |
