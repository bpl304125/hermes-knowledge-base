# 音频中间件 & 着色器优化 & 云游戏

## 一、音频中间件深度

### FMOD vs Wwise 函数对比
```
FMOD Studio API:
  FMOD::System::createSound("explosion.wav", ...)
  FMOD::System::playSound(sound, channelGroup, &channel)
  channel->set3DAttributes(&pos, &vel)
  channel->setVolume(0.8f)

Wwise:
  AK::SoundEngine::RegisterGameObj(GAME_OBJ_ID_PLAYER, "Player")
  AK::SoundEngine::SetPosition(GAME_OBJ_ID_PLAYER, transform)
  AK::SoundEngine::PostEvent("Play_Explosion", GAME_OBJ_ID_PLAYER)
```

### 性能基准
| 操作 | CPU占用 | 内存 |
|------|---------|------|
| 单声道3D音源 | <0.1ms | ~100KB |
| 立体声BGM流式 | <0.2ms | 流式缓冲 |
| 混响效果器 | ~0.5ms | 额外 |
| 100并发音源 | <5ms | ~10MB |

## 二、着色器性能优化

```
移动端GPU友好:
✓ mediump精度(片段着色器)
✓ 纹理采样<4次/像素
✓ 避免discard(破坏Early-Z)
✓ 分支统一(避免if动态条件)
✓ MipMap + 各向异性过滤

桌面端GPU:
✓ compute shader预处理
✓ 延迟渲染GBuffer压缩
✓ HZB遮挡查询
```

## 三、云游戏技术栈

| 方案 | 延迟 | 成本 |
|------|------|------|
| NVIDIA GeForce NOW | <30ms | $10/月 |
| Xbox Cloud Gaming | <40ms | $15/月 |
| 自建WebRTC+GPU服务器 | <20ms | 高 |
| WebRTC游戏流 | <50ms | 中 |
