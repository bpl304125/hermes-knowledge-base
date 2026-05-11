# UE5核心技术 & GPU编程 & 动画混合

## 一、UE5 Nanite (虚拟几何体)

```
原理:
1. 导入高模→集群化(128三角形/集群)
2. 构建BVH层级→LOD自动生成
3. 运行时: 屏幕空间误差<1像素→选对应LOD
4. GPU Driven: 剔除+LOD选择全在GPU完成
5. 光栅化: 软光栅(像素<16) + 硬光栅(像素>16)

限制: 不透明刚体、不支持WPO(世界位置偏移)、骨骼动画需传统管线
```

## 二、UE5 Lumen (动态全局光照)

```
Surface Cache → 网格体素化 → 光照传播体积
Card Trace: 屏幕空间射线(SW) + Mesh Distance Field(HW)
Final Gather: 降噪+时空累积 → 高质量间接光照

性能: 30fps目标需关掉硬件光追(Software mode)
```

## 三、GPU Compute实际应用

```hlsl
// GPU 粒子更新
[numthreads(256, 1, 1)]
void UpdateParticles(uint3 tid : SV_DispatchThreadID) {
    Particle p = gParticles[tid.x];
    if(p.life <= 0) { p = spawnNewParticle(tid.x); }

    p.velocity += gGravity * gDeltaTime;
    p.velocity += gWind * gDeltaTime;
    p.position += p.velocity * gDeltaTime;
    p.life -= gDeltaTime;

    gParticles[tid.x] = p;
}
// 256线程×N组 → 百万粒子实时
```

## 四、动画混合技术

### Blend Space 2D
```
横轴: 速度(-300~600 cm/s)  → 后退/静止/慢走/跑/冲刺
纵轴: 转向(-180~180度)     → 左转90°/直行/右转90°

从4个角动画插值:
finalPose = lerp(lerp(TL,TR,speed), lerp(BL,BR,speed), angle)
```

### 动画层 (Layered Blending)
```
Base层(全身): 奔跑动画
Upper层(上半身,遮罩): 射击动画
Additive层: 呼吸微动 (+0.03强度)

最终骨骼 = Base + (Upper × 遮罩权重) + Additive
```

### IK骨骼修正
```
脚部IK: 射线检测地面 → 调整脚位置(CCD/FABRIK)
手部IK: 武器握持点 = IK目标
脊柱IK: 瞄准时自动调整上半身朝向
```

## 五、开放世界流式加载

```
世界分区: 512m×512m Chunk
加载距离: 玩家周围3×3 Chunk完整加载
预加载: 移动方向预测→提前2-3 Chunk
卸载: 5×5范围外的Chunk异步释放

内存预算: 常驻2GB, 流式4GB, 总共6GB@PC
```
