# 2D/3D 游戏开发完整技术栈 —— 深度总结

---

## 第一部分：2D 游戏开发

### 一、2D 渲染系统

#### 1.1 Sprite 精灵系统

Sprite 是 2D 游戏最基本的渲染单元，本质是一张带位置、旋转、缩放的纹理矩形。

核心概念：
- **纹理图集 (Texture Atlas)**：将多个 Sprite 合并到一张大纹理中，减少 GPU draw call。运行时通过 UV 坐标裁剪显示不同的子图。工具：TexturePacker、Shoebox。
- **批处理 (Batching)**：渲染器将使用同一图集/材质的 Sprite 合并为一次 draw call。动态批处理有顶点数限制（通常 <300 顶点），静态批处理无此限制但内存占用更高。
- **渲染顺序**：通过 SortingLayer + OrderInLayer 控制绘制顺序，实现前后景关系。
- **九宫格 (9-Slicing)**：将 UI/Sprite 分成 9 个区域，四角保持原样，边缘拉伸，中心填充。用于可伸缩的背景框、对话框。

#### 1.2 TileMap 瓦片地图

瓦片地图是 2D 场景构建的基础手段，将地图划分为规则网格。

| 技术点 | 说明 |
|--------|------|
| 瓦片集 (Tileset) | 一张包含所有瓦片纹理的图片，每个瓦片通常 32x32 或 64x64 |
| 图层 (Layers) | 地面层、障碍物层、装饰层、碰撞层等分层管理 |
| 渲染模式 | 正方形/六边形/等距 (Isometric) |
| Tiled 编辑器 | 开源地图编辑器，导出 TMX/JSON 格式，所有主流引擎均支持 |
| 自动拼接 (Auto-tiling) | 根据相邻瓦片自动选择正确的过渡瓦片（如 Godot 的 Terrains） |
| 大世界优化 | Chunk 分块加载、视锥剔除、LOD（远处合并瓦片） |

#### 1.3 骨骼动画 (Spine / DragonBones)

与传统帧动画相比，骨骼动画内存占用极低（一套骨骼 + 少量纹理 vs 大量帧图），且支持平滑混合。

工作流程：
1. 将角色拆分为各个部件（头、身体、手臂、腿等）
2. 建立骨骼层级结构
3. 绑定蒙皮（顶点权重映射）
4. 制作关键帧动画
5. 导出 JSON/Skel + Atlas 文件到引擎

关键技术：
- **骨骼混合**：两套动画之间平滑过渡（奔跑→跳跃）
- **动画遮罩**：只混合上半身（例如边跑边射击）
- **IK 反向动力学**：指定末端位置，自动计算关节角度（脚踩地面）
- **FFD 自由变形**：网格变形实现柔体效果
- **Spine vs DragonBones**：Spine 是商业软件（$299起），DragonBones 开源免费但停止维护。Spine 生态系统更成熟，Cocos Creator、Unity、Godot 均有官方运行时。

#### 1.4 粒子系统

用于火焰、烟雾、爆炸、魔法、雨雪等动态效果。

关键参数：
- 发射速率、生命周期、初始速度/方向/颜色/大小
- 速度衰减 (Damping)、重力、风力
- 颜色渐变曲线、大小渐变曲线
- 渲染模式：Billboard（始终朝向相机）、拉伸粒子、网格粒子
- 模块组合：Shape（发射形状）、ColorOverLifetime、SizeOverLifetime、Noise、SubEmitter（粒子死亡时生成新粒子）

性能优化：
- 最大粒子数硬限制
- 简化 Shader（无光照计算）
- 使用图集合批

---

### 二、2D 物理引擎

#### 2.1 Box2D 深入

Box2D（作者 Erin Catto，GitHub Stars 9,653）是 2D 游戏物理的事实标准，C++ 编写，几乎所有引擎的 2D 物理均基于或受其启发。

