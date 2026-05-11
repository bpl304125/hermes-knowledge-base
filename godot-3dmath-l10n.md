# Godot 4 GDScript 实战 & 3D 数学速查

---

## 一、Godot 4 核心模式

### 节点生命周期
```gdscript
_ready()         — 节点就绪(一次性)
_process(delta)  — 每帧调用
_physics_process(delta) — 固定60Hz物理帧
_enter_tree()    — 进入场景树
_exit_tree()     — 离开场景树
```

### 信号系统 (解耦利器)
```gdscript
signal health_changed(new_health)
health_changed.emit(current_health)
# 连接: 编辑器拖线 或 health_changed.connect(_on_health_changed)
```

### 资源预加载 vs 动态加载
```gdscript
@export var scene: PackedScene      # 预加载(快,占内存)
var enemy = load("res://enemy.tscn") # 需要时加载
ResourceLoader.load_threaded_request("big_scene.tscn")  # 异步
```

## 二、3D 数学速查

### 向量运算
```
v1 + v2    = 位移叠加
v1 - v2    = 从v2到v1的方向
v1 * 标量   = 缩放
v1.dot(v2) = cos(夹角)*|v1|*|v2|  (同向>0, 垂直=0, 反向<0)
v1.cross(v2) = 垂直两向量的法向量 (右手定则)
v.normalized() = 单位向量(方向不变,长度=1)
```

### 四元数 (避免万向节锁)
```
Quaternion(axis, angle)  = 绕axis旋转angle弧度
q1 * q2                   = 组合旋转(q1后q2)
q.inverse()               = 反向旋转
slerp(q1, q2, t)          = 球面线性插值(平滑旋转)
```

### 常用变换
```gdscript
# 世界→局部
var local_pos = global_transform.affine_inverse() * world_pos
# 前方方向
var forward = -global_transform.basis.z
# 看向目标
look_at(target_position, Vector3.UP)
# 射线检测
var result = space_state.intersect_ray(origin, origin + dir * 100)
```

## 三、游戏本地化

### CSV→多语言
```
key,        zh_CN,          en_US,          ja_JP
menu_start, 开始游戏,        START,          ゲーム開始
menu_quit,  退出,           QUIT,           終了
```

### Godot 翻译
```
项目设置 → Localization → 添加CSV → tr("menu_start")
```
