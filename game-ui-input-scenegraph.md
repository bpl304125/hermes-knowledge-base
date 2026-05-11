# 游戏UI & 输入系统 & 场景图优化

## 一、Dear ImGui 游戏内UI集成

### 渲染循环集成
```cpp
// 初始化
ImGui::CreateContext();
ImGui_ImplSDL3_InitForOpenGL(window, gl_context);
ImGui_ImplOpenGL3_Init("#version 330");

// 游戏循环
while(running) {
    ImGui_ImplOpenGL3_NewFrame();
    ImGui_ImplSDL3_NewFrame();
    ImGui::NewFrame();

    // 游戏UI面板
    ImGui::Begin("Debug");
    ImGui::Text("FPS: %.1f", 1.0f/deltaTime);
    ImGui::SliderFloat3("Player Pos", &pos.x, -100, 100);
    ImGui::Checkbox("Wireframe", &wireframe);
    ImGui::End();

    // 渲染游戏...
    ImGui::Render();
    ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
}
```

### 编辑器模式集成
```cpp
// Unity风格 Hierarchy/Inspector/Console
DockSpace → 
  ├── Scene View (游戏画面)
  ├── Hierarchy (场景树节点列表)
  ├── Inspector (选中对象属性)
  ├── Console (日志输出)
  └── Asset Browser (资源浏览)
```

## 二、输入系统架构

### 动作映射 + 多设备
```cpp
InputMap {
    "Jump":  [Space, Gamepad_A, Touch_RightHalf],
    "Shoot": [MouseLeft, Gamepad_RT, Touch_LeftHalf],
    "MoveX": [AD_Keys, Gamepad_LeftStickX, Touch_DragX],
    "MoveY": [WS_Keys, Gamepad_LeftStickY, Touch_DragY],
};

// 设备热插拔
InputSystem::onDeviceChanged = [](DeviceEvent e) {
    if(e.type == CONTROLLER_CONNECTED) showGamepadUI();
    if(e.type == CONTROLLER_DISCONNECTED) showPauseMenu();
};
```

### 输入缓冲队列 (格斗游戏用)
```cpp
InputBuffer buffer(10); // 10帧窗口
buffer.push(InputEvent::LP, frame5);
buffer.push(InputEvent::LP, frame7);
buffer.push(InputEvent::LK, frame9);
// 检测到 LP→LP→LK → 触发特殊技
if(buffer.matchSequence({LP, LP, LK})) executeSpecial();
```

## 三、场景图优化

### 空间分割加速
```
场景树有10000节点 → 每帧遍历太慢

方案1: 八叉树
root → 8个子节点 → 每子节点再8分 → 直到叶子(≤16对象)
查询: O(log N) 替代 O(N)

方案2: 场景图层
StaticLayer (不动物体,合并Mesh)
DynamicLayer (移动物体,独立渲染)
UILayer (永远最前,单独Pass)
```

### 视锥剔除快速版
```cpp
// AABB vs 6个视锥面
bool isVisible(const AABB& box, const Frustum& frustum) {
    for(int i=0; i<6; i++) {
        // 如果AABB完全在某个平面外侧 → 不可见
        if(frustum.planes[i].distance(box.center) + box.radius < 0)
            return false;
    }
    return true; // 与所有平面相交 → 可见
}
```
