# 开元筑城纪 — 技术选型

## 最终决策: Godot 4.4+

### 选型矩阵
| 维度 | Godot 4 | Three.js | Unity |
|------|---------|----------|-------|
| 开源/费用 | MIT免费 | MIT免费 | 个人免费 |
| 3D渲染 | Vulkan+GL | WebGL2 | URP/HDRP |
| 移动端 | ✅ 原生导出 | ⚠️ 浏览器 | ✅ IL2CPP |
| 抖音适配 | ⚠️ 需插件 | ✅ 天然 | ⚠️ 需导出 |
| 学习曲线 | 中 | 低 | 中高 |
| 包体 | 20-50MB | 即时加载 | 50-100MB |

### 技术栈
- 引擎: Godot 4.4+ (GDScript + C#)
- 物理: GodotPhysics (备选Jolt)
- 存档: ConfigFile + 云同步
- 网络: ENet (好友拜访)
- 音效: Godot AudioServer
- CI/CD: GitHub Actions