| 概念 | 说明 |
|------|------|
| World | 物理世界容器，管理所有 Body、Joint、Contact |
| Body | 刚体，含位置、角度、速度、阻尼。三种类型：Static(不动/质量0)、Dynamic(完全模拟)、Kinematic(手动控制/不受力) |
| Fixture | 碰撞形状附着在 Body 上，包含形状、摩擦系数、弹性(restitution)、密度 |
| Shape | Circle(圆形)、Edge(线段)、Polygon(多边形/最多8个顶点)、Chain(链条/地形) |
| Joint | 关节连接两个 Body：Distance(距离)、Revolute(旋转/铰链)、Prismatic(滑动)、Pulley(滑轮)、Weld(焊接)、Mouse(拖拽) |
| Contact Listener | 碰撞回调：BeginContact / EndContact / PreSolve / PostSolve |
| 连续碰撞检测 CCD | 高速物体（子弹）防止穿透，对指定 Body 开启 bullet 标志 |

平台跳跃实现要点：
- 角色用 Dynamic Body，控制器直接修改速度而非施加力（保证手感）
- 地面检测：用射线或底部小圆 Fixture + Contact 判断 IsGrounded
- 可变跳跃高度：检测按键松手→如果还在上升则减小 Y 速度
- 土狼时间 (Coyote Time) + 输入缓冲 (Input Buffer)：增强手感

物理谜题要点：
- 依赖稳定模拟：使用固定时间步长 (1/60)，累积器模式
- 速度/位置迭代次数：速度迭代 8、位置迭代 3 为常用设置
- 休眠机制：静止物体自动休眠节省计算

#### 2.2 JavaScript 物理引擎

- **planck.js**（Stars 5,246）：Box2D 的 JavaScript 移植，API 与 Box2D 一致
- **Matter.js**：轻量级 2D 物理，适合简单游戏和原型
- **p2.js**：3D 物理简化版，支持更多形状类型

---

### 三、设计模式

#### 3.1 Game Loop 游戏循环

```
固定时间步长模式（推荐）：
  lag += deltaTime
  while (lag >= FIXED_DT):
      physics.Update(FIXED_DT)    // 物理/逻辑以固定步长更新
      lag -= FIXED_DT
  render(alpha = lag / FIXED_DT)  // 渲染做插值，平滑画面
```

关键点：
- 物理与渲染解耦：物理固定更新保证确定性，渲染插值保证流畅
- requestAnimationFrame（Web）/ vsync（原生）：与显示器刷新同步
- 避免 deltaTime 巨大抖动（切后台返回时 cap 最大步长）

#### 3.2 对象池 (Object Pool)

子弹、敌兵、粒子、特效等高频创建/销毁对象必须用对象池。

```
class Pool:
    available = []
    def get():
        if available: return available.pop().reset()
        else: return new Object()
    def release(obj):
        obj.deactivate()
        available.append(obj)
```

要点：
- 预热 (Pre-warm)：场景加载时预创建 N 个
- 自动扩容 + 上限保护
- 每个对象有 Acquire/Release 生命周期回调

#### 3.3 状态机 (State Machine / FSM)

角色行为管理核心模式。

```
PlayerState: Idle → Run → Jump → Fall → Land → Idle
                        ↘ Attack (子状态机)
```

实现方式：
- Switch/Enum 状态机：简单但扩展性差
- 状态对象模式：每个状态一个类，含 Enter/Update/Exit，状态自己管理转换
- 分层状态机：子状态继承父状态逻辑
- 行为树：更灵活但更复杂，适合 AI

#### 3.4 命令模式 (Command Pattern)

应用场景：
- 输入系统：将按键映射到命令对象，方便改键、录制回放
- 撤销/重做：每个操作封装为命令，维护历史栈
- 网络同步：将操作序列化为命令发送

```
class Command:
    def execute(): pass
    def undo(): pass

MoveCommand(unit, direction) → 支持 Undo 回到原位
```

#### 3.5 其他关键模式

- 观察者模式 / 事件总线：模块解耦（得分变化→UI更新、音效播放、成就检测）
- 组件模式 (ECS)：Entity 是 ID，Component 存数据，System 处理逻辑。Unity DOTS / Godot 节点组件
- 服务定位器：全局服务访问（音频管理器、资源管理器）
- 单例模式：游戏管理器、配置表等全局唯一实例

---

### 四、UI 系统

#### 4.1 分辨率适配

