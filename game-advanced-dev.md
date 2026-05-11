# 游戏开发高级技术深度研究

---

## 一、Shader 编程实战

### 1.1 着色器基础管线

```
顶点着色器 → 曲面细分 → 几何着色器 → 光栅化 → 片段着色器 → 输出合并
```

### 1.2 GLSL 实战：PBR 片段着色器

```glsl
// Cook-Torrance BRDF
float DistributionGGX(vec3 N, vec3 H, float roughness) {
    float a = roughness * roughness;
    float a2 = a * a;
    float NdotH = max(dot(N, H), 0.0);
    float denom = NdotH * NdotH * (a2 - 1.0) + 1.0;
    return a2 / (PI * denom * denom);
}

float GeometrySchlickGGX(float NdotV, float roughness) {
    float k = (roughness + 1.0) * (roughness + 1.0) / 8.0;
    return NdotV / (NdotV * (1.0 - k) + k);
}

float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness) {
    return GeometrySchlickGGX(max(dot(N, V), 0.0), roughness) *
           GeometrySchlickGGX(max(dot(N, L), 0.0), roughness);
}

vec3 fresnelSchlick(float cosTheta, vec3 F0) {
    return F0 + (1.0 - F0) * pow(max(1.0 - cosTheta, 0.0), 5.0);
}
```

### 1.3 卡通渲染 (Cel/Toon Shading)

```
核心技巧: 量化漫反射为离散阶梯
├── Step函数: 漫反射 > 阈值 → 亮色，否则 → 暗色
├── 多级色阶: smoothstep 生成柔和过渡带
├── 描边: Sobel深度边缘检测 或 背面膨胀法
└── 高光: Blinn-Phong + step(specular > 0.99)
```

**Toon Ramp 技术**: 1D纹理查找表替换连续光照：
```glsl
float NdotL = dot(normal, lightDir);
float diffuse = texture(rampTexture, vec2(NdotL * 0.5 + 0.5, 0.5)).r;
```

### 1.4 常见特效 Shader

| 效果 | 原理 | 关键 |
|------|------|------|
| **溶解(Dissolve)** | noise纹素 < 阈值 → discard | Perlin/Voronoi噪声 |
| **全息(Hologram)** | 扫描线 + 边缘发光 + 半透明 | sin(distortedPos.y + time) |
| **水面** | Gerstner波叠加 + 法线扰动 + 菲涅尔 | 多层正弦波累加 |
| **力场护盾** | 菲涅尔边缘发光 + 六边形网格 + 相交高亮 | 深度比较+sin(tiling) |
| **热浪扭曲** | GrabPass → 噪声UV偏移 | simplex noise偏移 |


## 二、程序化生成

### 2.1 噪声算法家族

| 噪声 | 特点 | 性能 | 应用 |
|------|------|------|------|
| **Perlin** | 经典梯度噪声 | 快 | 地形基础 |
| **Simplex** | 无方向性伪影 | 更快 | Perlin升级版 |
| **Voronoi/Worley** | 细胞状图案 | 中 | 裂纹/石板/生物 |
| **FBM(分形布朗)** | 多层叠加(octaves) | Perlin×N | 云/山细节 |
| **Domain Warping** | FBM+坐标扭曲 | 慢 | 异世界地形 |

```
基础层(Low Freq) → f=1, a=1
   + 第二层 → f=2, a=0.5
      + 第三层 → f=4, a=0.25
         = FBM结果
```

### 2.2 地形生成管线

```
Perlin FBM高度图 → 侵蚀模拟 → 生物群系映射 → 植被散布 → 道路/河流
```

**侵蚀模拟**: 水力侵蚀(雨滴→径流→沉积) + 热力侵蚀(陡坡崩塌)

### 2.3 地牢生成算法

