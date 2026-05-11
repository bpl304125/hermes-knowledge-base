# Shader 实战 & Game Feel & Web 游戏变现

## 一、GLSL Shader 速查

```glsl
// 顶点着色器
gl_Position = projection * view * model * vec4(pos, 1.0);

// 菲涅尔效果(边缘发光)
float fresnel = pow(1.0 - abs(dot(normal, viewDir)), 3.0);

// 卡通着色(色阶量化)
float diffuse = dot(normal, lightDir) * 0.5 + 0.5;
diffuse = floor(diffuse * steps) / steps;

// 全息扫描线
float scanline = sin(uv.y * 200.0 + time * 10.0) * 0.1;

// 溶解效果
float noise = texture(noiseTex, uv).r;
if(noise < dissolveAmount) discard;
```

## 二、Game Feel 手感清单

### 每个动作必须有: 视觉反馈 + 音效 + 屏幕效果
```
跳跃: 挤压拉伸(0.1s) + "boing" + 微震
攻击: 冻结帧(0.05s) + 挥砍音 + 命中火花粒子  
受击: 闪白(0.1s) + 屏幕震动(0.3) + 击退
死亡: 慢动作(0.3x) + 径向模糊 + 低频轰隆
收集: 弹跳动画(easeOutBack) + 音阶上升 + 数字跳动
```

### 数值设计: Coyote Time 100ms | Jump Buffer 150ms | 可变跳跃高度 | 杀敌冻结帧80ms

## 三、Web 游戏变现

| 平台 | 分成 | 适合 |
|------|------|------|
| itch.io | 0-30%(自定) | 独立/实验 |
| CrazyGames | 50-70%分成 | HTML5休闲 |
| Poki | 分成+买断 | 休闲/儿童 |
| GamePix | 分成 | HTML5 |
| Newgrounds | 社区驱动 | 独立 |
