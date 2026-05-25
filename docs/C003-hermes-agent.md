# C003 — Hermes Agent 调研文档

> 仓库：https://github.com/NousResearch/hermes-agent
> 本地路径：`/data/projs/anetchat/refs/hermes-agent`
> 本地 Docker 镜像：`nousresearch/hermes-agent:latest`（已存在，8.51GB）
> 官方文档：https://hermes-agent.nousresearch.com/docs/user-guide/docker
> 当前版本：v0.14.0（2026-05-16 发布）
> 调研日期：2026-05-25
> 调研重点：Kanban（任务看板）+ Multi-Agent（多智能体编排）

---

## 1. 项目定位

Hermes Agent 是 **Nous Research** 官方的生产级自治智能体框架，围绕 **Hermes 系列模型**（也兼容 OpenAI/Anthropic/OpenRouter/xAI/DeepSeek/本地 vLLM 等）构建。

它的核心差异化不是模型，而是 **多智能体协作基础设施**：
- **基于 SQLite + WAL 的持久化 Kanban 看板**，作为多 Agent 之间唯一的协调原语
- **Embedded Dispatcher**（嵌入式调度器），按节拍扫描 Ready 任务、CAS 抢占、派生 worker 子进程
- **Swarm 拓扑**（蜂群）：root → 多个并行 worker → verifier → synthesizer，整套生命周期持久化到 DB
- **Claim TTL + Heartbeat + Zombie 检测**，gateway 重启不丢任务

对 anet.chat 的意义：**Hermes 提供的是一套可以直接套到 chat backend 上的"持久化多智能体调度核"**，不是又一个聊天 UI。

---

## 2. 仓库布局

| 目录 | 作用 |
|---|---|
| `agent/` | Agent 内核（provider 适配、压缩、记忆、工具执行） |
| `hermes_cli/` | CLI 子命令（setup、config、kanban、profiles、plugins）— **Kanban 全部在这里** |
| `tools/` | 40+ 工具实现（fs、shell、browser、code-exec、approval、kanban_tools 等） |
| `gateway/` | 22 个消息平台适配（Telegram/Discord/Slack/Teams/LINE/SimpleX 等）+ 嵌入调度器 |
| `acp_adapter/` | Agent Client Protocol 服务器（对接 VS Code、Zed、JetBrains） |
| `acp_registry/` | ACP 注册器 |
| `plugins/` | 插件系统（memory、providers、kanban dispatcher、observability） |
| `cron/` | 定时任务（scheduler.py、jobs.py） |
| `skills/` | 内置 skill + 管理 |
| `ui-tui/` | React/Ink 终端 UI |
| `web/` | 浏览器 dashboard（React + FastAPI） |
| `tests/` | 17k+ pytest 用例 |
| `optional-skills/` | 非默认装载的重型 skill |
| `RELEASE_v0.X.0.md` × 13 | 版本演化的"考古地层"，能反推架构变迁 |

---

## 3. 构建 & 运行（Docker）

### 3.1 Dockerfile 摘要

- Base：`debian:13.4` + `uv`（rust 写的 pip 替代品，比 pip 快 10×）
- PID 1：`s6-overlay`（zombie 回收 + 多 profile gateway 监督）
- 非 root 用户：`hermes:10000`
- 入口：`ENTRYPOINT ["/init"]`（s6），默认 `CMD ["hermes"]`

### 3.2 最小运行（README 指南）

```bash
docker run -it \
  -e OPENROUTER_API_KEY=sk-... \
  -v hermes-data:/opt/data \
  nousresearch/hermes-agent
```

- `/opt/data` → `HERMES_HOME`，持久化 sessions / kanban / memory
- 环境变量：`HERMES_UID`、`HERMES_HOME`，以及各种 provider key
- 本地 `nousresearch/hermes-agent:latest`（8.51GB 解压前 / 2.65GB 压缩）已经存在

### 3.3 PyPI 也可（v0.14.0+）

```bash
pip install hermes-agent
hermes   # 立刻可用
```

