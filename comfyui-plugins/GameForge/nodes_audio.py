"""
GameForge Audio Nodes — Suno / Stable Audio / ElevenLabs
"""
import os, json, time, requests
try:
    import folder_paths
    COMFY_OUTPUT = folder_paths.get_output_directory()
except ImportError:
    COMFY_OUTPUT = "/tmp/comfyui_output"

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

STYLES = {
    "game_bgm": "cyberpunk electronic, dark synthwave, 120bpm, instrumental, game bgm",
    "battle": "epic orchestral battle, fast 140bpm, powerful drums, brass, instrumental",
    "ambient": "atmospheric ambient, ethereal pads, peaceful, instrumental",
    "8bit": "chiptune 8-bit, retro game, upbeat 150bpm, NES style, loopable",
    "orchestral": "cinematic orchestra, sweeping strings, grand, film score",
    "lofi": "lofi chill, 85bpm, warm piano, soft beats, instrumental",
}
VOICES = {
    "narrator_sage": "TxGEqnHWrfWFTfGW9XjX",
    "hero_young": "VR6AewLTigWG4xSOukaG",
    "villain_deep": "ErXwobaYiN019PkySvjV",
    "robot": "GBv7mTt0atIp3Br8iCZE",
    "elf_fairy": "EXAVITQu4vr4xnSDxMaL",
}

class SunoMusicGen:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"prompt": ("STRING", {"default": "cyberpunk electronic game bgm", "multiline": True}), "style": (list(STYLES.keys())+["custom"], {"default": "game_bgm"}), "duration": ("INT", {"default": 60, "min": 10, "max": 300, "step": 10}), "api_key": ("STRING", {"default": os.environ.get("SUNO_API_KEY", "")})}}
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("music_url", "status")
    FUNCTION = "generate"
    CATEGORY = "GameForge/Audio"
    def generate(self, prompt, style, duration, api_key):
        if not api_key: return ("", "Need SUNO_API_KEY")
        p = prompt if style == "custom" else STYLES.get(style, prompt)
        try:
            resp = requests.post("https://api.suno.ai/v1/generate", headers={"Authorization": f"Bearer {api_key}"}, json={"prompt": p, "make_instrumental": True, "duration": duration}, timeout=120)
            if resp.status_code == 200:
                r = resp.json()
                url = r.get("audio_url") or r.get("url", "")
                if url:
                    ar = requests.get(url, timeout=60)
                    os.makedirs(os.path.join(COMFY_OUTPUT, "gameforge"), exist_ok=True)
                    out = os.path.join(COMFY_OUTPUT, "gameforge", f"bgm_{style}_{int(time.time())}.mp3")
                    with open(out, "wb") as f: f.write(ar.content)
                    return (out, f"OK: {out}")
                return (url, "online URL")
            return ("", f"API {resp.status_code}: use suno.com web UI")
        except Exception as e: return ("", str(e))

class StableAudioGen:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"prompt": ("STRING", {"default": "heavy impact punch", "multiline": True}), "duration": ("FLOAT", {"default": 2.0, "min": 0.5, "max": 90.0, "step": 0.5}), "sfx_type": (["impact","magic","ambient","mechanical","nature","ui","custom"], {"default": "impact"}), "api_key": ("STRING", {"default": os.environ.get("STABILITY_API_KEY", "")})}}
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("audio_file", "status")
    FUNCTION = "generate"
    CATEGORY = "GameForge/Audio"
    SFX = {"impact":"heavy impact low thud game sfx","magic":"magical sparkle ethereal fantasy","ambient":"ambient atmosphere environmental","mechanical":"robot servo mechanical sci-fi","nature":"nature wind leaves organic","ui":"UI click digital clean beep"}
    def generate(self, prompt, duration, sfx_type, api_key):
        if not api_key: return ("", "Need STABILITY_API_KEY")
        p = prompt if sfx_type == "custom" else self.SFX.get(sfx_type, prompt)
        try:
            resp = requests.post("https://api.stability.ai/v2beta/stable-audio/generate", headers={"Authorization": f"Bearer {api_key}"}, json={"prompt": p, "duration": duration}, timeout=120)
            if resp.status_code == 200:
                os.makedirs(os.path.join(COMFY_OUTPUT, "gameforge"), exist_ok=True)
                out = os.path.join(COMFY_OUTPUT, "gameforge", f"sfx_{sfx_type}_{int(time.time())}.wav")
                with open(out, "wb") as f: f.write(resp.content)
                return (out, f"OK: {out}")
            return ("", f"API {resp.status_code}")
        except Exception as e: return ("", str(e))

