# anet.chat

人类和多位 AI persona 共享一块 Excalidraw 画板做实时协作脑暴的实验环境。

## 架构（v5）

```
┌─────────────────────────────────────────────────────┐
│ Browser: http://127.0.0.1:3000                      │
│  - Excalidraw 画板（标题 anet.chat）                 │
│  - 6 个预装 libraries（AWS / Azure / Stick figs / …）│
│  - 左上角 "Join Agent Network" → agentnetwork.org.cn │
└──────────────────┬──────────────────────────────────┘
                   │ WebSocket + REST
                   ▼
┌─────────────────────────────────────────────────────┐
│ mcp-excalidraw-canvas (Express + ws + 内存元素表)    │
│   /api/elements POST/PUT/DELETE                     │
│   /api/elements/clear                               │
│   ws://canvas:3000/  广播 element_created/updated/…  │
└──────────────────▲──────────────────────────────────┘
                   │ HTTP REST
                   │
┌─────────────────────────────────────────────────────┐
│ anet-souls (Python 48MB 容器，我手写)                │
│  ┌────────────────────────────────────────────────┐ │
│  │ Scheduler: A@:03/:37  B@:17/:45  C@:25/:53     │ │
│  │ Curator: 每 5 round 出场，A/B/C 暂停            │ │
│  │ Re-moderator: 每 10 round 重选 3 灵魂           │ │
│  │ 重叠保护: auto-shift down 50px ×8 / drop        │ │
│  │ 空形状拒绝: rectangle/ellipse/diamond 必带 text  │ │
│  └────────────────────────────────────────────────┘ │
│   每个 agent prompt = persona SKILL.md + AGENT.md   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
        MiniMax /v1/messages (Anthropic 兼容)
```

## 人才池（personas）

| Slug | 名字 | 色 | SKILL.md 来源 |
|---|---|---|---|
| feynman  | Richard Feynman   | #fa5252 红 | github.com/alchaincyf/feynman-skill |
| munger   | Charlie Munger    | #1c7ed6 蓝 | github.com/alchaincyf/munger-skill |
| karpathy | Andrej Karpathy   | #37b24d 绿 | github.com/alchaincyf/karpathy-skill |
| musk     | Elon Musk         | #ff8c00 橙 | github.com/alchaincyf/elon-musk-skill |

未来加教授：在 `refs/<slug>-skill/` 放 SKILL.md，往 `orchestrator/personas.json` 追加一条即可。

## 启动

```bash
# 1. 启 canvas + MCP（前者就是画板，后者目前未被调）
cd refs/mcp_excalidraw && docker compose --profile full up -d

# 2. 启协作脑
cd /data/projs/anetchat && docker compose --env-file .minimax.env up -d --build

# 3. 浏览器打开
open http://127.0.0.1:3000
```

`.minimax.env` 格式：
```
ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic
ANTHROPIC_API_KEY=sk-...
ANTHROPIC_MODEL=MiniMax-M2.7-highspeed
```

## 调研文档

- [docs/C001-excalidraw.md](docs/C001-excalidraw.md) — Excalidraw 内部架构
- [docs/C002-mcp_excalidraw.md](docs/C002-mcp_excalidraw.md) — mcp_excalidraw 服务深析
- [docs/C003-hermes-agent.md](docs/C003-hermes-agent.md) — Hermes Agent Kanban + Swarm 调研
- [docs/C004-nuwa-skill.md](docs/C004-nuwa-skill.md) — Nuwa 蒸馏方法论调研

## 目录

```
anetchat/
├── orchestrator/             ← 我手写的协调器
│   ├── main.py               ← 1100+ 行 asyncio 调度核
│   ├── AGENT.md              ← 注入到每个 agent 的通用规范
│   ├── personas.json         ← 人才池注册表（可扩展到 40+）
│   └── Dockerfile
├── docker-compose.yml        ← souls 服务
├── patches/mcp_excalidraw/   ← 我们对上游 mcp_excalidraw 的定制
├── docs/                     ← C001-C004 调研文档
└── refs/                     ← 4 个 persona skill + Excalidraw + Hermes 等 (gitignored)
```

## 已知局限（v5）

- Hermes Docker 镜像本地有但**未使用**——anet-souls 是手写薄壳替代
- mcp_excalidraw 的 **MCP 协议层未使用**——直接走 canvas REST
- mcp_excalidraw 的 **SKILL.md 设计指南未注入** agent 提示词（v6 路线图）

详细对比见 docs/。