### 3.4 入口

- `hermes` → `hermes_cli/__main__.py` 总分发
- `cli.py` → 历史 CLI 入口
- `batch_runner.py` → 批量任务运行器（不开交互终端）

---

## 4. ⭐ Kanban 系统（重点 1）

> Hermes 把"任务"做成了**一等公民**：所有 multi-agent 协作都不绕过看板，直接读写 SQLite。

### 4.1 核心模块（`hermes_cli/`）

| 文件 | 作用 |
|---|---|
| `kanban.py` | CLI 命令面：`hermes kanban list/add/move/...` |
| `kanban_db.py` | SQLite 持久化、抢占逻辑、调度编排（2000+ LOC，核心中的核心） |
| `kanban_swarm.py` | Swarm 抽象（并行 worker + verifier + synthesizer） |
| `kanban_decompose.py` | 自动任务分解（大目标 → 子任务图） |
| `kanban_specify.py` | 任务规格化 & triage |
| `kanban_diagnostics.py` | 健康检查 & 求救信号 |
| `tools/kanban_tools.py` | Agent 可调用工具（`kanban_complete`、`kanban_block`、`kanban_heartbeat`、`kanban_create`、`kanban_list`、`kanban_unblock`） |
| `plugins/kanban/` | Dispatcher 插件 + Dashboard API（2217 LOC） |

测试：`tests/hermes_cli/test_kanban_*.py` 50+ 个文件，`tests/stress/` 还有并发抢占的压力测试。

### 4.2 任务数据模型（`kanban_db.py:Task` dataclass）

```python
id: str                      # 任务 ID
title: str                   # 一句话摘要
body: str                    # 完整描述（markdown）
status: str                  # triage|todo|scheduled|ready|running|blocked|review|done|archived
priority: int                # 0 默认，越大越优先
assignee: Optional[str]      # profile 名或 worker 标识
created_by: str              # 谁建的（profile / tool / orchestrator）
created_at: int              # unix ts
started_at: Optional[int]    # worker claim 时刻
completed_at: Optional[int]  # 完成/阻塞/归档时刻
result: Optional[str]        # markdown 结果摘要
skills: Optional[list[str]]  # 需要装载的 skill 依赖
tenant: Optional[str]        # 多租户隔离键
workspace_kind: str          # scratch|worktree|dir（解耦 git）
workspace_path: Optional[str]
branch_name: Optional[str]   # 与 git 绑定的任务的分支
max_retries: int             # 单任务重试预算
session_id: Optional[str]    # 关联的会话 UUID
workflow_template_id: Optional[str]
current_step_key: Optional[str]
claim_lock: Optional[str]    # worker 抢占令牌（CAS 用）
worker_pid: Optional[int]
claim_expires: Optional[int] # 心跳过期时间（默认 15min）
```

### 4.3 持久化策略

- **SQLite + WAL 模式**：单写多读，dispatcher 抢占不阻塞前端 dashboard 读取
- **路径解析顺序**（`kanban_db.py:L25-37`）：
  1. 调用方显式 `board=` 参数
  2. 环境变量 `HERMES_KANBAN_BOARD`（dispatcher 派 worker 时注入）
  3. `HERMES_KANBAN_DB` 全路径覆盖
  4. `$HERMES_KANBAN_HOME/kanban/current` 持久化的"当前 board"标记
  5. 默认 `default` board
- **多 board 隔离**：`$HERMES_KANBAN_HOME/kanban/boards/{slug}/kanban.db`，每个 project 独立 DB

辅助表：
```
tasks          — 主表
task_links     — 任务依赖（parent / blocker / related）
task_comments  — 结构化 JSON 黑板（agent 间通信用）
task_events    — 历史运行（started_at, ended_at, duration, exit_code）
task_attachments — （未来扩展）文件/产物
```

### 4.4 状态机