class ElevenLabsVoice:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"text": ("STRING", {"default": "Welcome to my game!", "multiline": True}), "voice_type": (list(VOICES.keys())+["custom"], {"default": "hero_young"}), "stability": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.05}), "api_key": ("STRING", {"default": os.environ.get("ELEVENLABS_API_KEY", "")})}, "optional": {"custom_voice_id": ("STRING", {"default": ""})}}
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("audio_file", "status")
    FUNCTION = "generate"
    CATEGORY = "GameForge/Audio"
    def generate(self, text, voice_type, stability, api_key, custom_voice_id=""):
        if not api_key: return ("", "Need ELEVENLABS_API_KEY")
        vid = custom_voice_id if custom_voice_id and voice_type == "custom" else VOICES.get(voice_type, "21m00Tcm4TlvDq8ikWAM")
        try:
            resp = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}", headers={"xi-api-key": api_key, "Content-Type": "application/json"}, json={"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": stability, "similarity_boost": 0.75}}, timeout=60)
            if resp.status_code == 200:
                os.makedirs(os.path.join(COMFY_OUTPUT, "gameforge"), exist_ok=True)
                out = os.path.join(COMFY_OUTPUT, "gameforge", f"voice_{voice_type}_{int(time.time())}.mp3")
                with open(out, "wb") as f: f.write(resp.content)
                return (out, f"OK: {out}")
            return ("", f"API {resp.status_code}")
        except Exception as e: return ("", str(e))

class SFXBatchGenerator:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"sfx_list": ("STRING", {"default": '[{"name":"hit","prompt":"impact","duration":2}]', "multiline": True}), "api_key": ("STRING", {"default": os.environ.get("STABILITY_API_KEY", "")})}}
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("output_dir", "status")
    FUNCTION = "generate_batch"
    CATEGORY = "GameForge/Audio"
    def generate_batch(self, sfx_list, api_key):
        if not api_key: return ("", "Need STABILITY_API_KEY")
        try:
            items = json.loads(sfx_list)
            out_dir = os.path.join(COMFY_OUTPUT, "gameforge", f"batch_{int(time.time())}")
            os.makedirs(out_dir, exist_ok=True)
            results = []
            for item in items:
                resp = requests.post("https://api.stability.ai/v2beta/stable-audio/generate", headers={"Authorization": f"Bearer {api_key}"}, json={"prompt": item.get("prompt",""), "duration": item.get("duration",2)}, timeout=120)
                if resp.status_code == 200:
                    p = os.path.join(out_dir, f"{item.get('name','sfx')}.wav")
                    with open(p, "wb") as f: f.write(resp.content)
                    results.append(f"OK {item.get('name','?')}")
                else: results.append(f"FAIL {item.get('name','?')} {resp.status_code}")
            return (out_dir, "\n".join(results))
        except Exception as e: return ("", str(e))

NODE_CLASS_MAPPINGS.update({"SunoMusicGen": SunoMusicGen, "StableAudioGen": StableAudioGen, "ElevenLabsVoice": ElevenLabsVoice, "SFXBatchGenerator": SFXBatchGenerator})
NODE_DISPLAY_NAME_MAPPINGS.update({"SunoMusicGen": "Suno BGM Generator", "StableAudioGen": "Stable Audio SFX", "ElevenLabsVoice": "ElevenLabs Voice/Dub", "SFXBatchGenerator": "Batch SFX Generator"})
