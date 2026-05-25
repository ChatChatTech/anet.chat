# C005 — Hermes Multi-Agent Integration（feat/hermes-multi-agent 分支）

> 当前 main 分支用的是 anet-souls（手写 200 行 Python 协调器）。
> 本分支重做：**真起 Hermes，真用 mcp_excalidraw 的 MCP 协议，按 Hermes 的 Swarm/Kanban 范式建多 sub-agent**。
> 目标：为未来 40+ 教授扩展打好框架。

调研基础参见 [C003-hermes-agent.md](./C003-hermes-agent.md)。

---

## 1. 与 anet-souls 的对比

| 维度 | anet-souls (main) | hermes-based (this branch) |
|---|---|---|
| 调度核 | 我手写 asyncio + slot scheduler | Hermes cron scheduler |
| Agent 状态 | 内存 dict | Hermes Kanban SQLite（持久化） |
| 多 agent 模型 | 3 个并发 LLM 调用 | Hermes Swarm（root → workers → verifier → synthesizer） |
| 是否用 MCP | ❌ REST 直连 | ✅ Hermes spawn mcp_excalidraw stdio MCP |
| 是否用上游 SKILL.md | v6 已注入 system prompt | ✅ + 真正调 MCP 工具 |
| 镜像体积 | 48MB | 8.5GB (Hermes) |
| Profile 数量 | 4 | 5（多一个 curator） |
| 扩展到 40 个教授 | 改 personas.json 即可 | 多 `hermes profile create` 命令 + 多 SOUL.md |

---

## 2. 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│ Browser: http://127.0.0.1:3000                              │
│ Excalidraw canvas + 6 预装 libraries                         │
└────────────────────┬────────────────────────────────────────┘
                     │ WebSocket + REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ mcp-excalidraw-canvas  (REST + ws server, 内存元素表)        │
│ mcp-excalidraw-mcp     (stdio MCP, NOW REALLY CONNECTED)    │
└────────▲────────────────────────────────────┬───────────────┘
         │                                    │
         │ stdio (subprocess spawned by Hermes)│ REST
         │                                    │
┌────────┴────────────────────────────────────┴───────────────┐
│ anet-hermes-gateway  (nousresearch/hermes-agent:latest)     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 5 profiles (each with SOUL.md):                        │ │
│  │   feynman / munger / karpathy / musk / curator         │ │
│  │ mcp_servers: { excalidraw: { command: node, ... } }    │ │
│  │ cron jobs: 4 个 persona x 2 fires/hour                  │ │
│  │ Kanban Swarm: root → workers → verifier → synthesizer  │ │
│  │ /v1/runs REST API on :8642 (bearer auth)               │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────────────▲────────────────────────────┘
                                 │ POST /v1/runs
                                 │
┌────────────────────────────────┴────────────────────────────┐
│ anet-hermes-bridge  (~250 lines python)                     │
│  - polls canvas every 3s                                    │
│  - WAITING_FOR_QUESTION ↔ ACTIVE 状态机                      │
│  - 每秒检查 slot 触发条件，匹配则 POST /v1/runs            │
│  - 每 5 round 触发 curator                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 关键设计抉择

### 3.1 为什么仍需 hermes-bridge 这个 sidecar？

Hermes 本身**没有画板 watcher**——它不知道"画布上多了一个人类元素就要触发讨论"。Hermes 的输入要么是平台消息（Slack/Telegram/Discord）要么是 cron。

我们用最小 sidecar 把"画布事件"翻译成"Hermes REST 调用"，让 Hermes 仍然按它的标准模式工作。

### 3.2 为什么 Hermes 内的 mcp_excalidraw 用 stdio 而不是 HTTP？

Hermes 的 MCP 集成更成熟的是 stdio 模式。`mcp_excalidraw/dist/index.js` 就是 stdio MCP server，spawn 即用。HTTP 模式我们的 mcp_excalidraw 也支持，但 stdio 隔离性更好（每个 profile run 自己的子进程）。

### 3.3 curator 为什么是独立 profile 而不是 sub-agent？

Hermes 的 sub-agent 模式（delegate_task）需要父 agent 主动 call。我们的 curator 是**周期触发**的整理工作，bridge 直接按 round_count 触发更简单。后续 v2 可以让 orchestrator profile 决定是否 delegate to curator。

---

## 4. 文件清单