```
triage  (人工 triage)
   ↓
 todo  (入队)
   ↓
scheduled  (定时启动)
   ↓
ready  (dispatcher 候选)
   ↓ [dispatcher CAS]
running  (worker in-flight)
   ├→ blocked  (worker 主动 kanban_block) → ready / done / archived
   ├→ review   (worker 请人工审核)        → done
   └→ done     (worker kanban_complete)
[任何状态] → archived  (清理)
```

### 4.5 ⭐ 调度器（Dispatcher）

`gateway/run.py:L5282-5481` 嵌入式调度器（默认启用）：

```python
# 伪代码
while True:
    sleep(dispatch_interval_seconds)  # 默认 60s
    for board in active_boards:
        asyncio.to_thread(
            kanban_db.dispatch_once,
            conn, board=board.slug,
            max_spawn=cfg.max_spawn,
            max_in_progress=cfg.max_in_progress,
        )
```

`dispatch_once()` 的核心 CAS（`kanban_db.py:L2296-2409`）：

```sql
-- 1. 选候选
SELECT * FROM tasks
WHERE status='ready'
  AND (assignee IS NULL OR assignee=profile_name)
LIMIT N;

-- 2. 抢占（CAS）— 只有一个 dispatcher 实例能成功
UPDATE tasks
SET status='running',
    claim_lock=?,
    worker_pid=?,
    claim_expires=?
WHERE id=? AND status='ready' AND claim_lock IS NULL;
-- affected_rows=1 才算抢到
```

抢到后派生子进程：

```bash
hermes -p {profile} chat --kanban-task {id} --board {slug} --skills S1,S2
```

子进程环境变量：
```
HERMES_KANBAN_TASK=<task_id>          # worker 把自己锚定到这个任务
HERMES_KANBAN_BOARD=<slug>            # 锁死 board
HERMES_KANBAN_WORKSPACES_ROOT=<path>
HERMES_KANBAN_DB=<full_path>
HERMES_KANBAN_RUN_ID=<run_id>
HERMES_SESSION_ID=<uuid>
```

并发护栏：
- `kanban.max_spawn` — 单次 tick 最多派生数
- `kanban.max_in_progress` — 同时 running 的硬上限
- `kanban.failure_limit` — 累计失败 N 次的任务自动转 blocked

### 4.6 Zombie / 心跳 / 重抢

`kanban_db.py:L2525-2627`：

- worker 周期性调 `kanban_heartbeat(task_id)` → 延长 `claim_expires`
- dispatcher 周期性 `release_stale_claims(timeout)` → `claim_expires < now()` 的 running 任务回到 ready
- Darwin（macOS）特化的 defunct 进程检测：进程存在但已 zombie 时主动重抢
- worker 异常退出（没 complete / block）→ 自动 block + 告警

**意义**：gateway 进程能挂、worker 能 OOM、机器能重启，**任务永远在 SQLite 里有据可查、永远能被恢复**。这是 Hermes 跟所有 in-memory orchestrator（langgraph、autogen 之类）的关键差异。

### 4.7 Hallucination Gate

`kanban_db.py:L20232` 防止"幽灵任务":
- worker 用 `kanban_create()` 建子任务时打上 `created_by=worker_session_id`
- worker 退出时如果建过任务但没显式 link 为子任务 → auto-block 父任务 + 报警

→ 防止 LLM 编造说"我已经派了 5 个任务"但实际什么都没建。

### 4.8 Agent 端工具表面（`tools/kanban_tools.py`）

| 工具 | 谁能用 | 说明 |
|---|---|---|
| `kanban_complete(task_id, summary, metadata)` | worker | 标记完成，metadata 是结构化 dict（session_id、产物路径、关键事实） |
| `kanban_block(task_id, reason)` | worker | 标记阻塞 |
| `kanban_heartbeat(task_id)` | worker | 续期 |
| `kanban_create(title, body, ...)` | worker | 派生子任务 |
| `kanban_list(filter, limit, board)` | **仅 orchestrator** | 读看板（worker 看不到） |
| `kanban_unblock(task_id)` | **仅 orchestrator** | 解阻塞 |