| 策略 | 说明 |
|------|------|
| 固定设计分辨率 | 设定基准分辨率（如 1920x1080），实际按比例缩放 |
| Canvas Scaler (Unity) | ScaleWithScreenSize 模式，设置 Match（宽高匹配权重 0~1） |
| 多分辨率策略 | Expand(超出裁剪)、Shrink(留黑边)、FixedHeight/FixedWidth |
| Godot Stretch | 设置 StretchMode=canvas_items, StretchAspect=expand |
| Cocos Creator | 设计分辨率 + Fit Height / Fit Width / SHOW_ALL / EXACT_FIT |

#### 4.2 SafeArea（安全区）

刘海屏/圆角屏（iPhone X 起、Android 全面屏）需要 SafeArea 适配。

- Unity：Screen.safeArea 获取安全区域 Rect
- Cocos Creator：screen.safeArea + Widget 组件自动适配
- Web：CSS env(safe-area-inset-top) 等环境变量

#### 4.3 UI 图集优化

- 将 UI 小图合并成大图集，降低 draw call
- 界面间图集隔离，避免加载不需要的资源
- 九宫格精灵减少 UI 背景图尺寸需求
- 压缩格式：ETC2/ASTC（移动端）、DXT5/BC7（PC）

---

### 五、2D 光照系统

2D 光照的核心技术是**法线贴图**加持下的动态光照。

实现原理：
1. 为 Sprite 制作法线贴图（Normal Map），编码每个像素的表面法线方向
2. 在 Shader 中接收灯光位置/颜色/强度参数
3. 计算每个像素的光照：
   ```
   N = normalize(normal_map.rgb * 2 - 1)   // 解码法线
   L = normalize(light_pos - pixel_pos)     // 光线方向
   diffuse = max(dot(N, L), 0) * light_color * intensity
   final = albedo * (ambient + diffuse)
   ```

支持的功能：
- 点光源、方向光、聚光灯
- 阴影投射（硬阴影/软阴影，基于射线或 Shadow Volume）
- 自发光材质
- 环境光、HDR 泛光 (Bloom) 后处理

引擎支持情况：
- Unity 2D：URP 内置 2D Renderer，支持 Sprite Light、Sprite Shape
- Godot：CanvasItemMaterial + Light2D 节点
- Cocos Creator：2D 渲染管线支持动态光照
- 纯 Web：PixiJS + 自定义 Shader / Phaser + Light2D 插件

---

### 六、跨平台 2D 框架对比

| 框架 | GitHub Stars | 语言 | 优势 | 劣势 |
|------|-------------|------|------|------|
| Godot | 110,546 | GDScript/C#/C++ | 完全免费开源，2D 一流（专用 2D 渲染器），轻量（~50MB），节点系统直观 | 3D 不如 Unity/Unreal，生态较小 |
| Unity 2D | - | C# | 生态最大，AssetStore 丰富，URP 2D 渲染管线，跨平台最全 | 较重，编译慢，许可证费用（收入超20万美元需付费） |
| Cocos Creator | 9,578 | TypeScript/JS | 国内小游戏/微信/抖音生态之王，2D 性能极佳，轻量，开源 | 3D 较弱，国际社区小，文档中英文割裂 |
| Phaser | 39,607 | JavaScript | Web 2D 最流行框架，学习曲线平缓，文档完善，插件丰富 | 仅 Web，无原生导出，大型项目难维护 |
| PixiJS | 47,156 | JavaScript | 纯粹 2D WebGL 渲染引擎，极快，灵活度极高 | 非完整框架（无物理/音效/场景管理），需自己搭建 |
| LittleJS | 4,094 | JavaScript | 超轻量（~10KB），零依赖，适合 JS13K 等比赛 | 功能极简，不适合商业项目 |

选择建议：
- 微信/抖音/H5 小游戏 → Cocos Creator（字节系有官方优化适配）
- 独立游戏/PC+主机 → Godot 或 Unity
- 纯 Web 轻量游戏 → Phaser
- 自定义渲染管线/创意项目 → PixiJS
- 快速原型/学习 2D 物理 → Love2D (Lua)

---

