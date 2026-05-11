"""
GameForge — ComfyUI 游戏资产生成插件
=====================================
将 ComfyUI 扩展为完整的游戏开发管线：

节点组:
  🎬 Animation   — DeepMotion 视频→3D骨骼动画
  🎵 Audio       — Suno BGM / Stable Audio 音效 / ElevenLabs 配音
  📦 SFX Batch   — 批量音效生成

用法:
  1. 复制此文件夹到 ComfyUI/custom_nodes/GameForge/
  2. 重启 ComfyUI
  3. 加载 workflows/game_forge_workflow.json
  4. 设置 API Keys (环境变量或节点输入):
     DEEPMOTION_API_KEY   — https://deepmotion.com
     SUNO_API_KEY         — https://suno.com (需 suno-api 代理)
     STABILITY_API_KEY    — https://platform.stability.ai
     ELEVENLABS_API_KEY   — https://elevenlabs.io
  5. 点击 Queue Prompt
"""

from . import nodes_animation
from . import nodes_audio

# 合并所有节点
from .nodes_animation import NODE_CLASS_MAPPINGS as ANIM_MAP, NODE_DISPLAY_NAME_MAPPINGS as ANIM_NAME
from .nodes_audio import NODE_CLASS_MAPPINGS as AUDIO_MAP, NODE_DISPLAY_NAME_MAPPINGS as AUDIO_NAME

NODE_CLASS_MAPPINGS = {**ANIM_MAP, **AUDIO_MAP}
NODE_DISPLAY_NAME_MAPPINGS = {**ANIM_NAME, **AUDIO_NAME}

# ComfyUI 插件元数据
__version__ = "1.0.0"
__author__ = "Hermes Agent"
WEB_DIRECTORY = None

print("🎮 GameForge v1.0 loaded — 游戏资产生成管线就绪")
print(f"   动画节点: {list(ANIM_MAP.keys())}")
print(f"   音频节点: {list(AUDIO_MAP.keys())}")
print("   加载工作流: workflows/game_forge_workflow.json")