门控（`kanban_tools.py:L62-90`）：
```python
def _check_kanban_mode():
    # worker：HERMES_KANBAN_TASK 已设置
    # orchestrator：profile 显式开启 kanban toolset
    return os.environ.get("HERMES_KANBAN_TASK") or _profile_has_kanban_toolset()

def _check_kanban_orchestrator_mode():
    # 只有 orchestrator 看得到 list/unblock
    return (not os.environ.get("HERMES_KANBAN_TASK")) and _profile_has_kanban_toolset()
```

**设计哲学**：worker 极度收敛——只看见自己那一个任务，不能扫看板；orchestrator 才有全局视野。降低 LLM 越权风险。

---

## 5. ⭐ Multi-Agent 编排（重点 2）

### 5.1 架构：以 Kanban 为枢纽的 Hub-and-Spoke

```
       ┌─────────────────────────────┐
       │   SQLite Kanban Board       │ ← 唯一共享状态
       │   (tasks + comments + links)│
       └──────────────┬──────────────┘
                      │
        ┌─────────────┼──────────────┐
        │             │              │
   ┌────▼───┐    ┌────▼───┐    ┌────▼───┐
   │worker A│    │worker B│    │worker C│ ← 各自子进程
   │(子进程)│    │(子进程)│    │(子进程)│
   └────────┘    └────────┘    └────────┘
        ▲             ▲              ▲
        └─────────────┼──────────────┘
                      │
              ┌───────┴────────┐
              │   Dispatcher   │ ← gateway 内嵌
              │ (60s tick + CAS)│
              └────────────────┘
```

关键属性：
- **没有 RPC**——agent 之间不互调，全部通过看板留言/读任务
- **没有 in-memory queue**——任务图就是真理之源
- **没有协调中心**——dispatcher 只是 SQL 客户端，看板才是协调器
- **进程级隔离**——worker 是独立 OS 进程，OOM/崩溃不会污染其它 worker

### 5.2 Swarm 拓扑（`hermes_cli/kanban_swarm.py`）

固定模式：
```
Root (Planning)
 ├─ Worker 1 (parallel) ─┐
 ├─ Worker 2 (parallel) ─┤
 ├─ Worker N (parallel) ─┴→ Verifier ──→ Synthesizer
```

API：
```python
SwarmCreated = create_swarm(
    goal="写一份竞品分析报告",
    workers=[
        SwarmWorkerSpec(profile="researcher", title="搜集 Crunchbase 数据", body="..."),
        SwarmWorkerSpec(profile="researcher", title="收集 G2 评论",       body="..."),
        SwarmWorkerSpec(profile="writer",     title="写定价对比章节",     body="..."),
    ],
    verifier_assignee="critic",
    synthesizer_assignee="lead",
    tenant="acme",
    workspace_kind="scratch",
)
# 返回 root_id, worker_ids, verifier_id, synthesizer_id
```

共享黑板：
- root task 的 `task_comments` 字段挂 `[swarm:blackboard]` JSON
- 所有 worker / verifier / synthesizer 都能读到兄弟节点贡献的事实
- 不需要单独消息队列 / pub-sub 服务

### 5.3 worker 生命周期

```
1. dispatcher CAS 抢到 task → 派 worker 子进程
2. worker 进程启动：
     hermes -p researcher chat --kanban-task <id>
3. AIAgent.run_conversation() 主循环：
     - 装载 skill（按 task.skills）
     - 注入任务上下文（title/body/comments）
     - 调工具（web_search / memory_save / kanban_heartbeat ...）
     - 调 kanban_complete(summary, metadata) 或 kanban_block(reason)
4. 进程退出 → dispatcher reaper 检测状态
     - 已 complete/block：onclear
     - 没 complete/block 就退出：auto-block + 告警
```

### 5.4 角色专业化

profile = "agent 人设 + 装载的工具集 + 模型选择"。用户在 `~/.hermes/config.yaml` 中定义：

