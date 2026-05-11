# 真实 3D 游戏开发工程知识

---

## 一、Godot 引擎架构 (110K⭐, MIT, C++)

### 场景树 (核心数据结构)
```
SceneTree (场景树)
├── Root (Viewport)
│   ├── World3D (物理世界 + 渲染世界)
│   ├── Camera3D (摄像机)
│   └── Node (一切皆节点)
│       ├── Node3D (3D空间节点)
│       │   ├── MeshInstance3D (网格渲染)
│       │   ├── CollisionShape3D (碰撞体)
│       │   └── AnimationPlayer (动画)
│       └── Node2D (2D节点,独立于3D)
```

### 渲染管线执行顺序
```
1. 视锥剔除 → 2. 遮挡剔除 → 3. 不透明度排序(前→后) 
→ 4. 正向渲染不透明Pass → 5. 天空渲染 → 6. 半透明排序(后→前)
→ 7. 后处理(Bloom/SSAO/DOF/ColorCorrection) → 8. 输出到屏幕
```

### 服务器架构 (Singleton)
```
RenderingServer — 所有渲染命令的抽象层
PhysicsServer3D — 物理世界管理 (GodotPhysics/Jolt)
AudioServer — 音频管理
NavigationServer3D — 寻路(NavMesh/Recast)
XRServer — VR/AR
```

## 二、Veloren — 开源 3D MMO

### 技术栈
```
引擎: 自研(基于wgpu Rust图形库)
语言: Rust
物理: 自研精简物理
网络: 客户端-服务器, UDP
世界: 体素+无限程序化生成
ECS: specs/legion (Rust ECS库)

项目结构:
veloren/
├── client/      # 客户端 (渲染+输入+UI)
├── server/      # 专用服务器
├── common/      # 共享代码(网络协议/数据定义)
├── world/       # 世界生成算法
├── voxygen/     # 客户端二进制入口
└── server-cli/  # 服务器二进制入口
```

### 关键架构决策
```
1. ECS分离客户端/服务器 → 客户端ECS有渲染组件,服务器只有逻辑
2. 网络同步: 只同步ECS组件变化(增量)
3. 世界生成: 噪声→生物群系→结构→实体放置(多层管道)
4. 渲染: wgpu(Vulkan/Metal/DX12), PBR+阴影映射
```

## 三、3D游戏通用架构模式

### 游戏循环 (生产级)
```cpp
class Game {
    double fixedDt = 1.0/60.0;  // 物理步长
    double accumulator = 0;
    double frameTime;

    void run() {
        while(running) {
            frameTime = getDeltaTime();
            accumulator += frameTime;

            processInput();      // 1. 输入
            while(accumulator >= fixedDt) {
                fixedUpdate(fixedDt);  // 2. 固定更新(物理/AI)
                accumulator -= fixedDt;
            }
            double alpha = accumulator / fixedDt;
            variableUpdate(frameTime);  // 3. 可变更新(动画/粒子)
            render(alpha);              // 4. 渲染(带插值)
            playAudio();                // 5. 音频
        }
    }
};
```

### 实体管理
```
方案1: ECS (最优,大世界/多实体)
  Entity → [Transform, Mesh, Health, AI] → Systems按Component查询

方案2: GameObject+Component (灵活,中小项目)
  GameObject → 挂载Component → Update()遍历

方案3: 继承层次 (简单,不适合扩展)
  Entity→Character→Player→Warrior (钻石继承问题)
```

### 事件总线 (解耦)
```cpp
EventBus::emit<DamageEvent>({attacker, target, 50});
// 多个系统独立响应:
//   HealthSystem: 扣血
//   UISystem: 显示伤害数字
//   AudioSystem: 播放受击音效
//   ParticleSystem: 播放血花粒子
// 各系统互不依赖
```

## 四、物理引擎集成

### Jolt Physics (Horizon Zero Dawn, Godot 4.4+)
```
集成步骤:
1. 创建 PhysicsSystem
2. 注册 Body (静态/动态/运动学)
3. 添加 Shape (Box/Sphere/Capsule/Convex/Mesh)
4. 每帧: PhysicsSystem.Update(dt)
5. 读取变换: body.GetPosition()/GetRotation()
6. 碰撞回调: ContactListener→游戏事件
```

### 物理层分离
```
表现层 (渲染Mesh) ← → 物理层 (碰撞Shape)
      不耦合                  不耦合
  可以不同精度              简化碰撞体
  可以不同位置              独立于渲染
```

## 五、资源管理

### 引用计数 + 异步加载
```
ResourceManager:
├── Load<T>(path) → 同步(阻塞,初始化用)
├── LoadAsync<T>(path) → 异步(游戏中使用)
├── Get<T>(path) → 返回已加载或null
└── UnloadUnused() → 释放无引用资源

对象池:
BulletPool: 预分配100个子弹
├── Get() → 从池中取
└── Return(bullet) → 重置状态,放回池
```

## 六、项目目录结构(生产级)

```
my_3d_game/
├── assets/              # 原始资源(不直接使用)
│   ├── models/          # Blender/Maya源文件
│   ├── textures/        # Substance/PS源文件
│   └── audio/           # 原始音频
├── build/               # 构建产物(不进版本控制)
├── src/                 # 源代码
│   ├── core/            # 引擎核心(游戏循环/事件/ECS)
│   ├── gameplay/        # 游戏玩法(角色/战斗/技能)
│   ├── render/          # 渲染(着色器/材质/后处理)
│   ├── physics/         # 物理(碰撞检测/射线)
│   ├── audio/           # 音频管理
│   ├── network/         # 网络(客户端/服务器)
│   ├── ui/              # UI系统
│   └── tools/           # 编辑器/工具
├── resources/           # 导入后资源(引擎格式)
├── scenes/              # 场景文件
├── shaders/             # 着色器
└── config/              # 配置文件
```