### 七、2D 游戏类型技术要点

#### 横版动作 (Platformer)
- 角色控制器：速度驱动（非力驱动），手感优先
- 土狼时间 + 输入缓冲 + 转角修正 (Corner Correction)
- 相机跟随：平滑插值 + 预测框 + 水平/垂直独立死区
- 关卡流式加载：分块异步加载

#### Roguelike / Roguelite
- 随机地图生成：BSP 空间分割、元胞自动机、Drunkard Walk、房间连接
- 种子系统：同一 seed 生成相同地图
- 道具/天赋系统：基于 ECS 或条件链的 Buff/Debuff 叠加
- 存档：序列化当前状态（房间图、玩家属性和道具）

#### 塔防 (Tower Defense)
- 寻路：A* 网格寻路，动态更新（建塔后重新规划）
- 塔的 AI：目标选择策略（最近/最远/最弱/最强）
- 弹道：追踪弹、抛物线、瞬时命中
- 波次系统：读取配置表生成敌兵波次

#### 三消 (Match-3)
- 棋盘数据结构：2D 数组
- 消除检测：BFS/DFS 搜索同色连通区域
- 下落 + 填充：补位动画序列管理
- 技能/道具系统：状态机管理特殊消除逻辑

#### 弹幕射击 (Bullet Hell)
- 弹幕生成器：极坐标 + 参数方程，控制弹幕形状（扇形、圆形、螺旋、激光）
- 优化：对象池 + 简化碰撞（圆形 vs 圆形，无物理引擎）
- 判定点：玩家碰撞体积极小（一个点），只有击中这个点才算被击中
- 帧同步/REPLAY：确定性逻辑（无浮点误差累积）

---

## 第二部分：3D 游戏开发

### 八、3D 数学基础

#### 8.1 向量 (Vector)

```
核心运算
v = (x, y, z)
length = sqrt(x^2 + y^2 + z^2)     // 模长
v_norm = v / length                 // 归一化
dot = a·b = |a||b|cos(theta)       // 点乘 → 判断方向/夹角/投影
cross = a×b                        // 叉乘 → 法线/垂直方向/左右判断
```

实战应用：
- 移动方向归一化避免斜向加速
- 点乘判断敌人在前方/后方（dot > 0 在前方）
- 点乘做视野检测：dot(forward, toTarget) > cos(FOV/2)
- 叉乘判断左右：cross(forward, toTarget).y > 0 在右侧
- 反射向量：R = I - 2(N·I)N

#### 8.2 矩阵 (Matrix)

4×4 变换矩阵是 3D 的核心：
- 模型矩阵 (Model)：局部坐标 → 世界坐标（SRT：缩放→旋转→平移）
- 视图矩阵 (View)：世界坐标 → 相机坐标
- 投影矩阵 (Projection)：相机坐标 → 裁剪空间（透视/正交）
- MVP = P × V × M：顶点着色器中每个顶点乘以 MVP

寻址方式：行主序 vs 列主序（不同引擎/API 不同，需注意转置）。

#### 8.3 四元数 (Quaternion)

解决欧拉角的万向节锁问题，所有 3D 旋转的底层实现。

```
q = (w, x, y, z)   // w 是标量部分，(x,y,z) 是向量部分
// 绕任意轴旋转 theta 角：
q = (cos(theta/2), axis.x*sin(theta/2), axis.y*sin(theta/2), axis.z*sin(theta/2))
```

实战操作：
- 球面线性插值 (Slerp)：Quaternion.Slerp(a, b, t) 平滑旋转
- LookRotation：从方向向量计算朝向四元数
- 旋转合成：q3 = q2 * q1（先 q1 后 q2）
- 与欧拉角转换：仅用于编辑器/用户界面显示，逻辑层全程用四元数

---

### 九、3D 动画系统

#### 9.1 骨骼动画 (Skeletal Animation)

核心流程：
1. 蒙皮 (Skinning)：为每个顶点绑定最多 4 根骨骼及权重
2. 骨骼层级：root → spine → chest → upper_arm → lower_arm → hand
3. 动画姿势 (Pose)：每帧记录所有骨骼的 TRS
4. 蒙皮矩阵：bone_matrix = bone_world * inverse_bind_pose，顶点最终位置 = sum(weight_i × bone_matrix_i × vertex_pos)

