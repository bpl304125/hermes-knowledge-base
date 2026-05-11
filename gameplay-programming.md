# 游戏玩法编程深度研究

---

## 一、游戏循环 (Game Loop)

### 1.1 经典固定步长循环

```cpp
const double MS_PER_UPDATE = 1000.0 / 60.0; // 16.67ms
double previous = getCurrentTime();
double lag = 0.0;

while (running) {
    double current = getCurrentTime();
    double elapsed = current - previous;
    previous = current;
    lag += elapsed;

    // 固定步长更新（可追赶）
    while (lag >= MS_PER_UPDATE) {
        fixedUpdate(MS_PER_UPDATE / 1000.0);
        lag -= MS_PER_UPDATE;
    }

    // 可变渲染+插值因子
    double alpha = lag / MS_PER_UPDATE;
    render(alpha);
}
```

**关键**: 物理/逻辑固定步长(稳定性)，渲染可变(流畅)，用alpha插值平滑。

### 1.2 三种循环对比

| 模式 | 更新频率 | 渲染频率 | 适合 |
|------|---------|---------|------|
| 可变步长 | 随帧率 | 随帧率 | 简单游戏 |
| 固定步长+追赶 | 60Hz | 可变 | PC/主机 |
| 固定步长+无追赶 | 60Hz | 60fps vsync | 移动端省电 |

---

## 二、输入系统

### 2.1 输入抽象层

```
物理输入(键盘/鼠标/手柄/触屏) → 输入映射 → 游戏动作
```

**动作映射设计**:
```
Jump  →  [Space] [A键(手柄)] [屏幕右侧点击]
Shoot →  [鼠标左键] [RT(手柄)] [屏幕左侧点击]
Move  →  [WASD] [左摇杆] [虚拟摇杆]
```

### 2.2 输入缓冲与手感

| 技术 | 原理 | 应用 |
|------|------|------|
| **输入缓冲** | 提前N帧按键仍然有效 | 跳跃落地瞬间按跳 |
| **土狼时间(Coyote Time)** | 离开平台后N帧仍可跳跃 | 平台跳跃 |
| **跳跃缓冲(Jump Buffer)** | 落地前按跳→落地后执行 | 流畅跳跃 |
| **输入队列** | 存储最近N个输入，依次处理 | 格斗游戏连招 |

```cpp
// Coyote Time示例
class Player {
    float coyoteTimer = 0;
    const float COYOTE_DURATION = 0.1f; // 100ms宽限期

    void update(float dt) {
        if (isGrounded) coyoteTimer = COYOTE_DURATION;
        else coyoteTimer -= dt;

        if (jumpPressed && coyoteTimer > 0) {
            velocity.y = jumpForce;
            coyoteTimer = 0; // 用完
        }
    }
};
```

### 2.3 触屏设计 (移动端/抖音)

```
手势识别:
├── 点击(Tap): 短按<300ms → 选择/确认
├── 滑动(Swipe): 单指滑动 → 方向控制/切水果
├── 长按(Hold): >500ms → 蓄力/拖拽
├── 双指缩放(Pinch): 地图缩放
├── 拖动(Drag): 按住+移动 → 瞄准/拖动物体
└── 多指: 2-3指同时触摸 → 高级操作

双摇杆(FPS手游):
├── 左摇杆: 移动(固定位置)
├── 右摇杆: 视角(相对位置，手指落点即摇杆中心)
└── 关键: 右摇杆需要'动态原点'
```

---

## 三、摄像机系统

### 3.1 第三人称摄像机

```
核心参数:
- 跟随目标偏移(followOffset): (0, 2, -5)
- 阻尼/平滑: springArm长度+旋转阻尼
- 碰撞检测: 射线检测，有障碍时缩短距离
- 输入旋转: 鼠标/右摇杆旋转俯仰(pitch)+偏航(yaw)

Cinemachine模式:
├── 固定跟随: 恒定偏移
├── 轨道: 围绕目标圆形轨道
├── 混合: 多虚拟摄像机平滑切换
└── 噪声: 手持晃动/爆炸震动
```

### 3.2 摄像机震动 (Camera Shake)

