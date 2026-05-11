"""
GameForge Animation Nodes — DeepMotion API Integration
Video/image to 3D skeletal animation
"""
import os, json, time, requests
import numpy as np
from PIL import Image
import io
try:
    import folder_paths
    COMFY_OUTPUT = folder_paths.get_output_directory()
except ImportError:
    COMFY_OUTPUT = "/tmp/comfyui_output"

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

class DeepMotionAnimation:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"default": "", "multiline": False}),
                "smoothing": (["low", "medium", "high"], {"default": "medium"}),
                "output_format": (["fbx", "bvh", "glb"], {"default": "fbx"}),
                "api_key": ("STRING", {"default": os.environ.get("DEEPMOTION_API_KEY", "")}),
            },
            "optional": {"face_tracking": ("BOOLEAN", {"default": True}), "hand_tracking": ("BOOLEAN", {"default": True})}
        }
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("animation_file", "animation_data_json", "status")
    FUNCTION = "generate"
    CATEGORY = "GameForge/Animation"

    def generate(self, video_path, smoothing, output_format, api_key, face_tracking=True, hand_tracking=True):
        if not api_key: return ("", '{"error":"No API key"}', "missing key")
        if not video_path or not os.path.exists(video_path): return ("", '{"error":"File not found"}', "no file")
        try:
            url = "https://api.deepmotion.com/v1/animate"
            with open(video_path, "rb") as f:
                resp = requests.post(url, headers={"Authorization": f"Bearer {api_key}"}, files={"video": f}, data={"smoothing": smoothing, "format": output_format, "face": str(face_tracking).lower(), "hands": str(hand_tracking).lower()}, timeout=300)
            if resp.status_code == 200:
                result = resp.json()
                anim_url = result.get("animation_url", "")
                anim_data = json.dumps(result, indent=2, ensure_ascii=False)
                if anim_url:
                    anim_resp = requests.get(anim_url, timeout=60)
                    os.makedirs(os.path.join(COMFY_OUTPUT, "gameforge"), exist_ok=True)
                    out_path = os.path.join(COMFY_OUTPUT, "gameforge", f"anim_{int(time.time())}.{output_format}")
                    with open(out_path, "wb") as of: of.write(anim_resp.content)
                    return (out_path, anim_data, f"OK: {out_path}")
                return ("", anim_data, "no download url")
            return ("", json.dumps(resp.json() if resp.text else {}), f"API {resp.status_code}")
        except Exception as e:
            return ("", json.dumps({"error": str(e)}), f"Error: {e}")

class AnimationDataProcessor:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"animation_json": ("STRING", {"default": "", "multiline": True}), "scale": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 100.0, "step": 0.01}), "loop_count": ("INT", {"default": 1, "min": 0, "max": 100})}}
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_json",)
    FUNCTION = "process"
    CATEGORY = "GameForge/Animation"
    def process(self, animation_json, scale, loop_count):
        try:
            data = json.loads(animation_json) if animation_json else {}
            data["processed"] = {"scale": scale, "loop_count": loop_count, "timestamp": time.time()}
            return (json.dumps(data, indent=2),)
        except: return (animation_json,)

NODE_CLASS_MAPPINGS.update({"DeepMotionAnimation": DeepMotionAnimation, "AnimationDataProcessor": AnimationDataProcessor})
NODE_DISPLAY_NAME_MAPPINGS.update({"DeepMotionAnimation": "DeepMotion Video->3DAnim", "AnimationDataProcessor": "Animation Data Processor"})