GPU Skinning：在顶点着色器中完成蒙皮计算，减少 CPU-GPU 数据传输。

#### 9.2 动画混合

- 线性混合：两个动画按权重插值（如走→跑过渡）
- 混合树 (Blend Tree)：根据参数（速度、方向）在多个动画间混合
  - 1D Blend: idle ← blend → walk ← blend → run （按速度参数）
  - 2D Blend: 八个方向移动动画按 (x, y) 混合
- 动画遮罩 (Avatar Mask)：上半身射击动画 + 下半身跑步动画同时播放
- 动画层 (Layer)：基础层（移动）+ 叠加层（受伤反应，Additive 模式）
- Sync：同步不同动画的时间位置，保证步伐一致

#### 9.3 IK (反向动力学)

- CCD IK：从末端逐关节向根迭代旋转，直到末端到达目标
- FABRIK：更快收敛的迭代算法，前后往返调整
- 应用：脚部贴地（Foot IK）、手抓取物体、头部注视

#### 9.4 动画状态机 (Animator / AnimationTree)

```
Entry → Idle → [speed>0.1] → Walk → [speed>0.8] → Run
         ^                        |[speed<0.1]
         +------------------------+
```

关键特性：
- 过渡条件（布尔/浮点/触发参数）
- 过渡持续时间 + 插值曲线
- 子状态机（如攻击子机，含起手→判定→收手）
- 分层混合

---

### 十、碰撞检测

#### 10.1 包围体类型

| 类型 | 检测复杂度 | 紧密度 | 适用场景 |
|------|-----------|--------|----------|
| 球体 (Sphere) | O(1)，只需距离比较 | 差 | 快速粗筛、弹幕、子弹 |
| AABB (轴对齐包围盒) | O(1)，6次比较 | 一般 | 最常用，静态/动态物体粗筛 |
| OBB (有向包围盒) | O(1)，需 SAT | 较好 | 旋转物体 |
| 凸包 (Convex Hull) | GJK/EPA 算法 | 好 | 复杂形状物理碰撞 |
| 三角网格 (Mesh) | 射线/球体扫描 | 精确 | 地形/静态关卡碰撞 |

#### 10.2 宽相与窄相

宽相 (Broad Phase)：快速排除不可能碰撞的物体对。
- 空间哈希 / 网格分区
- 扫描线 (Sweep and Prune)：按 AABB 在某轴排序
- BVH (层次包围体树)：递归细分包围盒

窄相 (Narrow Phase)：对候选对的精确检测。
- SAT (分离轴定理)：凸多面体间碰撞检测
- GJK (Gilbert-Johnson-Keerthi)：任意凸形状间最近距离/碰撞
- EPA (扩展多面体算法)：从 GJK 结果算出穿透深度和方向

#### 10.3 射线检测 (Raycast)

应用场景：射击命中判定、鼠标拾取 3D 物体、AI 视线检测、地面高度检测。

```
Raycast(origin, direction, maxDistance, layerMask)
返回: hitPoint, hitNormal, hitDistance, hitCollider
```

优化：
- 分层 (LayerMask) 过滤无关对象
- 使用空间加速结构 (BVH/Octree)，避免逐个三角面检测
- 球体投射 (SphereCast)：替代细射线检测可移动物体（有厚度）

---

### 十一、相机系统

#### 11.1 第三人称相机

最常见的动作/冒险游戏相机。

核心需求：
- 跟随目标 + 平滑插值（避免抖动）
- 旋转：鼠标/右摇杆绕目标旋转（轨道）
- 碰撞检测：相机与场景碰撞时自动缩短距离（缩进到玩家附近）
- 透明化遮挡物：射线检测到障碍物时将其半透明化或替换材质

```
理想位置 = target.position + rotation * (-forward * distance)
射线检测：从目标到理想位置，如果碰到场景 → 相机位置 = 碰撞点前移一些
```

#### 11.2 第一人称相机

