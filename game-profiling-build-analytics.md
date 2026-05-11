# 游戏性能分析 & 跨平台构建 & 数据分析

## 一、性能分析工具链

| 工具 | 平台 | 用途 | 命令 |
|------|------|------|------|
| RenderDoc | Win/Linux | 帧调试/GPU分析 | 注入进程→捕获帧→查看DrawCall/纹理 |
| NVIDIA Nsight | Win/Linux | GPU Trace/Shader调试 | nsys profile ./game |
| Tracy | Win/Linux | CPU/GPU实时追踪 | 代码插入ZoneScoped宏 |
| Optick | Win | CPU采样/帧分析 | 类似Tracy,UE内置 |
| PIX | Win/Xbox | DirectX调试 | GPU捕获+时序分析 |
| Instruments | Mac/iOS | 全栈分析 | Xcode自带 |

### Tracy 集成 (C++)
```cpp
#include <Tracy.hpp>
void GameLoop() {
    ZoneScoped;  // 自动追踪此函数
    {
        ZoneScopedN("Physics");
        physicsWorld->Update(dt);
    }
    {
        ZoneScopedN("AI");
        aiSystem->Update(dt);
    }
    FrameMark; // 标记帧结束
}
```

## 二、跨平台构建系统

### CMake + vcpkg (C++项目)
```cmake
cmake_minimum_required(VERSION 3.20)
project(MyGame)
find_package(SDL2 REQUIRED)
find_package(Vulkan REQUIRED)
add_executable(game src/main.cpp)
target_link_libraries(game SDL2::SDL2 Vulkan::Vulkan)
```

### 平台差异处理
```cpp
#ifdef _WIN32
    #include <windows.h>
#elif __APPLE__
    #include <CoreFoundation/CoreFoundation.h>
#elif __linux__
    #include <unistd.h>
#endif

// 路径统一用 /
std::filesystem::path assetPath = "assets/textures/hero.png";
```

### 构建矩阵
```
平台:      Win64 | macOS | Linux | Android | iOS
渲染:      DX12/Vulkan | Metal | Vulkan | Vulkan | Metal
架构:      x64 | x64/ARM64 | x64 | ARM64 | ARM64
包格式:    .exe/.msix | .app | .AppImage | .apk | .ipa
```

## 三、游戏数据分析

### 关键指标
```cpp
struct TelemetryEvent {
    string event;      // "level_start", "boss_kill"
    json properties;   // {level:3, weapon:"sword", time:45.2}
    uint64_t timestamp;
};

// 埋点
Telemetry::track("player_death", {
    {"level", currentLevel},
    {"cause", deathCause},
    {"playtime", sessionTime}
});
```

### 漏斗分析
```
进入游戏: 100%
→ 完成教程: 85%  (-15%流失)
→ 通过第1关: 70%  (-15%)
→ 通过第5关: 40%  (-30% ← 这里有问题!)
→ 付费: 5%
→ D7留存: 20%
```
