# 游戏AI行为系统 & 移动端优化速查

---

## 一、NPC AI 行为架构

### 分层AI设计
```
战略层(GOAP/效用AI) → 战术层(行为树) → 执行层(寻路/动画)
```

### 行为树节点速查
```
Composite: Selector(优先级) | Sequence(顺序) | Parallel(并行)
Decorator: Inverter | Repeater | UntilFail | Cooldown | Limiter
Condition: IsDay | HasTarget | IsHealthy | CanSeePlayer | Distance < X
Action:    MoveTo | Attack | Patrol | Flee | Idle | UseSkill | Search
```

### GOAP 规划示例
```
目标: KillEnemy {enemyDead:true}
动作池:
  EquipWeapon: cost=1, pre={hasWeapon:false}, post={hasWeapon:true}
  MoveToCover: cost=2, pre={},            post={inCover:true}
  MoveToEnemy: cost=1, pre={},            post={nearEnemy:true}
  Aim:         cost=1, pre={hasWeapon},   post={isAiming:true}
  Shoot:       cost=1, pre={isAiming,nearEnemy}, post={enemyDead:true}

A*搜索 → [EquipWeapon → MoveToEnemy → Aim → Shoot] ✓
```

---

## 二、移动端性能优化速查

### 帧预算 (60FPS)
```
16.67ms 总预算
├── 物理: 2-3ms
├── AI/逻辑: 2-3ms
├── 渲染: 6-8ms
├── UI: 1-2ms
└── 余量: 2-3ms
```

### 抖音小游戏核心指标
| 指标 | 目标 |
|------|------|
| Draw Call | <50 |
| 首包 | <4MB |
| 总包 | <20MB |
| 内存峰值 | <200MB |
| FPS | >30 |
| 崩溃率 | <0.1% |

### 移动端纹理压缩
```
Android: ETC2 (GLES 3.0+)
iOS:     ASTC 4x4/6x6
通用:    ETC2 + ASTC (多格式分发)
```
