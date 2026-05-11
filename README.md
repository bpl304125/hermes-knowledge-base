# Hermes AI 知识体系

> 由 Hermes Agent 系统化学习 18 个平台/仓库生成 | 2026-05-11

---

## 一、核心概念与关键术语

### 知识工程层

| 术语 | 定义 | 来源 |
|------|------|------|
| **RAG** (检索增强生成) | 文档→分割→向量化→检索→生成的流水线，减少大模型幻觉 | MaxKB, WeKnora, LangChain |
| **Knowledge Materialization** | 从 LLM 中系统性地提取、结构化知识，构建可查询知识库 | GPTKB (ACL 2025) |
| **Knowledge Graph** | 代码/SQL/文档→节点-边关系图，Leiden 算法社区发现 | Graphify (46k⭐) |
| **MCP** (Model Context Protocol) | 标准化工具调用协议，Agent 发现和使用外部工具 | MaxKB, GameCodex |
| **Agentic Workflow** | 工作流引擎驱动的智能体编排，条件分支+循环 | MaxKB |
| **Deep Agents** | 内置规划/子代理/文件系统的更高层 Agent 包 | LangChain |
| **Vectorization** | 文本自动分割+向量化，实现语义检索 | MaxKB, WeKnora |
| **Semantic Retrieval** | 基于语义相似度的文档召回，非关键词匹配 | WeKnora |
| **Tool-Use** | Agent 调用外部工具（API/数据库/文件系统）的能力 | LangChain, MaxKB |

### 算法与编程层

| 术语 | 定义 | 来源 |
|------|------|------|
| **Project-Based Learning** | 通过构建数十个实战项目来学习编码 | freeCodeCamp |
| **Algorithm Implementation** | 算法从理论到代码的系统实现 | TheAlgorithms/Python (220k⭐) |
| **Self-Paced Curriculum** | 自定节奏的线性课程体系 | freeCodeCamp, DataWhale |

---

## 二、知识逻辑关系

```
                    ┌─────────────────────────────┐
                    │      AI Agent 应用层          │
                    │  (智能客服/企业知识库/学术研究)  │
                    └─────────────┬───────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            │                     │                     │
    ┌───────▼───────┐    ┌───────▼───────┐    ┌───────▼───────┐
    │  Agent 工程    │    │  知识管理      │    │  知识图谱      │
    │ LangChain     │    │ MaxKB/WeKnora │    │ GPTKB/Graphify│
    │ (编排框架)     │    │ (RAG 平台)     │    │ (结构化知识)   │
    └───────┬───────┘    └───────┬───────┘    └───────┬───────┘
            │                     │                     │
            └─────────────────────┼─────────────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │       基础能力层              │
                    │  算法(TheAlgorithms)          │
                    │  编程(freeCodeCamp/DataWhale) │
                    │  文档(CSDN/free-books)        │
                    └─────────────────────────────┘
```

**因果链**: 算法基础 → 编程能力 → Agent 框架 → RAG/知识图谱 → 企业级应用

---

## 三、方法论原则

### 原则 1：RAG 优先，后 Agent 增强
先用 RAG 管道解决幻觉问题，再引入 Agent 工作流做复杂编排。

### 原则 2：知识结构化是效率杠杆
非结构化文档→知识图谱/向量索引，检索效率提升 10-50 倍。

### 原则 3：项目驱动，认证验证
构建项目→获得认证→求职。freeCodeCamp/DataWhale 共同理念。

### 原则 4：MCP 标准化工具接入
一次性 MCP 接入，所有 Agent 共享工具。GameCodex 已接入 950+ 游戏开发文档。

### 原则 5：开源社区杠杆
公共知识库 + 社区贡献 = 指数级价值增长。

---

## 四、平台速查表

| 平台 | 规模 | 核心功能 | 最佳场景 | 局限性 |
|------|------|---------|---------|--------|
| LangChain | 136k⭐ | Agent 工程框架 | 自定义 Agent、多模型编排 | 学习曲线陡，迭代快 |
| MaxKB | 20.9k⭐ | 企业级 Agent 平台 | 企业知识库、智能客服 | GPL 协议，Python生态 |
| WeKnora | 14.5k⭐ | 文档→可查询RAG | 微信生态知识管理 | 腾讯绑定 |
| Graphify | 46.2k⭐ | 代码→知识图谱 | 代码库理解、架构可视化 | 需AI编码助手配合 |
| GPTKB | ACL 2025 | LLM知识物化 | 学术研究 | 学术阶段 |
| freeCodeCamp | 388k⭐ | 免费编程教育 | 零基础学编程 | 偏Web，无中文 |
| DataWhale | 开源社区 | AI学习路线 | AI入门、中文社区 | 高级内容少 |
| TheAlgorithms | 220k⭐ | 算法实现全集 | 面试准备、教学 | 只Python |
| free-books | 388k⭐ | 免费编程书 | 自学参考 | 需筛选质量 |
| CSDN | 中文最大 | 开发者社区 | 中文技术文档 | 内容质量参差 |
| GameCodex | 小社区 | 游戏开发AI助手 | 游戏开发辅助 | 文档手动维护 |
| 百度学术 | - | 中文论文检索 | 中文学术搜索 | 国际覆盖不足 |
| 创新树 | - | 创新知识平台 | AI素养教育 | 内容有限 |
| 超星闻道 | - | 科学导航 | 学术资源发现 | 高校绑定 |

---

## 五、可用 AI Provider

| # | 服务 | 模型数 | 端点 |
|---|------|--------|------|
| 1 | OpenRouter | 365 | openrouter.ai/api/v1 |
| 2 | 阿里百炼 | 239 | dashscope.aliyuncs.com |
| 3 | 百度千帆 | 183 | qianfan.baidubce.com/v2 |
| 4 | 硅基流动 | 102 | api.siliconflow.cn/v1 |
| 5 | 腾讯混元 | 40 | api.hunyuan.cloud.tencent.com/v1 |
| 6 | Kimi | 9 | api.moonshot.cn/v1 |
| 7 | 小米MiMo | 9 | api.xiaomimimo.com/v1 |
| 8 | 智谱GLM | 7 | open.bigmodel.cn/api/paas/v4 |
| 9 | MiniMax | M2.7等 | api.minimax.chat/v1 |
| 10 | DeepSeek | 2 | api.deepseek.com/v1 |