```
Perlin噪声驱动:
shakeX = noise(time * frequency + seedX) * intensity
shakeY = noise(time * frequency + seedY) * intensity
shakeZ = noise(time * frequency + seedZ) * intensity * 0.5

衰减: intensity *= (1 - dt / duration)  // 线性
      intensity *= exp(-dt / decayTime)    // 指数衰减

分级:
├── 微震: 脚步落地  intensity=0.02, freq=50
├── 中震: 射击后坐力 intensity=0.1, freq=30
├── 强震: 爆炸        intensity=0.5, freq=20
└── 持续: 地震        intensity=0.3, freq=5, duration=5s
```

---

## 四、游戏手感 (Game Feel / Juice)

### 4.1 屏幕效果

| 效果 | 触发 | 视觉 |
|------|------|------|
| **屏幕震动** | 爆炸/受击 | 摄像机Perlin偏移 |
| **冻结帧(Hit Stop)** | 重击命中 | TimeScale=0 持续50-100ms |
| **色差/扭曲** | 受伤/中毒 | 边缘RGB分离 |
| **径向模糊** | 加速/冲击波 | 从中心向外模糊 |
| **闪白/闪红** | 受击/回血 | 全屏瞬间着色 |

### 4.2 粒子反馈

```
每个动作 = 粒子+音效+震动

普通攻击:
├── 挥砍轨迹(Trail Renderer)
├── 命中火花(金属粒子+闪光)
├── 击退效果(受力方向粒子爆发)
└── 屏幕微震(30Hz, 0.02强度)

暴击:
├── 以上全部 × 1.5倍大小
├── 冻结帧(80ms)
├── 屏幕闪白(10ms)
├── 文字弹出("暴击!" 放大+弹跳)
└── 敌人击飞(慢动作)
```

### 4.3 UI 动画

```
缓动函数(Easing):
├── easeOutBack:  UI弹出效果(超出→回弹)
├── easeInOutCubic: 平滑滑入
├── elasticOut: 橡皮筋效果(弹性)
└── bounceOut: 弹跳落地

数字跳动:
从0→1000: lerp(current, target, 0.1) + 每帧递增音效
关键: 数字滚动+音效节奏匹配 → 满足感
```

### 4.4 手感检查清单

```
□ 角色移动: 加速度/减速度/转向响应
□ 跳跃: 可变跳跃高度(按住更高)/Coyote Time/输入缓冲
□ 攻击: 前摇→判定帧→后摇，可取消窗口
□ 受击: 击退+无敌帧+闪白+震动
□ 音效: 每个动作都有对应的音效反馈
□ UI: 过渡动画+缓动+数字跳动
```

---

## 五、存档与持久化

### 5.1 存档系统设计

```cpp
// 云存档兼容结构
struct SaveData {
    uint32_t version;        // 存档版本
    uint32_t checksum;       // 校验
    uint64_t timestamp;
    PlayerData player;
    WorldData world;
    // JSON或二进制
};

// 多存档槽位
// save_slot_0.sav, save_slot_1.sav, autosave.sav
```

### 5.2 防作弊基本策略

```
客户端存档(单机): JSON混淆+校验和
├── 敏感数值(金币/钻石)加密存储
├── checksum = hash(数据+秘密盐)
└── 定期验证

服务端权威(网游): 所有关键数值服务器验证
├── 客户端只存缓存(UI显示用)
├── 服务器推送真实值
└── 差异>阈值 → 断线/回滚
```

---

## 六、对话与事件系统

### 6.1 对话系统架构

```
对话树节点:
{
  id: "npc_village_001",
  speaker: "村长",
  text: "勇者，请帮我们打败恶龙！",
  choices: [
    {text: "交给我吧", next: "quest_accept"},
    {text: "我考虑一下", next: "quest_later"},
    {text: "给多少钱？", next: "quest_reward", condition: "has_skill:讨价还价"}
  ],
  onEnter: "play_animation:talk",
  onExit: "give_quest:dragon_slayer"
}
```

### 6.2 脚本语言选择

| 方案 | 优点 | 缺点 | 适合 |
|------|------|------|------|
| **Lua** | 极轻量、快、游戏行业标准 | C API繁琐 | 游戏逻辑 |
| **JSON数据驱动** | 无需脚本引擎、策划友好 | 逻辑能力弱 | 简单对话 |
| **C# 脚本** | 与Unity深度集成 | 需编译 | Unity项目 |
| **可视化脚本** | 策划可独立工作 | 复杂逻辑混乱 | 中等复杂度 |