| 算法 | 输出 | 适合 |
|------|------|------|
| **BSP树** | 矩形房间+走廊 | 经典Roguelike |
| **随机游走** | 洞穴状隧道 | 自然地下城 |
| **细胞自动机** | 有机洞穴 | 类Minecraft洞穴 |
| **WFC(波函数坍缩)** | 带约束的规则生成 | 建筑/城镇 |
| **Delaunay三角剖分** | 房间图+最短走廊连接 | 结构化关卡 |

### 2.4 城市/建筑生成

```
WFC核心: 
1. 定义合法邻接规则(建筑A左边可以是B/C)
2. 从熵最小格开始坍缩
3. 传播约束更新邻居可能性
4. 重复直至全部确定
```

---

## 三、游戏 AI 深度

### 3.1 行为树实现

**核心节点类型**:
```
组合节点(Composite):
├── Selector (优先级选择): 从左到右，成功则停止
├── Sequence (序列): 从左到右，全部成功才成功
└── Parallel (并行): 多子节点同时运行

装饰节点(Decorator):
├── Inverter: 取反子节点结果
├── Repeater: 重复执行N次
├── UntilFail/UntilSuccess
└── Cooldown: 冷却时间内跳过

条件节点(Condition):
├── HasTarget / IsHealthLow / CanSeePlayer

动作节点(Action):
├── MoveTo / Attack / Patrol / Flee / UseSkill
```

### 3.2 GOAP 规划系统

```
Agent状态:  {health:30, hasAmmo:true, enemyDistance:50}
目标:       {health>50, enemyDead:true}
可用动作:
├── FindCover:  cost=1, pre={enemyInSight}, post={inCover:true}
├── Heal:       cost=2, pre={inCover, hasHealthPack}, post={health:100}
├── Shoot:      cost=1, pre={hasAmmo,enemyDistance<100}, post={enemyDead:true}

A*搜索状态空间 → 最优动作序列
```

### 3.3 决策方案对比

| 方案 | 复杂度 | 可预测性 | 可维护性 | 适合 |
|------|--------|---------|---------|------|
| 有限状态机 | 低 | 高 | 中 | 简单敌人 |
| 分层状态机 | 中 | 高 | 好 | 中复杂AI |
| 行为树 | 中 | 中-高 | 优秀 | 中等AI标准方案 |
| GOAP | 高 | 低(涌现) | 好 | 需要动态行为的AI |
| 效用AI | 高 | 低 | 优秀 | 多因素权衡决策 |
| 机器学习 | 极高 | 极低 | 差 | 特定问题(导航/瞄准) |

### 3.4 NavMesh 寻路

```
Recast构建:
体素化 → 过滤可行走区域 → 划分区域 → 生成轮廓 → 三角剖分 → NavMesh

Detour查询:
FindNearestPoly → FindPath(A*) → 路径平滑(Funnel Algorithm) → 转向速度控制
```

---

## 四、GPU 粒子与 VFX

### 4.1 GPU 粒子系统

**优势**: CPU粒子(CPU更新→上传GPU→渲染) → GPU粒子(GPU全程计算)，百万级粒子实时

**Transform Feedback/Compute Shader**:
```
Compute Shader每帧:
├── 位置 += 速度 * dt
├── 速度 += (重力 + 风力 + 湍流) * dt
├── 生命 -= dt
├── 如果生命≤0: 重置粒子
└── 输出到渲染Buffer
```

### 4.2 后处理效果栈

```
场景渲染 → [Bloom] → [SSAO] → [DOF] → [Motion Blur] → [Color Grading] → [Vignette] → 输出
```

| 效果 | 算法 | GPU成本 |
|------|------|---------|
| **Bloom** | 亮度提取→高斯模糊(降采样)→叠加 | 低-中 |
| **SSAO** | 深度法线重建→半球采样→模糊 | 中 |
| **景深(DOF)** | CoC计算→模糊散景→合成 | 中 |
| **运动模糊** | 速度Buffer→方向模糊 | 低 |
| **色差** | RGB通道偏移(边缘) | 极低 |
| **色调映射** | ACES/Reinhard/Filmic | 极低 |
| **LUT调色** | 3D查找表颜色映射 | 极低 |
