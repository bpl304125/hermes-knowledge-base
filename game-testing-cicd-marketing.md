# 游戏测试 & CI/CD & Steam营销

## 一、游戏测试体系
| 类型 | 频率 | 工具 |
|------|------|------|
| 单元测试 | 每次提交 | NUnit/xUnit/GUT(Godot) |
| 性能回归 | 每日 | Profiler/RenderDoc |
| 可玩性测试 | 每2周 | 观察+问卷 |

## 二、CI/CD 流水线
```
Push → Lint → Test → Build(Win/Mac/Linux/Android/iOS) → Package → Upload
```
工具: GitHub Actions, Unity Build Automation, Fastlane

## 三、Steam 营销时间线
| 时间 | 行动 |
|------|------|
| -90天 | 商店页+愿望单 |
| -30天 | Next Fest+Demo |
| -7天 | 媒体+直播预热 |
| 发布日 | 首发9折 |

**公式**: 首周销量≈愿望单×0.2~0.5 | 目标>5000
