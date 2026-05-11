# 3D渲染管线实现 & 网络同步 & 游戏AI代码

## 一、PBR 渲染完整实现

### GBuffer 布局 (延迟渲染)
```
RT0: Albedo.rgb + Metallic.a     (RGBA8)
RT1: Normal.rgb + Roughness.a    (RGBA8)  
RT2: Emission.rgb + AO.a         (RGBA8)
DepthStencil: Depth32 + Stencil8

总带宽: 12 bytes/pixel @1080p = ~25MB
```

### 光照Pass (Compute Shader)
```hlsl
// Tile-Based Deferred Lighting
[numthreads(16, 16, 1)]
void CSLighting(uint3 tid : SV_DispatchThreadID) {
    // 1. 从GBuffer读取像素属性
    float3 albedo = gAlbedo[tid.xy].rgb;
    float metallic = gAlbedo[tid.xy].a;
    float3 normal = decodeOctahedron(gNormal[tid.xy].rg);
    float roughness = gNormal[tid.xy].b;

    // 2. 重建世界位置
    float depth = gDepth[tid.xy];
    float3 worldPos = reconstructWorldPos(tid.xy, depth);

    // 3. 遍历Tile内的灯光
    uint tileIdx = getTileIndex(tid.xy);
    float3 color = 0;
    for(uint i=tileStart[tileIdx]; i<tileStart[tileIdx+1]; i++) {
        Light light = gLights[i];
        color += evaluatePBR(albedo, metallic, roughness, normal, worldPos, light);
    }
    // 4. 环境光 (IBL)
    color += evaluateIBL(albedo, metallic, roughness, normal, worldPos);

    gOutput[tid.xy] = float4(color, 1);
}
```

### 阴影映射 (CSM级联)
```
级联0: 0-15m  → 512×512 shadow map
级联1: 15-50m → 512×512
级联2: 50-150m → 512×512
级联3: 150-500m → 512×512

选择级联: pixelDepth < cascadeDistances[i]
```

## 二、网络同步核心代码

### 快照插值
```cpp
struct Snapshot {
    uint32_t tick;
    std::vector<EntityState> entities;
};

class InterpolationSystem {
    Snapshot from, to;
    float time;

    void update(float dt, Snapshot newSnap) {
        if(newSnap.tick > to.tick) {
            from = to;
            to = newSnap;
            time = 0;
        }
        time += dt;
        float t = time / TICK_INTERVAL; // 0..1
        for(auto& entity : renderEntities) {
            auto& a = findInSnapshot(from, entity.id);
            auto& b = findInSnapshot(to, entity.id);
            entity.position = lerp(a.position, b.position, t);
        }
    }
};
```

### 客户端预测+和解
```
1. 输入→立即移动(预测)
2. 保存预测历史 [seq100:posA, seq101:posB, seq102:posC]
3. 收到服务器确认(seq=100, pos=posA')
4. 比较posA vs posA':
   - 误差<阈值→保持
   - 误差>阈值→回滚到seq100→重放seq101,102输入
```

## 三、游戏AI系统代码

### 行为树基础节点
```cpp
enum Status { SUCCESS, FAILURE, RUNNING };

class Selector : public Node { // 优先级选择
    Status tick() {
        for(auto& child : children) {
            Status s = child->tick();
            if(s != FAILURE) return s;
        }
        return FAILURE;
    }
};

class Sequence : public Node { // 顺序执行
    Status tick() {
        for(auto& child : children) {
            Status s = child->tick();
            if(s != SUCCESS) return s;
        }
        return SUCCESS;
    }
};
```

### 感知系统
```cpp
class PerceptionSystem {
    void update() {
        for(auto& ai : entities) {
            ai.canSeePlayer = false;
            // 视觉锥检测
            float angle = angleBetween(ai.forward, player.pos - ai.pos);
            if(angle < ai.fov/2 && distance(ai.pos, player.pos) < ai.sightRange) {
                // 射线检测
                if(!physics.raycast(ai.eyes, player.pos)) {
                    ai.canSeePlayer = true;
                    ai.lastKnownPos = player.pos;
                }
            }
            // 听觉检测
            if(player.noiseLevel > 0) {
                float hearDist = player.noiseLevel * ai.hearing;
                if(distance(ai.pos, player.pos) < hearDist) {
                    ai.heardSomething = true;
                }
            }
        }
    }
};
```