```
hermes/                                     ← 配置 + 5 profiles，bind 到 /opt/data
├── config.yaml                             ← model + mcp_servers + delegation
└── profiles/
    ├── feynman/SOUL.md                     ← 红色，第一性原理 + cargo cult
    ├── munger/SOUL.md                      ← 蓝色，多元思维 + 逆向 + Lollapalooza
    ├── karpathy/SOUL.md                    ← 绿色，march of 9s + Software 3.0
    ├── musk/SOUL.md                        ← 橙色，物理 first principles + 5 步算法
    └── curator/SOUL.md                     ← 灰色，整理画板（不参与讨论）

hermes-bridge/                              ← sidecar
├── main.py                                 ← 250 行 watcher + scheduler
└── Dockerfile                              ← python:3.12-slim + httpx

docker-compose.hermes.yml                   ← 2 个服务（gateway + bridge）
docs/C005-hermes-integration.md             ← 本文件
```

---

## 5. 启动步骤（计划，未实测）

```bash
# 1. canvas 仍由 main 分支的 compose 跑
cd refs/mcp_excalidraw && docker compose --profile full up -d

# 2. 把 anet-souls 停掉（避免与 Hermes 并行写画板）
cd /data/projs/anetchat && docker compose --env-file .env stop souls

# 3. 拉起 Hermes 栈
docker compose -f docker-compose.hermes.yml --env-file .env up -d --build

# 4. 第一次启动后，Hermes 会在 hermes/ 下创建 cron/jobs.json 等运行时文件
#    （bind-mount 把它们持久化到我们的 repo 目录）

# 5. 创建 cron 作业（每个 persona 一次）：
docker exec -it anet-hermes-gateway hermes -p feynman cron create \
  --name "feynman-trigger-by-bridge" \
  --schedule "manual" \
  --prompt "(triggered by anet-hermes-bridge with canvas context)"

# (其余 4 个 profile 同理)
```

---

## 6. 已知未解 / TODO

1. **`/v1/runs` 实际 payload shape 还未验证**——research agent 给的是推测；首次启动需调 `/v1/openai-spec` 看 OpenAPI schema。
2. **profile selection 怎么传**——payload 里 `profile` 字段是否被 Hermes 识别？也可能需要 per-profile API endpoint。可能需要 `POST /v1/profiles/feynman/runs`。
3. **`hermes profile create` 在 Docker 容器内**——交互式 CLI 工具。可能需要先 `docker exec` 进容器手动创建，或者在 entrypoint 写一个 init 脚本。
4. **MCP 进入 Hermes**——上游 mcp_excalidraw 默认期望 `EXPRESS_SERVER_URL=http://127.0.0.1:3000`，docker `network_mode: host` 才能解析。如果走 docker bridge 网络，要用 `host.docker.internal:3000`。
5. **MiniMax 兼容性**——MiniMax 的 Anthropic API 兼容是 simulated；某些 anthropic-version 头可能行为不一致。需要观察实际请求。
6. **Swarm 触发器**——目前 bridge 是 cron 模式（按秒触发）。理想是让 orchestrator profile 用 `delegate_task` 工具调 4 个 worker，由 Hermes 内部 Kanban 调度。**v2 工作**。

---

## 7. 设计原则：扩展到 40+ 教授

```
# 加入新教授（slug=prof_xxx）：
mkdir -p hermes/profiles/prof_xxx
cp refs/<prof_xxx>-skill/SKILL.md hermes/profiles/prof_xxx/SOUL.md
# Hermes 重启或调 reload；新 profile 立刻可用。

# 加入 cron 触发：
docker exec anet-hermes-gateway hermes -p prof_xxx cron create \
  --schedule "<unique-second-offset> * * * *" \
  --prompt "(bridge will rewrite at runtime)"

# bridge 端的 SLOT_FIRE dict 加一行：
"prof_xxx": [<sec1>, <sec2>],
```

无 schema 变更，纯配置增长。

---

## 8. 与 main (v6) 互斥并存

main 和 feat/hermes-multi-agent 都用**同一个 canvas server**（mcp-excalidraw-canvas）。
**不要同时**跑 anet-souls 和 anet-hermes-bridge——它们都会响应人类输入。

切换方式：
```bash
git checkout main && docker compose --env-file .env up -d souls && \
  docker compose -f docker-compose.hermes.yml stop hermes-bridge hermes-gateway

git checkout feat/hermes-multi-agent && \
  docker compose --env-file .env stop souls && \
  docker compose -f docker-compose.hermes.yml --env-file .env up -d
```

---

## 9. 状态（截至本文件创建）

- ✅ Hermes config.yaml 写好
- ✅ 5 个 profile 的 SOUL.md 写好
- ✅ hermes-bridge sidecar 写好（main.py + Dockerfile）
- ✅ docker-compose.hermes.yml 写好
- ⏳ **未实测**——首次启动会暴露上面 §6 的未解项
- ⏳ Swarm/delegate 模式只有架构图，未实现
- ⏳ MiniMax → Doubao → Mimo fallback 链未在 Hermes config 里反映（这是 main 分支同步在做的工作，会回流到这里）
