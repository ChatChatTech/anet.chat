# C002 — mcp_excalidraw 调研文档

> 仓库：https://github.com/yctimlin/mcp_excalidraw
> 本地路径：`/data/projs/anetchat/refs/mcp_excalidraw`
> npm：`mcp-excalidraw-server@1.0.7`
> Docker：`ghcr.io/yctimlin/mcp_excalidraw:latest` & `ghcr.io/yctimlin/mcp_excalidraw-canvas:latest`
> 调研日期：2026-05-25
> 目的：理解作为 MCP Server + Canvas Server + Agent Skill 的三体架构，评估 anetchat 直接复用或派生的可行性。

---

## 1. 项目定位

mcp_excalidraw 提供一个面向 **AI Agent** 的 Excalidraw 工具箱，让 Claude Desktop / Claude Code / Cursor / Codex CLI 等带 MCP 客户端的 AI 可以**实时操控一块共享的 Excalidraw 画布**。

与官方 [`excalidraw-mcp`](https://github.com/excalidraw/excalidraw-mcp) 的差异（README 摘录）：

| 维度 | 官方 Excalidraw MCP | yctimlin/mcp_excalidraw |
|---|---|---|
| 调用模式 | 一次性 "prompt → diagram" | 26 个工具，元素级 CRUD |
| 状态 | 无状态，每次调用独立 | 持久化的实时画布 |
| AI 是否能"看见"画布 | ❌ | ✅ `describe_scene`（文本）+ `get_canvas_screenshot`（图像） |
| 迭代精修 | 整图重生 | 画 → 看 → 改 → 再看，逐元素 |
| 布局算子 | ❌ | `align_elements` / `distribute_elements` / `group_elements` |
| 文件 I/O | ❌ | `export_scene` / `import_scene` |
| 快照回滚 | ❌ | `snapshot_scene` / `restore_snapshot` |
| Mermaid | ❌ | `create_from_mermaid` |
| 多 Agent 并发 | ❌ | ✅ 多个 MCP 客户端可同时画同一画布 |
| Skill 备份方案 | ❌ | 自带 REST API + Agent Skill 兜底 |

→ 对 anetchat 的价值：**直接拿来当 "AI 白板后端" 用**，或把它的 server 架构 + 工具集"移植"进 anetchat 自家进程。

---

## 2. 两进程架构

```
┌─────────────────────────────┐         ┌─────────────────────────────┐
│ MCP Server (stdio)          │         │ Canvas Server (HTTP+WS)     │
│ src/index.ts                │ HTTP    │ src/server.ts               │
│ 26 个 MCP 工具              │ ──────▶ │ /api/elements POST/GET/PUT  │
│ Claude/Codex 通过 stdio 调用 │         │ /api/snapshots, /api/files  │
└─────────────────────────────┘         │ /api/export/image, /viewport │
                                        │ WebSocket → 广播给所有客户端 │
                                        └────────────┬────────────────┘
                                                     │ WS broadcast
                                          ┌──────────▼──────────┐
                                          │ Frontend (React)    │
                                          │ frontend/src/App.tsx │
                                          │ <Excalidraw />       │
                                          │ excalidrawAPI.updateScene │
                                          └──────────────────────┘
```

- **Canvas Server** (`npm run canvas`)：Express + ws，默认 `127.0.0.1:3000`，挂载内存元素表 + 广播 + 静态服务前端
- **MCP Server** (`node dist/index.js`)：纯 stdio，进程拉起后通过 `EXPRESS_SERVER_URL` 反向调用 Canvas REST API
- **Frontend**：纯客户端 React，挂 `<Excalidraw />`，通过 WebSocket 接收元素差量并应用到 `excalidrawAPI`

---

## 3. 仓库结构

| 路径 | 内容 |
|---|---|
| `src/index.ts` (82.7 KB) | MCP 服务端，所有 26 个工具定义 + 处理 switch + AES-GCM 加密上传 |
| `src/server.ts` (38.6 KB) | Express 应用，所有 REST endpoint，WebSocket 广播，IPv4-loopback 守卫 |
| `src/types.ts` (8.6 KB) | `ServerElement` 模型、`Map<string, ServerElement>` 内存表、`generateId()`、字体编号映射 |
| `src/utils/logger.ts` | Winston 配置（console → stderr，file → 平台路径） |
| `frontend/src/main.tsx` | React 挂载 |
| `frontend/src/App.tsx` | `<Excalidraw />` 包装、WS 订阅、`excalidrawAPI` 远程驱动 |
| `frontend/src/utils/mermaidConverter.ts` | 浏览器内执行 Mermaid → Excalidraw 转换 |
| `skills/excalidraw-skill/SKILL.md` (16.7 KB) | Agent Skill 主文档（MCP/REST 双模式说明、布局反模式、设计原则） |
| `skills/excalidraw-skill/scripts/*.cjs` | 7 个 Node CJS 工具脚本（REST 兜底） |
| `skills/excalidraw-skill/references/cheatsheet.md` | API 速查 |
| `Dockerfile` | MCP server 镜像（多阶段，Node 18 slim） |
| `Dockerfile.canvas` | Canvas server 镜像（3 阶段：frontend builder + backend builder + production） |
| `docker-compose.yml` | `canvas` 服务（默认开）+ `mcp` 服务（`--profile full` 才启）|
| `scripts/check-local-bind.mjs` | 本地绑定回归测试（防止意外暴露 0.0.0.0 / IPv6） |
| `claude_desktop_config.json` | Claude Desktop 示例配置 |
| `vite.config.js` | 前端构建（root=`frontend/`，输出 `dist/frontend/`，dev `/api` 代理到 3000） |
| `tsconfig.json` | ES2022 target，ESM，strict，输出 `dist/`，排除 `frontend/` |

---

## 4. 依赖与构建

`package.json` 关键脚本：

| 脚本 | 命令 | 用途 |
|---|---|---|
| `build:server` | `npx tsc` | 编译 TS → `dist/` |
| `build:frontend` | `vite build` | 前端 → `dist/frontend/` |
| `build` | `build:frontend && build:server` | 全量构建 |
| `start` | `build:server && node dist/index.js` | MCP server |
| `canvas` | `build:server && node dist/server.js` | Canvas server |
| `dev` | `concurrently dev:server vite` | 开发模式 |
| `production` | `build && canvas` | 生产 Canvas |
| `test:bind` | `build:server && node scripts/check-local-bind.mjs` | 绑定回归 |
| `type-check` | `npx tsc --noEmit` | 仅类型校验 |

核心依赖：

| 包 | 版本 | 角色 |
|---|---|---|
| `@modelcontextprotocol/sdk` | latest | MCP stdio 协议 |
| `@excalidraw/excalidraw` | ^0.18.0 | React 组件 + 类型 |
| `@excalidraw/mermaid-to-excalidraw` | ^1.1.3 | Mermaid 转换 |
| `mermaid` | ^11.12.1 | Mermaid DSL |
| `express` | ^4.18.2 | HTTP 框架 |
| `ws` | ^8.14.2 | WebSocket |
| `zod` | ^3.22.4 | 输入校验 |
| `zod-to-json-schema` | ^3.22.3 | 生成 MCP 工具 JSON Schema |
| `winston` | ^3.11.0 | 日志 |
| `cors` | ^2.8.5 | CORS |
| `dotenv` | ^16.3.1 | env |
| `node-fetch` | ^3.3.2 | 反向调 Canvas REST |

Node ≥ 18，TypeScript 5.8.3，Vite 6.3.5。

---

## 5. 26 个 MCP 工具清单（实测自 `src/index.ts`）

按定义顺序：

| # | 工具 | 行号 | 类别 | 关键参数 / 说明 |
|---|---|---|---|---|
| 1 | `create_element` | L375 | CRUD | `type`/`x`/`y` 必填，`id` 可选自动生成 |
| 2 | `update_element` | L407 | CRUD | `id` 必填，其余 patch |
| 3 | `delete_element` | L435 | CRUD | 按 ID 删除 |
| 4 | `query_elements` | L446 | CRUD | 按类型/范围/字段查询 |
| 5 | `get_resource` | L473 | 资源 | enum: `scene` / `theme` / `elements` / `library` |
| 6 | `group_elements` | L487 | 布局 | 把多个元素纳入同一 `groupId` |
| 7 | `ungroup_elements` | L501 | 布局 | 移除 `groupId`，失败抛错 |
| 8 | `align_elements` | L512 | 布局 | left/center/right/top/middle/bottom |
| 9 | `distribute_elements` | L530 | 布局 | horizontal / vertical 均匀分布 |
| 10 | `lock_elements` | L548 | 布局 | `locked=true` |
| 11 | `unlock_elements` | L562 | 布局 | `locked=false` |
| 12 | `create_from_mermaid` | L576 | 特殊 | 把 Mermaid 文本送给前端，前端调用 `convertMermaidToExcalidraw()` 后返回元素 |
| 13 | `batch_create_elements` | L611 | CRUD | 一次创建多个，保留传入 ID（重要：箭头要先有源/目标 ID 才能绑定） |
| 14 | `get_element` | L652 | CRUD | 按 ID 获取单元素 |
| 15 | `clear_canvas` | L663 | 状态 | 清空所有元素 |
| 16 | `export_scene` | L671 | 文件 | 导出 `.excalidraw` JSON（v2 格式） |
| 17 | `import_scene` | L684 | 文件 | 从 `.excalidraw` 文件 / 原始 JSON 导入，`mode='replace' \| 'merge'` |
| 18 | `export_to_image` | L707 | 文件 | PNG/SVG，可写盘 |
| 19 | `duplicate_elements` | L730 | CRUD | 克隆 + 偏移（默认 20px） |
| 20 | `snapshot_scene` | L747 | 状态 | 命名快照（内存 Map） |
| 21 | `restore_snapshot` | L761 | 状态 | 恢复命名快照 |
| 22 | `describe_scene` | L775 | 检查 | 返回 markdown 化场景描述：分类计数、bounding box、按 y/x 排序的元素列表、连接关系、分组 |
| 23 | `get_canvas_screenshot` | L783 | 检查 | 通过 `/api/export/image` 让前端渲染 PNG，返回 base64 image content（**AI 可直接看到画布**） |
| 24 | `read_diagram_guide` | L796 | 文档 | 返回内嵌的设计指南（色板、尺寸规则、布局模式、反模式），写在 `src/index.ts:L280-370` |
| 25 | `export_to_excalidraw_url` | L804 | 分享 | AES-GCM 加密 + zlib 压缩 → 上传 `json.excalidraw.com` → 返回 `https://excalidraw.com/#json=...` 可分享 URL |
| 26 | `set_viewport` | L812 | 视图 | `scrollToContent` / `scrollToElementId` / 手动 zoom + offsetX/Y |

> Skill manifest 与早期 README 里偶有"28 个工具"的措辞（含一些查询/列表辅助），代码实测注册的是 26 个。

### 5.1 工具特殊点

- **`describe_scene`**：把场景按 50px 行桶排序，输出形如 `[abc123] rectangle at (100, 50) | size 200x100 | text: "Service A" | groups: [g1]` 的 markdown 列表，专门设计成 LLM 易消化的格式。
- **`get_canvas_screenshot`**：流程为 MCP → POST `/api/export/image` (requestId) → 通过 WS 通知前端 → 前端用 `exportToBlob()` 渲染并 POST base64 回 `/api/export/image/result` → MCP 阻塞读取结果 → 返回给 LLM 作为 image content。**因此前端必须运行**（headless 模式下需要 Puppeteer/Playwright 兜底，作者推荐外置 `agent-browser`）。
- **`export_to_excalidraw_url`**：完整复现 excalidraw.com 的 E2E 加密协议：
  1. 清洗元素 + 补充默认字段（angle/roundness/seed/versionNonce 等）
  2. 处理 bound text 与 boundElements 引用
  3. 构造 v2 `.excalidraw` JSON
  4. `concatBuffers([version:4B, len:4B, data])` 框
  5. `zlib.deflate` 压缩
  6. AES-GCM 128 加密（随机 IV + 随机 key）
  7. POST `https://json.excalidraw.com/api/v2/post/` → `{id}`
  8. JWK 导出 key 的 `k` 字段
  9. 拼 `https://excalidraw.com/#json={id},{k}` 返回
- **`create_from_mermaid`**：MCP 不在 Node 端跑 Mermaid（Node 没 DOM），而是通过 `/api/elements/from-mermaid` 让浏览器前端调用 `@excalidraw/mermaid-to-excalidraw`，结果回传再写入元素表。
- **`set_viewport`**：与 `get_canvas_screenshot` 类似的 request/result 异步模型，通过 WS 让前端调 `excalidrawAPI.scrollToContent()` 或手动设置 zoom/offset。

---

## 6. Canvas Server (`src/server.ts`)

### 6.1 REST API 全表

| 路径 | 方法 | 用途 |
|---|---|---|
| `/health` | GET | 健康检查 |
| `/api/sync/status` | GET | 元素数 + 时间戳 |
| `/api/elements` | GET | 列出全部元素 |
| `/api/elements` | POST | 创建单个 |
| `/api/elements/clear` | DELETE | 清空（**注意路由顺序：必须在 `:id` 之前**） |
| `/api/elements/search` | GET | type/filter/bbox 查询 |
| `/api/elements/batch` | POST | 批量创建（保留 ID） |
| `/api/elements/sync` | POST | 全量替换（import_scene 走这条） |
| `/api/elements/from-mermaid` | POST | 转 Mermaid 并写入 |
| `/api/elements/:id` | GET | 单元素 |
| `/api/elements/:id` | PUT | 更新 |
| `/api/elements/:id` | DELETE | 删除 |
| `/api/files` | GET/POST | 图片文件列表/上传 |
| `/api/files/:id` | DELETE | 删除文件 |
| `/api/export/image` | POST | 让前端渲染图，requestId 异步 |
| `/api/export/image/result` | POST | 前端回填 base64 结果 |
| `/api/viewport` | POST | 视图变更请求 |
| `/api/viewport/result` | POST | 视图变更确认 |
| `/api/snapshots` | GET/POST | 列表 / 保存 |
| `/api/snapshots/:name` | GET | 取快照 |
| `/` | GET | 前端 `index.html` |

### 6.2 WebSocket 协议

`ws://HOST:PORT/`，无需鉴权。连接即订阅。

广播消息类型（`src/types.ts:L171-189`）：
- `initial_elements` — 客户端连接时下发当前全部元素
- `element_created` / `element_updated` / `element_deleted` / `elements_batch_created` / `canvas_cleared`
- `sync_status` — 心跳/同步状态
- `export_image_request` — 让前端渲染图（带 requestId）
- `set_viewport` — 让前端设置视图（带 requestId）
- `mermaid_convert` — 让前端执行 Mermaid 转换

冲突解决：**无**。直接 last-write-wins，多 Agent 并发的"协同"是粗粒度广播 + 内存覆盖。

### 6.3 安全防护

- 默认 `HOST=127.0.0.1`（仅 IPv4 loopback）
- IPv6 `[::1]` 端口被显式拒绝（防止意外双绑）
- 同端口二次启动 → `EADDRINUSE` 失败
- 路径遍历守卫 `sanitizeFilePath()`，`EXCALIDRAW_EXPORT_DIR` env 限定根目录
- **没有 token / 鉴权**，作者明确警告暴露公网必须配合网络层 ACL
- CORS 默认全开（`cors()` 无参数）

`scripts/check-local-bind.mjs` 是这些约束的回归测试。

---

## 7. 元素数据模型（`src/types.ts`）

```ts
export const elements   = new Map<string, ServerElement>();
export const snapshots  = new Map<string, Snapshot>();
export const files      = new Map<string, ExcalidrawFile>();

export function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).substring(2);
}
```

支持类型（`EXCALIDRAW_ELEMENT_TYPES`）：`rectangle`、`ellipse`、`diamond`、`arrow`、`text`、`line`、`freedraw`、`image`。

`ServerElement` 字段：

| 字段 | 说明 |
|---|---|
| `id, type, x, y, width?, height?, angle?` | 基础几何 |
| `strokeColor`, `backgroundColor`, `fillStyle`, `strokeWidth`, `strokeStyle`, `roughness`, `opacity` | 样式 |
| `locked?`, `groupIds?` | 元数据 |
| `text`, `fontSize`, `fontFamily` | 文本元素（fontFamily 用 1..8 编号映射 Virgil/Helvetica/Cascadia/Excalifont/Nunito/Lilita/Comic） |
| `points`, `startBinding`, `endBinding`, `startArrowhead`, `endArrowhead`, `start?`, `end?` | 箭头/线 |
| `createdAt`, `updatedAt`, `version`, `syncedAt`, `source` | 同步元数据 |

`normalizeFontFamily()` 把 `"virgil"` / `"helvetica"` / `"sans"` / `"mono"` 字符串映射成数字。

**持久化**：仅内存。重启即清空。建议靠 `snapshot_scene` + `export_scene` 做用户级持久。

---

## 8. 前端（`frontend/src/App.tsx`）

```tsx
const App = () => {
  const apiRef = useRef<ExcalidrawImperativeAPI>(null);
  useEffect(() => {
    const ws = new WebSocket(`ws://${location.host}/`);
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.type === "initial_elements") apiRef.current?.updateScene({ elements: msg.elements });
      // ... 处理 element_created / updated / deleted / batch / cleared
      // ... 处理 export_image_request → 调 exportToBlob → POST /api/export/image/result
      // ... 处理 set_viewport → 调 scrollToContent/setZoom → POST /api/viewport/result
      // ... 处理 mermaid_convert → 调浏览器侧 convertMermaidToExcalidraw → POST 结果
    };
  }, []);
  return <Excalidraw excalidrawAPI={(api) => (apiRef.current = api)} />;
};
```

要点：
- WebSocket 自动重连，去抖 sync 避免抖动
- 对 `boundElements` / `containerId` 做清洗，防止远端发来孤儿引用
- Vite dev 模式 `/api` 走代理到 3000
- 生产构建放在 `dist/frontend/`，由 Express 静态托管

---

## 9. Agent Skill (`skills/excalidraw-skill/`)

**SKILL.md frontmatter**（实测）：

```yaml
name: excalidraw-skill
description: Programmatic canvas toolkit for creating, editing, and refining Excalidraw diagrams via MCP tools with real-time canvas sync. Use when an agent needs to (1) draw or lay out diagrams on a live canvas, (2) iteratively refine diagrams using describe_scene and get_canvas_screenshot to see its own work, (3) export/import .excalidraw files or PNG/SVG images, (4) save/restore canvas snapshots, (5) convert Mermaid to Excalidraw, or (6) perform element-level CRUD, alignment, distribution, grouping, duplication, and locking. Requires a running canvas server (EXPRESS_SERVER_URL, default http://127.0.0.1:3000).
```

### 9.1 模式自动检测

Skill 启动流程：
1. 先看 tool list 里有没有 `excalidraw/batch_create_elements` → 有则走 **MCP 模式**
2. 否则尝试 `http://127.0.0.1:3000/health` → 通则走 **REST 模式**（用 `scripts/*.cjs` 兜底）
3. 都不通则给用户安装提示

### 9.2 MCP vs REST 关键差异

来自 `SKILL.md` 内嵌表（重要 — 后续 anetchat 集成时一定要注意）：

1. **标签**：MCP 接受 `text: "My Label"` 直接挂形状；REST 要 `label: { text: "My Label" }`
2. **箭头绑定**：MCP 接受 `startElementId` / `endElementId`；REST 要 `start: { id }` / `end: { id }`
3. **fontFamily**：永远传字符串（如 `"1"`）或不传，绝不要传数字
4. **REST 更新标签**：PUT 必须重传 `label` 才能正常渲染

### 9.3 设计指南内嵌（很重要）

`SKILL.md` 与 `read_diagram_guide` 工具内嵌了大量布局反模式与色板规则，例如：

- ❌ 不要在背景区域 rectangle 上挂 `text`（会变成 bound text 居中 → 与内部元素重叠且无法移动）
- ✅ 区域标签应该用独立的 text 元素放在区域顶部
- 垂直层间距 80–120px；同层水平 40–60px
- 形状宽 `max(160, labelChars * 9)`，避免文本截断
- 区域 padding 50px

这些规则是作者用大量真实 LLM 输出调出来的，**直接复用价值很高**。

### 9.4 Helper 脚本（CJS，REST 兜底）

7 个：`healthcheck`、`export-elements`、`import-elements`、`create-element`、`update-element`、`delete-element`、`clear-canvas`，全部读 `EXPRESS_SERVER_URL` env。

---

## 10. Docker

### 10.1 `Dockerfile`（MCP 镜像）

- 多阶段：`node:18-slim` builder → 编译 TS → production 拷贝 `dist/` 与 `node_modules`
- 非 root（UID 1001）
- ENV: `NODE_ENV=production`、`EXPRESS_SERVER_URL=http://127.0.0.1:3000`、`ENABLE_CANVAS_SYNC=true`
- 通过 stdio 通信，无端口

### 10.2 `Dockerfile.canvas`（Canvas 镜像）

- 三阶段：frontend-builder（vite build）→ backend-builder（tsc）→ production
- 暴露 3000，默认 `HOST=0.0.0.0`（容器内）
- Healthcheck 用 `http://127.0.0.1:3000/health`

### 10.3 `docker-compose.yml`

```yaml
services:
  canvas: ports: ["3000:3000"]; HOST=0.0.0.0; healthcheck → /health
  mcp:    stdin_open: true; depends_on: canvas (service_healthy); profiles: [full]
```

常规用法：`docker-compose up canvas`（MCP 走宿主 Claude Desktop），完整栈用 `docker-compose --profile full up`。

---

## 11. 日志、CI、测试

- **日志**：Winston，console 仅 warn/error 走 stderr（避免污染 stdio 协议），文件日志走平台路径（Linux `~/.local/state/excalidraw-mcp/excalidraw.log`），ANSI 关闭防止 JSON 损坏
- **CI**：`.github/workflows/ci.yml`（Node 18/20/22 矩阵 — type-check + build + artifact 验证）+ `docker.yml`（构建并推 GHCR）
- **测试**：
  - `npm run test:bind` — `scripts/check-local-bind.mjs` 验证 127.0.0.1/IPv6/重复端口
  - 推荐 MCP Inspector：`npx @modelcontextprotocol/inspector --cli -e EXPRESS_SERVER_URL=http://127.0.0.1:3000 -- node dist/index.js --method tools/list`
  - 推荐 `agent-browser` 做前端截图回归

---

## 12. Claude Code / Claude Desktop / Cursor / Codex 接入

### 12.1 Claude Desktop

`~/.config/Claude/claude_desktop_config.json`（Linux）：
```json
{
  "mcpServers": {
    "excalidraw": {
      "command": "node",
      "args": ["/data/projs/anetchat/refs/mcp_excalidraw/dist/index.js"],
      "env": {
        "EXPRESS_SERVER_URL": "http://127.0.0.1:3000",
        "ENABLE_CANVAS_SYNC": "true"
      }
    }
  }
}
```

### 12.2 Claude Code

```bash
claude mcp add excalidraw --scope user \
  -e EXPRESS_SERVER_URL=http://127.0.0.1:3000 \
  -e ENABLE_CANVAS_SYNC=true \
  -- node /data/projs/anetchat/refs/mcp_excalidraw/dist/index.js
```

或项目级：`--scope project`（写入 `.mcp.json`）。

### 12.3 npx 一行起（无需 clone）

```json
{ "mcpServers": { "excalidraw": { "command": "npx", "args": ["-y", "mcp-excalidraw-server"] } } }
```

### 12.4 Agent Skill 用法

```bash
mkdir -p ~/.claude/skills
cp -R /data/projs/anetchat/refs/mcp_excalidraw/skills/excalidraw-skill ~/.claude/skills/
# 在 Claude Code 用 /excalidraw-skill 调用
```

---

## 13. 与 anetchat 的接入路径

**短期方案（最低成本）**：把 Canvas Server 当外部依赖跑在 anetchat backend 旁边
- 优点：零侵入、可独立升级；anetchat 通过 REST `/api/elements/*` + WS 直接驱动 `<Excalidraw />`
- 缺点：多一个进程；无认证；状态在内存

**中期方案（推荐）**：把 `src/server.ts` 的 REST/WS 部分内嵌到 anetchat 自家 Node 服务
- 加 auth middleware（session/JWT）
- 元素表换成 Redis / Postgres（按 chat session 隔离）
- 保留 26 个工具的语义，作为 anetchat 内部 AI tool-call 实现
- `frontend/src/App.tsx` 的 WS 订阅逻辑直接搬到 anetchat 客户端

**长期方案**：完全自研，把 mcp_excalidraw 作为参考实现
- 复用 `read_diagram_guide` 的设计规则
- 复用 `describe_scene` 的 LLM-friendly 描述格式
- 复用 `export_to_excalidraw_url` 的 E2E 加密上传协议
- 复用 Skill manifest 的反模式约束（直接拷贝到 anetchat system prompt）

---

## 14. 已知坑与注意

- **无认证**：直接暴露 0.0.0.0 等于裸奔，必须放在网关后
- **内存状态**：进程重启即丢，需要自己加持久化
- **截图依赖前端**：headless 部署需配 Puppeteer / playwright 渲染
- **路由顺序**：`/api/elements/clear` 必须在 `/api/elements/:id` 之前注册
- **fontFamily 数字 vs 字符串**：REST 与 MCP 不一致，SKILL.md 有警告
- **没有冲突解决**：多 Agent 并发是 last-write-wins，不保证一致性
- **TypeScript 严格但弱 schema 在 server**：内部存的 ServerElement 与 Excalidraw 真实元素结构有差异，落到前端时由 App.tsx 做清洗
- **`get_canvas_screenshot` 阻塞**：MCP 端会等前端回填，超时需自己留 fallback

---

## 15. 许可

MIT License。可自由商用、修改、再分发。

---

## 16. 关键文件索引（本地）

- [`src/index.ts`](../refs/mcp_excalidraw/src/index.ts) — 26 工具实现，AES 加密上传
- [`src/server.ts`](../refs/mcp_excalidraw/src/server.ts) — Express + WS
- [`src/types.ts`](../refs/mcp_excalidraw/src/types.ts) — 模型 + 内存表
- [`src/utils/logger.ts`](../refs/mcp_excalidraw/src/utils/logger.ts) — Winston 平台日志
- [`frontend/src/App.tsx`](../refs/mcp_excalidraw/frontend/src/App.tsx) — 前端 + WS 订阅
- [`skills/excalidraw-skill/SKILL.md`](../refs/mcp_excalidraw/skills/excalidraw-skill/SKILL.md) — Skill manifest + 设计规则
- [`skills/excalidraw-skill/references/cheatsheet.md`](../refs/mcp_excalidraw/skills/excalidraw-skill/references/cheatsheet.md) — API 速查
- [`scripts/check-local-bind.mjs`](../refs/mcp_excalidraw/scripts/check-local-bind.mjs) — 绑定回归测试
- [`docker-compose.yml`](../refs/mcp_excalidraw/docker-compose.yml) — 部署编排
- [`Dockerfile.canvas`](../refs/mcp_excalidraw/Dockerfile.canvas) — 生产 canvas 镜像

参见 [C001-excalidraw.md](./C001-excalidraw.md) 了解被驱动的 `@excalidraw/excalidraw` 组件细节。