- 相机即角色眼睛位置
- 鼠标输入旋转：Pitch（上下，限制 -89度 ~ 89度 防止翻转）+ Yaw（左右）
- 头部晃动：走路/跑步时微小的相机位移和旋转
- FOV 变化：冲刺时增大 FOV 增强速度感

#### 11.3 轨道相机

用于策略游戏、编辑器、模型查看。

- 绕固定焦点旋转/缩放
- 输入：滚轮缩放、中键拖拽平移、右键拖拽旋转
- 关键：旋转用四元数，避免欧拉角导致的选择限制

#### 11.4 Cinemachine / 虚拟相机

Unity Cinemachine 或类似系统通过虚拟相机实现：
- 多相机优先级混合（跟随→瞄准→过场）
- Transposer：位置跟随模式
- Composer：画面构图（保持目标在屏幕特定位置）
- Noise：手持晃动效果
- Damping：各轴独立阻尼

---

### 十二、3D 特效

#### 12.1 粒子系统 (VFX Graph / Niagara / GPU Particles)

进阶 3D 粒子系统超越 2D 的要点：
- GPU 粒子：百万级粒子在 GPU 上模拟，远超 CPU 能力
- Mesh 粒子：每个粒子是 3D 模型而非 Billboard
- 条带粒子：粒子间连线形成拖尾、闪电、锁链
- 碰撞：粒子与场景碰撞反弹
- 力场：风力、旋涡、引力场影响粒子运动
- Sub-emitter：粒子死亡时触发新粒子系统（如火花→烟）

#### 12.2 后处理 (Post-Processing)

| 效果 | 原理 | 用途 |
|------|------|------|
| Bloom 泛光 | 提取亮部→模糊→叠加原图 | 光晕、魔法光芒、霓虹 |
| SSAO 环境光遮蔽 | 屏幕空间采样周围深度，计算遮蔽度 | 增强角落/缝隙阴影 |
| DOF 景深 | 根据深度模糊远近 | 聚焦效果、过场 |
| Motion Blur | 像素速度向量模糊 | 速度感 |
| Color Grading | LUT 查色表映射 | 风格化色调 |
| Vignette | 边缘压暗 | 聚焦中心、恐怖氛围 |
| Chromatic Aberration | RGB 通道错位 | 损伤效果、科幻感 |
| Tone Mapping | HDR→LDR 映射 | ACES/Filmic 更自然的亮度过渡 |

渲染顺序：
```
不透明物体 → 天空盒 → 透明物体 → 后处理 → UI
```

---

### 十三、WebGL 3D 优化

#### 13.1 Three.js（Stars 112,398）核心优化

Three.js 是 Web 3D 的事实标准库。

性能策略：
- 几何体合并 (BufferGeometryUtils.mergeGeometries)：合并静态 Mesh 减少 draw call
- InstancedMesh：渲染大量相同几何体（树木、石块、子弹壳），一次 draw call 渲染 N 个实例
- LOD (Level of Detail)：远处用低面模型
- 视锥剔除 (Frustum Culling)：自动跳过相机外的物体
- 材质/Shader 共享：同材质不同纹理用 Texture Atlas

#### 13.2 低多边形 (Low Poly) 策略

Web 3D 必须极致压缩面数：
- 角色：500~2000 三角面
- 道具：50~500 三角面
- 场景：10,000~50,000 三角面（全场景）
- 法线贴图 + 低模：用贴图欺骗光照细节
- 贴花 (Decal)：子弹孔、脚印等用贴花投影而非建模

#### 13.3 纹理优化

| 技术 | 说明 |
|------|------|
| 纹理图集 (Atlas) | 多张纹理合并为一张，减少状态切换 |
| MipMap | 预生成缩小纹理链，远处物体用低分辨率，减少显存和缓存缺失 |
| 压缩纹理 | Basis Universal 格式跨平台，GPU 原生解码 |
| POT 纹理 | 使用 2^n 尺寸（512/1024/2048），GPU 优化更好 |
| 纹理流式加载 | 先低清后高清，减少首屏等待 |

#### 13.4 WebGL 专项优化