```yaml
profiles:
  orchestrator:
    enabled_toolsets: [kanban]                        # 只能看板路由
    model: openrouter/llama-3:8b
  researcher:
    enabled_toolsets: [web-search, memory, kanban]
    model: openrouter:openai/gpt-4o
  writer:
    enabled_toolsets: [code-execution, memory, kanban]
    model: openrouter/llama-3:70b
  critic:
    enabled_toolsets: [vision, memory, kanban]
    model: openrouter/claude-3.5-sonnet
  code:
    enabled_toolsets: [terminal, git, code-search, kanban]
    model: openrouter/qwen2.5-coder
```

worker 由 `task.assignee=profile_name` 决定加载哪个 profile。

### 5.5 成本控制

| 维度 | 机制 |
|---|---|
| 每 agent 迭代上限 | `max_iterations`（共享给 subagent） |
| 每 agent token 上限 | `iteration_budget`（软限，提示模型自停） |
| 跨 agent 共享配额 | 父 `credential_pool` 全局会计 |
| 单任务重试 | `task.max_retries` |
| 失败熔断 | `kanban.failure_limit` |
| 死任务回收 | `dispatch_stale_timeout_seconds` |
| 模型路由 | 不同 profile 用不同价位的模型（researcher 用 gpt-4o，orchestrator 用 llama-3:8b） |

### 5.6 Handoff 协议

```python
kanban_complete(
    task_id=...,
    summary="找到 5 家竞品的定价数据，详见 metadata.findings",
    metadata={
        "worker_session_id": "...",        # 下游 agent 可继承记忆
        "findings": [{...}, {...}],        # 结构化事实
        "logs": ["s3://...", "..."],       # 产物引用
        "code_review_approved": True,
    },
)
```

下游 verifier / synthesizer：
1. 读 `task_links` 找上游 task
2. 读上游的 `result` + `task_events` + 黑板 comments
3. 跨 session 记忆通过 `worker_session_id` 接力

---

## 6. 其他能力（速览）

### 6.1 工具集

40+ 内置工具，自动从 `tools/` 发现：

| 类别 | 工具 |
|---|---|
| 文件系统 | `read_file`、`write_file`、`patch_file`、`list_files`、`delete_file` |
| Shell | `run_shell`（沙箱）、`python_repl` |
| 浏览器 | `browser_navigate`、`browser_screenshot`、`browser_execute_javascript` |
| Web | `web_search`（Tavily/SearXNG/Brave/DDG/Exa）、`web_extract` |
| 代码 | `git_*`、`code_search`、`code_completion` |
| 视觉 | `vision_analyze`、`video_analyze` |
| 媒体 | `image_generate`、`video_generate`、`text_to_speech` |
| 控制 | `approval`（人工闸门）、`clarify`（多选追问） |
| 记忆 | `memory_recall`、`memory_save`、`memory_forget` |
| 协调 | `kanban_*`、`delegate`（生 subagent）、`skill_install`、`mcp_call` |
| 定时 | `cronjob` |

沙箱：
- shell 命令走 `approval` 工具门控 + 危险命令检测（v0.14.0 关闭了 3 个 `sudo -S` 绕过点）
- 浏览器是被监督的持久 Chrome 进程
- 终端后端可选：local / Docker / SSH / Modal / Daytona / Singularity / Vercel

### 6.2 ACP（Agent Client Protocol）

`acp_adapter/server.py`：把 Hermes 暴露成"agent endpoint"给 VS Code / Zed / JetBrains 调用。

- 类似 LSP 之于 language server
- 传输：stdio / SSE / HTTP
- 能力：session fork、模型切换、模式控制、工具调用流式、approval 闸门
- 启动：`hermes acp server`

### 6.3 Cron

`cron/scheduler.py`：
- 60 秒 tick，从 config 读 croniter 表达式
- 三种模式：
  - **agent 模式**（默认）：派一个 AIAgent 跑这个 prompt
  - **no_agent 模式**：纯 shell，输出送平台
  - **watch 模式**：每 tick 跑脚本，**输出非空才送**
