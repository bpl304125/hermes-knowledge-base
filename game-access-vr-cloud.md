# 游戏无障碍 + VR/AR + 云服务

## 一、游戏无障碍设计

| 类型 | 方案 | 目标 |
|------|------|------|
| 视觉 | 色盲模式/高对比度/字幕可调 | 色弱/低视力 |
| 听觉 | 字幕+可视化音效指示 | 听障 |
| 运动 | 辅助瞄准/一键操作/按键映射 | 肢体障碍 |
| 认知 | 难度调节/提示系统/简化UI | 认知障碍 |

**行业标准**: Xbox Accessibility Guidelines, Game Accessibility Guidelines

## 二、VR/AR 开发

| 平台 | SDK | 引擎 | 难度 |
|------|-----|------|------|
| Meta Quest | Oculus SDK/OpenXR | Unity/Unreal | 中 |
| Apple Vision Pro | visionOS SDK | Unity/RealityKit | 高 |
| WebXR | Three.js/A-Frame | 浏览器 | 低 |
| AR手机 | ARCore/ARKit | Unity | 中 |

**VR性能基线**: 72-90fps × 双眼渲染, 每眼≥1832×1920

## 三、游戏云服务

| 服务 | 功能 | 免费层 |
|------|------|--------|
| PlayFab(Azure) | 后端/排行榜/匹配 | 10万MAU |
| Firebase | 实时数据库/认证 | 慷慨 |
| Unity Gaming Services | 一站式 | 有限 |
| Steamworks | 成就/云存档/匹配 | 免费 |
| Photon | 多人网络 | 20CCU免费 |
| Nakama(Heroic Labs) | 开源游戏后端 | 自部署免费 |
