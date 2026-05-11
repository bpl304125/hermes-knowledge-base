# 游戏内存管理 & 资产管线 & 存档 & Mod系统

## 一、游戏内存管理策略

### 内存分配器层级
```
Stack Allocator    — 帧内临时数据(标记/重置,O(1)释放)
Pool Allocator     — 固定大小对象(子弹/粒子,零碎片)
Linear Allocator   — 加载时分配,关卡结束释放
Free List          — 通用分配,适合变长数据

游戏专用: 每帧开始标记,帧结束重置Stack
         关卡加载用Linear,切换关卡整体释放
```

### 对象池实现
```cpp
template<typename T>
class ObjectPool {
    std::vector<T> pool;
    std::vector<size_t> freeList;
public:
    T* acquire() {
        if(freeList.empty()) {
            pool.emplace_back();
            return &pool.back();
        }
        size_t idx = freeList.back(); freeList.pop_back();
        return &pool[idx];
    }
    void release(T* obj) {
        obj->reset(); // 重置状态
        freeList.push_back(obj - pool.data());
    }
};
```

## 二、资产管线

### 纹理压缩
```
原始PNG(24MB) → ASTC 6x6(压缩16:1) → 1.5MB → GPU直接使用
工作流: Blender导出→glTF 2.0(Basis Universal压缩)→引擎导入
```

### 音频压缩
```
WAV(48kHz/24bit) → Ogg Vorbis q5 → MP3 128kbps
BGM: Ogg q5立体声(压缩10:1)
短SFX: MP3单声道(压缩20:1)
语音: Opus 32kbps(最高压缩比)
```

## 三、存档序列化

```cpp
class SaveManager {
    void save(SaveData& data) {
        json j;
        j["version"] = SAVE_VERSION;
        j["player"] = { {"pos",{data.x,data.y}}, {"hp",data.hp} };
        j["inventory"] = data.items;
        j["checksum"] = crc32(j.dump());

        string compressed = compress(j.dump());
        encrypt(compressed, SECRET_KEY);
        file.write(compressed);
    }
};
```

## 四、Mod系统架构

```
mods/
├── fantasy_mod/
│   ├── manifest.json  {"name":"Fantasy","version":"1.0","deps":[]}
│   ├── assets/        textures/models/替换资源
│   ├── scripts/       Lua/C# 脚本
│   └── data/          JSON 数据覆盖

加载顺序: 核心→依赖Mod→Mod自身
冲突: 后加载覆盖先加载
热重载: 文件监控→检测变化→重新加载Mod
```