- 安全：cron agent 强制禁用 `cronjob`（防递归）、`messaging`、`clarify` 三个 toolset；装载的 skill 被 prompt-injection 扫描（issue #3968）

### 6.4 记忆

- **session store**：每个 profile 独立 SQLite，FTS5 全文索引
- **chat compression**：checkpoint v2，真删旧轮 + 磁盘配额
- **user memory**：默认 `~/.hermes/MEMORY.md`，可换 Honcho / mem0 / Supermemory
- **user profile**：`~/.hermes/USER.md` 自动抽取
- **`.context` 文件**：项目级注入 system prompt

### 6.5 Dashboard

`http://localhost:8080`，React 18 + FastAPI + WebSocket：
- Chat（嵌 TUI）
- **Kanban Board**（drag-drop、实时状态、平台 notification 开关）
- Sessions、Skills、Plugins、Profiles、Logs、Settings

### 6.6 安全

- v0.13.0 redaction 默认开启（API key / GH token / Slack token 等正则脱敏）
- v0.14.0 关闭 8 个 P0：sudo -S 暴破阻断、Discord 角色按 guild 隔离（CVSS 8.1）、工具错误消息净化、调试分享 redaction、cron prompt-injection 扫描…
- 密钥落在 `~/.hermes/.env`（hermes 用户 0600）

---

## 7. 版本演化（精选）

| 版本 | 日期 | 重点 |
|---|---|---|
| v0.13.0 | 2026-05-07 | **Kanban 多智能体首发**：durable board / heartbeat / reclaim / zombie 检测；`/goal` Ralph 循环；checkpoints v2；gateway 自动恢复；cron no_agent；8 个 P0 安全闭环 |
| v0.14.0 | 2026-05-16 | **基石版**：Kanban 稳定 + Swarm 拓扑；PyPI 包；原生 Windows beta；Claude 1h 跨 session 缓存；OAuth provider 的 OpenAI 兼容代理；xAI Grok + SuperGrok OAuth；22 平台；冷启动 ~19s |

Kanban 是 v0.13 才 GA 的功能，v0.14 才补齐 Swarm 抽象与多 board——**写本文档时这套机制刚定型 2 周左右**。

---

## 8. 许可

**MIT License**（Copyright © 2025 Nous Research）。

---

## 9. ⭐ 对 anet.chat 的集成路径

### 9.1 短期：把 Hermes 作为外部 backend（推荐 0→1）

把本地 `nousresearch/hermes-agent:latest` 镜像跟 [C002](./C002-mcp_excalidraw.md) 的 mcp_excalidraw 一起编排：

```yaml
# docker-compose.yml（追加 service）
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: anet-hermes
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - HERMES_HOME=/opt/data
    volumes:
      - hermes-data:/opt/data
    ports:
      - "127.0.0.1:8080:8080"      # Dashboard
    networks: [mcp-network]
```

anet.chat backend 只需要：
1. 调 Hermes dashboard 的 REST 接口创建 task
2. 订阅 WebSocket 拿状态/结果
3. UI 上把 task 状态映射到 anet.chat 的 chat session

### 9.2 中期：把 Hermes 的 Kanban 抽出来做 anet.chat 自家任务核

不要重写——直接把 `hermes_cli/kanban_db.py` + `kanban_swarm.py` + `tools/kanban_tools.py` 当 vendored library 用：

```
anet.chat backend
   ├─ kanban_db.py (vendored)           ← SQLite + WAL + CAS
   ├─ kanban_swarm.py (vendored)        ← Swarm 抽象
   ├─ anet_dispatcher.py (新)            ← 替换 gateway/run.py 的 dispatcher
   │    → 派 anet 自家 worker 进程
   │    → 注入 anet 自家 system prompt 和工具集
   └─ anet_tools.py (新)                 ← 把 mcp_excalidraw 的画板工具
                                          + anet.chat 业务工具 包成 toolset
```

