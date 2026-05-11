# Hermes 五大扩展集成报告

## 安装时间：2026-05-11

---

## 1. Superpowers — 软件工程方法论 (obra/superpowers, MIT)

> 14 个自动触发技能，强制执行测试驱动、计划驱动的开发流程

### 技能清单

| 技能 | 功能 | 触发时机 |
|------|------|---------|
| **using-superpowers** | Bootstrap 入口 | 每次对话开始 |
| **brainstorming** | Socratic 需求澄清 | 写代码前 |
| **writing-plans** | 拆解为 2-5 分钟任务 | 设计确认后 |
| **test-driven-development** | RED-GREEN-REFACTOR | 编码过程中 |
| **subagent-driven-development** | 子代理逐任务执行 | 计划确认后 |
| **executing-plans** | 批量执行+人工检查点 | 计划确认后 |
| **requesting-code-review** | 任务间代码审查 | 每个任务完成后 |
| **receiving-code-review** | 处理审查反馈 | 收到审查后 |
| **systematic-debugging** | 4阶段根因调试 | Bug 出现时 |
| **using-git-worktrees** | 隔离工作区+分支 | 设计确认后 |
| **finishing-a-development-branch** | PR/合并/清理 | 所有任务完成 |
| **verification-before-completion** | 验证后报告 | 任务完成前 |
| **writing-skills** | 制作/测试新技能 | 技能编写时 |
| **dispatching-parallel-agents** | 并行子代理 | 多独立任务 |

### 核心哲学
- TDD: 测试先于代码
- 系统化 > 拍脑袋
- 简化复杂度
- 证据 > 声明

### 安装位置
`~/.hermes/skills/superpowers/`

---

## 2. GBrain — 知识图谱大脑 (garrytan/gbrain, 14.7k⭐)

> Y Combinator 总裁 Garry Tan 的 Hermes Agent 大脑系统 —— 知识图谱 + PostgreSQL

### 技能（50+）

| 类别 | 技能 |
|------|------|
| 研究 | academic-verify, archive-crawler, article-enrichment, concept-synthesis, citation-fixer |
| 记忆 | brain-ops, brain-pdf, memory-layers, memory-ops, cold-start |
| 生产力 | briefing, daily-digest, ask-user, conventions, book-mirror |
| 阅读 | reading, rss-reader, rss-ingest, epub-reader, web-monitor, web-summarizer |
| 编程 | coding-agent, codex, opencode, claude-code, plan, spike |
| 内容 | ocr, youtube-transcript, newsletter, publishing |
| 元 | skill-manager, meta-cognition, growth-loop |

### 核心组件
- **Brain**: PostgreSQL + Qdrant 向量存储
- **Memory Layers**: 短期/中期/长期三层记忆
- **Embedding Recipes**: 5 种嵌入策略（语义/关键词/查询/摘要/跨域）
- **Evals**: 内置评估框架

### 安装位置
`~/.hermes/skills/gbrain/` (后台下载中)

---

## 3. Hermes Plugins — 23 个自治插件 (42-evey/hermes-plugins, AGPL-3.0)

### 自主与决策
| 插件 | 功能 |
|------|------|
| evey-autonomy | 核心自治引擎 |
| evey-council | 3模型辩论决策 |
| evey-delegate-model | 智能模型路由+4级回退 |

### 可观测性
| 插件 | 功能 |
|------|------|
| evey-telemetry | 结构化 JSON 日志 |
| evey-status | 统一状态检查 |
| evey-mqtt | MQTT 实时事件流 |
| evey-cost-guard | Langfuse 预算管控 |

### 质量与安全
| 插件 | 功能 |
|------|------|
| evey-reflect | 自纠错循环 |
| evey-validate | 幻觉检测 |
| evey-email-guard | 注入攻击筛查 |
| evey-sandbox | 沙箱代码执行 |

### 学习与记忆
| 插件 | 功能 |
|------|------|
| evey-learner | 经验学习 |
| evey-memory-adaptive | 记忆重要性评分+衰减 |
| evey-memory-consolidate | 夜间记忆整合 |
| evey-identity | 自更新 SOUL.md |

### 通信
| 插件 | 功能 |
|------|------|
| evey-bridge | Claude Code 双向通信 |
| evey-goals | 自主目标管理 |
| evey-digest | 日报汇编 |
| evey-research | 自动化研究管线 |

### 安装位置
`~/.hermes/plugins/`

---

## 4. Hermes Agent Self-Evolution — 进化引擎 (NousResearch, MIT, 3k⭐)

> DSPy + GEPA 自动进化技能、Prompt、工具描述

### 工作原理
```
读取技能 → 生成评估数据集 → GEPA 优化器（读执行轨迹）→ 候选变体 → 评估
→ 约束门禁（测试/尺寸/语义）→ 最佳变体 → PR
```

### 能力
| Phase | 目标 | 状态 |
|-------|------|------|
| 1 | 技能文件进化 | ✅ 已实现 |
| 2 | 工具描述进化 | 🔲 计划中 |
| 3 | 系统 Prompt 进化 | 🔲 计划中 |
| 4 | 代码实现进化 | 🔲 计划中 |

### 用法
```bash
python -m evolution.skills.evolve_skill --skill 技能名 --iterations 10
```

### 安装位置
`/root/hermes-agent-self-evolution/`

---

## 5. Awesome Hermes Agent — 生态索引 (0xNyk, 2.8k⭐)

> Hermes Agent 全生态系统导航地图

### 分类覆盖
- 官方资源（Hermes Agent / autonovel / paperclip / self-evolution）
- 社区技能（wondelai/skills / litprog / super-hermes / hermes-life-os）
- 插件系统（hermes-plugins / hermes-dojo / skill-marketplace）
- GUI 工具（hermes-workspace / mission-control）
- 部署方案（Docker / Kubernetes / 无服务器）

### 安装位置
`/root/awesome-hermes-agent/`

---

## 系统当前状态

```
Hermes 精装版 v2.0
├── 🧠 核心引擎
│   ├── SOUL.md (游戏建筑师身份)
│   ├── 10 Provider (916+ 模型)
│   └── 8 角色编排体系
├── 📚 技能生态
│   ├── 14 Superpowers (软件工程)
│   ├── 50+ GBrain (知识大脑)
│   ├── 48+ 自建技能 (游戏/动画/AI)
│   └── 5 ComfyUI GameForge 管线
├── 🔌 插件系统
│   └── 23 evey-* 插件 (自治/记忆/安全)
├── 🦾 进化引擎
│   └── DSPy + GEPA 自动优化
└── 🗺️ 生态地图
    └── Awesome Hermes 完整索引
```