- Draw Call：目标 < 100/帧（移动端 < 50）
- 状态排序：不透明前到后、透明后到前、按材质/纹理分组
- Geometry Instancing 代替逐个渲染
- requestAnimationFrame + 时间步长控制
- Web Worker 中执行寻路/AI 计算，主线程只做渲染
- OffscreenCanvas：Web Worker 中离屏渲染
- WebAssembly：物理/寻路等计算密集模块编译为 WASM
- 内存管理：显式 Dispose 几何体/纹理/材质，监控 JS Heap 和 GPU Memory

#### 13.5 Babylon.js（Stars 25,475）补充

Babylon.js 是 Three.js 的主要竞品，更加"引擎化"：
- 内置物理引擎集成
- GUI 系统
- 粒子编辑器
- PBR 材质开箱即用
- WebXR 支持
- 适合需要完整引擎功能但不想用 Unity/Unreal 的 Web 项目

---

### 十四、Cocos Creator 3D 抖音适配

#### 14.1 抖音小游戏环境

- 运行环境：字节跳动自研 JS 引擎，基于 V8 剪裁
- 限制：代码包 ≤ 20MB（主包 16MB + 分包），不支持 eval/new Function
- 渲染：Canvas/WebGL，iOS 上为 WKWebView → WebGL 性能有限
- 启动：要求首屏 < 3 秒

#### 14.2 Cocos Creator 3D 优化建议

1. 纹理压缩：使用 ETC2/ASTC，从 PNG 转换为 GPU 压缩格式，体积减少 70%+
2. 模型压缩：Draco 压缩 glTF，面数控制在移动端可接受范围
3. Draw Call：抖音小游戏建议 ≤ 30 DC
4. 分包加载：非首关场景放到分包
5. 自动合图：Cocos Creator 内置 Auto Atlas
6. LOD：3D 场景必须使用 LOD Group
7. 遮罩剔除：细粒度剔除弥补 WebGL 性能短板
8. GC 控制：避免每帧创建临时对象，使用对象池
9. 骨骼动画：使用 GPU Skinning，限制同时播放骨骼数量
10. 粒子系统：最大粒子数严格限制，复杂效果用序列帧替代

#### 14.3 性能基线

抖音小游戏建议目标（中低端机）：
- 帧率：30fps 保底，60fps 目标
- Draw Call：≤ 30
- 三角面：全场景 ≤ 30,000
- 骨骼动画同时播放：≤ 10
- 纹理内存：≤ 100MB
- 代码包：主包 ≤ 16MB

---

## 附录：GitHub 关键项目速查

| 项目 | Stars | 类型 |
|------|-------|------|
| godotengine/godot | 110,546 | 2D/3D 开源引擎 |
| mrdoob/three.js | 112,398 | Web 3D 渲染库 |
| pixijs/pixijs | 47,156 | 2D WebGL 渲染 |
| phaserjs/phaser | 39,607 | 2D Web 游戏框架 |
| BabylonJS/Babylon.js | 25,475 | Web 3D 引擎 |
| erincatto/box2d | 9,653 | 2D 物理引擎 |
| cocos/cocos-engine | 9,578 | 跨平台引擎 |
| piqnt/planck.js | 5,246 | Box2D JS 移植 |
| KilledByAPixel/LittleJS | 4,094 | 超轻量 HTML5 引擎 |

---

## 总结

- 2D 游戏的核心链路：Sprite/图集批处理 → TileMap 场景构建 → Box2D 物理 → 状态机行为 → UI 适配 → 对象池优化。框架按需选择：国内小游戏用 Cocos Creator，独立游戏用 Godot，纯 Web 用 Phaser/PixiJS。
- 3D 游戏的核心链路：四元数/矩阵数学 → 骨骼蒙皮动画/混合 → 碰撞检测管线（宽相→窄相→响应）→ 相机系统 → 后期特效 → 极致性能优化。Web 3D 首选 Three.js（灵活）或 Babylon.js（完整），移动端小游戏用 Cocos Creator 3D。
- 无论 2D 还是 3D，设计模式（Game Loop、对象池、状态机、命令模式、观察者）是工程质量的基石，性能优化（合批、LOD、剔除、纹理压缩、分包）是上线的保障。