这样 anet.chat 拿到的是 **"任务持久化 + 多 agent 并发"** 的成熟核，业务层只关心 prompt / 工具 / UI。

### 9.3 长期：用 Hermes 的 ACP / MCP 通道接 anet.chat 的 chat 入口

- ACP：把 anet.chat 暴露成像 VS Code 那样的"客户端"，所有 chat 走 ACP 调 Hermes
- MCP：用 Hermes 的 `mcp_call` 工具把 anet.chat 已经接的 MCP（excalidraw、shadcn 等）合并进 Hermes 的工具池

### 9.4 与 mcp_excalidraw 的协同

mcp_excalidraw 提供"画板"——Hermes 提供"派人画"。一个典型 demo：

```
用户："画一张 anet.chat 后端架构图"
  ↓
anet.chat → kanban swarm:
  root: "anet.chat 后端架构图"
   ├─ worker[researcher]:  "用 web_search 找 anet.chat 现有架构线索"
   ├─ worker[architect]:   "基于 researcher 结果列出节点/边"
   └─ worker[diagrammer]:  "用 excalidraw MCP 调 batch_create_elements 画出来"
       → 调 mcp_excalidraw 的 create_from_mermaid 或 batch_create_elements
       → 在 http://127.0.0.1:3000 实时显现
  verifier[critic]:        "调 get_canvas_screenshot 看效果，给改进意见"
  synthesizer[lead]:       "导出 .excalidraw 文件 + Mermaid 备份"
```

整个流程 SQLite 全程可观察，gateway 重启不丢，Dashboard 看 board 实时进度。

---

## 10. 关键文件索引（本地）

- `hermes_cli/kanban_db.py` — Kanban 持久化与调度核心
- `hermes_cli/kanban_swarm.py` — Swarm 拓扑
- `hermes_cli/kanban_decompose.py` — 任务分解
- `hermes_cli/kanban_diagnostics.py` — 健康检查
- `tools/kanban_tools.py` — Agent 端工具
- `plugins/kanban/dashboard/plugin_api.py` — Dashboard API
- `gateway/run.py:L5282-5481` — 嵌入调度器
- `agent/` — Agent 内核
- `acp_adapter/server.py` — ACP server
- `cron/scheduler.py` — 定时任务
- `Dockerfile` — 镜像构建
- `RELEASE_v0.13.0.md`、`RELEASE_v0.14.0.md` — Kanban 演化史

---

## 11. 注意事项 / 已知坑

- **存储集中在单 SQLite**：单机 OK；要分布式得自己上 Postgres 替换层
- **worker 抢占 CAS 只在同 board 内有保证**：多 board 任务依赖要靠 `task_links` 跨表手工维护
- **dispatcher 是 60s tick**：低延迟交互（用户期望"立刻派活"）需调小 `dispatch_interval_seconds` 到 5-10s
- **Claude 1h 缓存只在 v0.14.0+**：低版本 prompt 长会很贵
- **22 个平台 gateway 都会启动**：anet.chat 集成时关掉不需要的 platform（config 里禁用）
- **Skill 装载的 prompt 会被扫 prompt injection**（v0.13.0 #3968）：第三方 skill 注入失败要看 logs/agent.log
- **Memory 默认 `~/.hermes/MEMORY.md`**：跑容器记得挂卷，否则重启就丢

---

## 12. 与 C001 / C002 / C004 的关联

- [C001 Excalidraw](./C001-excalidraw.md) 提供画板组件
- [C002 mcp_excalidraw](./C002-mcp_excalidraw.md) 提供 AI Agent 控制画板的 MCP 通道
- **C003 Hermes（本文）** 提供 AI Agent 集群的持久化调度
- [C004 nuwa-skill](./C004-nuwa-skill.md) 提供把"专家本人"蒸馏为可调用 Skill 的方法论

整合方向：用 **C003 Hermes 调度 + C004 nuwa-skill 角色 → 调 C002 MCP 工具 → 画到 C001 画板**——anet.chat 的差异化能力栈。
