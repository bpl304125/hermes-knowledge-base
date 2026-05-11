# ECS 架构 & 游戏设计文档

## 一、ECS 深入 (Entity Component System)

### 核心概念
```
Entity:  ID(无数据,无行为)
Component: 纯数据(位置/血量/速度)
System:   纯逻辑(遍历含特定Component的Entity)
World:    容器,管理所有Entity/Component/System

// Bevy 示例
fn move_system(mut query: Query<(&mut Transform, &Velocity)>) {
    for (mut transform, velocity) in query.iter_mut() {
        transform.translation += velocity.vec * time.delta_seconds();
    }
}
```

### ECS vs OOP
| | ECS | OOP |
|------|-----|-----|
| 数据布局 | SoA连续(缓存友好) | AoS散列 |
| 扩展 | 加Component+System | 修改继承链 |
| 并行 | 依赖分析自动并行 | 手动 |
| 引擎 | Bevy/Flecs/EnTT/DOTS | Unity传统/Unreal |

## 二、GDD 模板

### 一页纸GDD
```
标题: [游戏名] | 平台: [PC/Mobile/Web] | 引擎: [Godot/Unity/Unreal]

核心玩法: [一句话描述玩家做什么]
独特卖点: [为什么玩家要玩你的游戏?]
目标受众: [谁在玩?]
美术风格: [像素/低多边形/写实/手绘]
参考游戏: [类似游戏1,2,3]
核心循环: [探索→战斗→收集→升级→循环]
变现: [买断/广告/IAP/混合]
开发周期: [估算时间]
```

### 必含文档
1. 玩法机制说明(核心循环+边缘系统)
2. 关卡设计文档(至少3关详细)
3. 数值表(Excel: 敌人/升级/经济)
4. 美术规范(风格指南+尺寸规范)
5. 技术文档(架构+API+工具链)
