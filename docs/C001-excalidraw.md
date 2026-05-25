# C001 — Excalidraw 调研文档

> 仓库：https://github.com/excalidraw/excalidraw
> 本地路径：`/data/projs/anetchat/refs/excalidraw`
> 调研日期：2026-05-25
> 目的：理解 Excalidraw 的架构、对外 API、协作机制与可嵌入方式，为 anetchat 集成"实时白板/示意图"能力打基础。

---

## 1. 项目定位与选型理由

Excalidraw 是一个 **开源、端到端加密、手绘风格** 的虚拟白板。核心卖点：

- **手绘风格**：基于 Rough.js，所有几何图形带有"潦草"质感，天然适合脑暴、架构示意。
- **零后端 / 可自托管**：作为纯前端 React 组件可独立运行；协作功能需要 Firebase + Socket.io 后端。
- **MIT License**：商用、二次封装皆可。
- **可嵌入**：发布在 npm 的 `@excalidraw/excalidraw` 包就是一个 React 组件，开放 `excalidrawAPI` imperative handle，可被宿主程序完全控制。
- **AI 友好**：内置 Magic Frame、Diagram-to-Code、Text-to-Diagram (TTDDialog)、Mermaid 转换等能力，已经面向 AI 场景做了铺垫。
- **丰富的导入导出**：`.excalidraw` JSON、`.excalidrawlib`、PNG/SVG/Clipboard/可分享 URL。

→ 对 anetchat 来说，这是把"AI 输出图示"做成实时画布最干净的方案。

---

## 2. 仓库布局

Yarn Workspaces 单体仓库，Node ≥ 18，Yarn 1.22.22。

| 路径 | 角色 |
|---|---|
| `excalidraw-app/` | excalidraw.com SaaS 应用（Vite + React 19），包含协作、Firebase、PWA |
| `packages/excalidraw/` | npm 包 `@excalidraw/excalidraw`（核心 React 组件）— 主入口 `index.tsx` |
| `packages/common/` | 共享常量：`THEME`、`FONT_FAMILY`、`COLOR_PALETTE`、`MIME_TYPES` |
| `packages/element/` | 元素数据模型与几何运算 — `types.ts` 定义 `ExcalidrawElement` |
| `packages/math/` | 坐标变换、几何工具 |
| `packages/utils/` | 导出、边界、嵌入工具 |
| `packages/fractional-indexing/` | 协作场景下保持稳定排序的小数索引算法 |
| `examples/with-script-in-browser/` | 用 `<script>` 标签直接引入的最小示例 |
| `examples/with-nextjs/` | Next.js 集成示例 |
| `firebase-project/` | Firestore 规则、Cloud Storage 规则（协作后端）|
| `dev-docs/` | Docusaurus 开发者文档站 |
| `scripts/` | `buildPackage.js` 等发布脚本 |

构建产物：`packages/*/dist/`（dev + prod 双份），`excalidraw-app/build/`。

---

## 3. 构建与工具链

- **打包器**：Vite 5（应用 & 示例）+ ESBuild（npm 包构建脚本 `scripts/buildPackage.js`）
- **类型**：TypeScript 5.9 strict，path alias `@excalidraw/common`、`@excalidraw/element`、`@excalidraw/excalidraw` 指向 `packages/*/src/index.ts`
- **测试**：Vitest 3.0.6 + jsdom，覆盖阈值 60% lines / 70% branches
- **关键脚本**：
  - `yarn build:packages` — 按依赖顺序构建内部包
  - `yarn build:app` — 生产构建（注入 git SHA、Sentry 等）
  - `yarn start` — 端口 3000 dev server
  - `yarn test:all` — typecheck + lint + format + tests

npm 包发布（`packages/excalidraw/package.json`）输出双重 ESM：`dist/dev/` 与 `dist/prod/`，并把 `./common/*` `./element/*` `./math/*` `./utils/*` 作为 sub-path 暴露，CSS 单独导出。

---

## 4. `@excalidraw/excalidraw` 组件 API

### 4.1 基本用法

```tsx
import { Excalidraw } from "@excalidraw/excalidraw";
import "@excalidraw/excalidraw/index.css";

export default function Board() {
  return (
    <Excalidraw
      onChange={(elements, appState, files) => { /* save / sync */ }}
      excalidrawAPI={(api) => { window.__excalidrawAPI = api; }}
      theme="dark"
      viewModeEnabled={false}
      zenModeEnabled={false}
      gridModeEnabled={true}
      langCode="zh-CN"
      initialData={{ elements: [], appState: {}, files: {} }}
    />
  );
}
```

定义位置：[`packages/excalidraw/index.tsx`](../refs/excalidraw/packages/excalidraw/index.tsx)，`Excalidraw = React.memo(ExcalidrawBase, areEqual)`。

### 4.2 ExcalidrawProps 核心字段

来自 `packages/excalidraw/types.ts:L570-714`：

| 类别 | 字段 |
|---|---|
| **数据回调** | `initialData`（Promise 也可）、`onChange(elements, appState, files)`、`onIncrement` |
| **API 暴露** | `excalidrawAPI(api)`、`onMount`、`onUnmount` |
| **视图模式** | `viewModeEnabled`、`zenModeEnabled`、`gridModeEnabled`、`theme`、`name` |
| **国际化** | `langCode`（默认 `en`，支持中文等几十种） |
| **UI 自定义** | `UIOptions`（细到每个工具按钮、菜单）、`renderTopLeftUI`、`renderTopRightUI`、`renderCustomStats`、`renderEmbeddable` |
| **嵌入控制** | `validateEmbeddable: boolean \| string[] \| RegExp[] \| ((url) => boolean)` |
| **交互** | `onPointerUpdate`、`onPointerDown`、`onPointerUp`、`onScrollChange`、`onPaste`、`onDuplicate`、`onLinkOpen` |
| **库管理** | `libraryReturnUrl`、`onLibraryChange` |
| **AI 功能** | `aiEnabled`、`generateLinkForSelection`、`onExport` |
| **图片** | `imageOptions`（最大尺寸/大小）、`generateIdForFile` |

### 4.3 命名导出（重要）

```ts
// 类型 / 常量
export { THEME, MIME_TYPES, FONT_FAMILY, ROUNDNESS };

// 数据工具
export {
  serializeAsJSON, loadFromBlob, loadSceneOrLibraryFromBlob,
  restoreElements, restoreAppState, restoreElement,
  reconcileElements,            // 协作场景合并远端
  getSceneVersion, hashElementsVersion,
};

// 导出
export {
  exportToCanvas, exportToBlob, exportToSvg, exportToClipboard,
};

// 坐标 / 几何
export {
  sceneCoordsToViewportCoords, viewportCoordsToSceneCoords,
  getCommonBounds, getVisibleSceneBounds,
  convertToExcalidrawElements,  // 用宽松对象（如 {type,x,y,text}）生成完整元素
};

// AI
export { TTDDialog, TTDDialogTrigger, TTDStreamFetch, DiagramToCodePlugin };
```

### 4.4 `ExcalidrawImperativeAPI`（命令式句柄）

来自 `types.ts:L943-1013`，是最常用的"远程驱动"入口。anetchat 后端要实时下发元素，最终就是调它。

| 类别 | 方法 |
|---|---|
| 场景管理 | `updateScene({ elements?, appState?, collaborators?, captureUpdate? })`、`getSceneElements()`、`getSceneElementsIncludingDeleted()`、`resetScene()`、`applyDeltas(deltas)` |
| 历史 | `history.clear()` |
| 文件 | `getFiles()`、`addFiles(BinaryFileData[])`、`updateLibrary(items)` |
| 视图 | `scrollToContent()`、`refresh()`、`setActiveTool(tool)`、`setCursor`、`resetCursor`、`toggleSidebar`、`updateFrameRendering` |
| 通知 | `setToast({ message, closable, duration })` |
| 订阅 | `onChange`、`onIncrement`、`onPointerDown`、`onPointerUp`、`onScrollChange`、`onStateChange`、`onEvent`、`onUserFollow` —— 全部返回 `UnsubscribeCallback` |
| 元信息 | `getAppState()`、`getName()`、`id`、`isDestroyed`、`registerAction` |

> **集成要点**：`updateScene` 是幂等的覆盖式 API；要做增量协同必须配合 `version` / `versionNonce` / 小数 `index` 字段。如果只是单端 AI 输出，直接每次 `updateScene({ elements: newElements })` 即可。

---

## 5. 数据模型（元素 / AppState / Files）

### 5.1 `ExcalidrawElement` 公共字段（`packages/element/src/types.ts:L40-82`）

```ts
type _ExcalidrawElementBase = {
  id: string;
  x: number; y: number; width: number; height: number; angle: number;
  strokeColor: string; backgroundColor: string;
  fillStyle: "hachure" | "cross-hatch" | "solid" | "zigzag";
  strokeWidth: number; strokeStyle: "solid" | "dashed" | "dotted";
  roughness: number; opacity: number;
  roundness: null | { type: number; value?: number };
  seed: number;                       // Rough.js 随机种子，决定"潦草度"形状
  version: number; versionNonce: number;
  index: FractionalIndex;             // 协作排序键
  isDeleted: boolean;
  groupIds: string[]; frameId: string | null;
  boundElements: { id: string; type: ... }[] | null;
  updated: number;                    // epoch ms
  link: string | null; locked: boolean;
  customData?: Record<string, any>;
};
```

### 5.2 元素变体

| `type` | 含义 |
|---|---|
| `rectangle` / `ellipse` / `diamond` | 基础形状 |
| `text` | 文本（`fontSize`、`fontFamily`、`textAlign`、`verticalAlign`、`containerId`、`autoResize`、`lineHeight`） |
| `line` / `arrow` | 线/箭头（`points`、`startArrowhead`、`endArrowhead`、`startBinding`/`endBinding` 绑定到形状） |
| `freedraw` | 手绘笔迹（`pressures[]`、`simulatePressure`） |
| `image` | 图片（`fileId` 引用 `BinaryFiles`，`status: pending\|saved\|error`、`scale`、`crop`） |
| `frame` | 普通分组框 |
| `magicframe` | AI 生成框（`customData.generationData` 跟踪状态） |
| `embeddable` | 第三方嵌入（YouTube、Spotify 等） |
| `iframe` | 通用 iframe（含 `video` / `generic` / `document` 子类） |

### 5.3 `AppState`（应用状态）

包含 `activeTool`、`selectedElementIds`、`selectedGroupIds`、`zoom: {value}`、`scrollX/Y`、`theme`、`viewBackgroundColor`、`gridSize/gridModeEnabled`、`isBindingEnabled`、`editingTextElement`、`croppingElementId`、`collaborators: Map<SocketId, Collaborator>`、`snapLines`、`hoveredElementIds` 等。

### 5.4 `BinaryFiles`

```ts
type BinaryFileData = {
  id: FileId;                          // 由 generateIdForFile 生成
  mimeType: IMAGE_MIME_TYPES | "application/octet-stream";
  dataURL: string;                     // data:image/png;base64,...
  created: number;                     // epoch ms
  lastRetrieved?: number; version?: number;
};
```

> 重要：图片元素只引用 `fileId`，二进制走 `getFiles()` / `addFiles()` 通道。意味着远程同步图片需要单独传 file blob。

---

## 6. 渲染管线

双 canvas 分层（`packages/excalidraw/renderer/`）：

1. **`staticScene.ts`** — 静态层（网格 + 元素本体），仅在场景变化时重绘
2. **`interactiveScene.ts`** — 交互层（选择框、把手、协作者光标、对齐辅助线），跟随鼠标重绘
3. **`staticSvgScene.ts`** — 导出 SVG 时的并行实现

**手绘风格**核心：[Rough.js 4.6.4](https://github.com/rough-stuff/rough)，`RoughCanvas` / `RoughSVG` 用 `element.seed` 做确定性渲染，所以相同元素在不同客户端"潦草度"一致。

**网格**：theme-aware，明亮主题 `#dddddd`，暗色用 dark mode filter，100% zoom 下 1px 像素对齐。

**Frame**：基于 Canvas clipping region 实现内容裁剪，支持嵌套。

---

## 7. 协作（excalidraw-app/collab）

仅用于 excalidraw.com SaaS；自托管/嵌入场景如果不需要协作可完全忽略。

- **传输**：[socket.io-client 4.7.2](https://socket.io/)
- **房间模型**：`roomId` + `roomKey` 共享在 URL fragment（`#room=...,...`）
- **端到端加密**：AES-GCM 128，密钥仅存在 URL fragment（不上传服务器），服务器只见密文
- **后端**：Firebase Firestore 存场景元数据，Cloud Storage 存图片二进制
- **关键文件**：`excalidraw-app/collab/Collab.tsx`、`Portal.tsx`
- **事件**：`init-room`、`new-user`、`room-user-change`、`server-broadcast`、`server-volatile-broadcast`
- **冲突解决**：`reconcileElements(localElements, remoteElements, localAppState)` —— 基于 `version` + `versionNonce` + `updated` 时间戳 + 小数 `index` 排序合并
- **空闲检测**：`IDLE_THRESHOLD` 用于显示协作者状态

---

## 8. 持久化与文件格式

- **本地**：浏览器 IndexedDB，通过 [`idb-keyval`](https://github.com/jakearchibald/idb-keyval) 自动保存
- **`.excalidraw` 文件**：MIME `application/vnd.excalidraw+json`，结构 `{ type, version: 2, source, elements, appState, files }`
- **`.excalidrawlib`**：可复用元素库，包含 `libraryItems`
- **可分享链接**：完整场景加密+压缩后存到对象存储，URL fragment 携带密钥（与协作相同的 E2E 模型）

---

## 9. Mermaid / Text-to-Diagram

依赖 `@excalidraw/mermaid-to-excalidraw` 2.2.2。

- `packages/excalidraw/mermaid.ts:isMaybeMermaidDefinition(text)` 用关键字嗅探 `flowchart` / `graph` / `sequenceDiagram` / `classDiagram` / `stateDiagram` / `erDiagram` / `journey` / `gantt` / `pie` / `quadrantChart` / `requirementDiagram` / `gitGraph` / `C4Context` / `mindmap` / `timeline` / `zenuml` / `sankey` / `xychart` / `block`
- UI：`components/TTDDialog/`，CodeMirror 编辑器 + 流式拉取（`TTDStreamFetch`）
- Vite 单独打包成 `mermaid-to-excalidraw` chunk，懒加载

集成思路：anetchat 可让模型先输出 Mermaid，前端调用 `parseMermaidToExcalidraw()` → 拿到 `{elements, files}` → 喂给 `excalidrawAPI.updateScene()`。

---

## 10. 嵌入 / iframe / Embeddable

- `validateEmbeddable` 控制白名单：`false` 关闭、`true` 全开、`string[]` 域名、`RegExp[]` 模式、`(url) => boolean` 自定义
- `renderEmbeddable(element, appState) → JSX.Element | null` —— 可以完全接管渲染（例如把某个 URL 渲染成自定义 React 组件而不是 iframe）
- IframeData 支持 sandbox 属性与内置尺寸

→ 这是把 anetchat 自家组件（比如代码片段、聊天记录卡片）"塞进"画布的官方扩展点。

---

## 11. AI 能力（内置）

| 功能 | 入口 |
|---|---|
| **Magic Frame** | `setActiveTool({ type: "magicframe" })` → 画一个框，框里的内容会被发送到后端 AI 转成 HTML/Mermaid/Excalidraw |
| **DiagramToCodePlugin** | `<DiagramToCodePlugin generate={async ({ elements }) => ...}>` —— 把选中的元素发给后端 LLM 生成代码 |
| **TTDDialog** | `<TTDDialog onTextSubmit={...}>` —— 文本生图对话框，前端调用宿主 LLM |
| **`generationData`** | 元素 `customData.generationData = { status, code, error }` 跟踪 AI 生成状态 |

`aiEnabled` prop 一键开关所有 AI UI 按钮。后端 endpoint 由宿主提供，Excalidraw 只负责前端流程。

---

## 12. 测试

- Vitest + jsdom，`vitest.config.mts`，parallel hooks
- 单测覆盖 `restore` / `reconcile` / 几何函数
- 快照测试覆盖关键组件
- 覆盖阈值：60% lines / 70% branches / 63% functions

---

## 13. 在第三方项目中消费的两条路径

### 13.1 作为 npm 组件（推荐 — anetchat 的方向）

```bash
npm install @excalidraw/excalidraw react react-dom
```

```tsx
"use client";              // Next.js App Router
import dynamic from "next/dynamic";
const Excalidraw = dynamic(
  async () => (await import("@excalidraw/excalidraw")).Excalidraw,
  { ssr: false }
);
```

注意点：
- **必须客户端渲染**：组件使用 `window` / `document`，SSR 会炸。Next.js 必走 `dynamic({ ssr: false })`。
- **必须导入 CSS**：`import "@excalidraw/excalidraw/index.css"`。
- **字体子集化**：生产构建会从同源加载字体文件，自托管需要把 `node_modules/@excalidraw/excalidraw/dist/prod/fonts` 暴露在 `/assets/fonts`。

### 13.2 作为 `<script>` 标签（CDN）

```html
<script src="https://cdn.jsdelivr.net/npm/@excalidraw/excalidraw@latest/dist/excalidraw.production.min.js"></script>
<script>
  const { Excalidraw } = window.ExcalidrawLib;
</script>
```

### 13.3 自托管完整 excalidraw.com

`yarn build:app` → `excalidraw-app/build/` → 静态托管 + Firebase 配置 + Socket.io server。除非要私有协作，否则不必走这条。

---

## 14. 许可与运营

- **MIT License**（自由商用、修改、再分发，须保留版权声明）
- **公司形态**：背后有 Excalidraw+（SaaS 增强版）作为商业化产品，开源版本不包含 Excalidraw+ 专属功能
- **社区**：GitHub PR 流程，CI 跑 typecheck / lint / vitest，Husky pre-commit
- **国际化**：通过 Crowdin（`crowdin.yml`），社区翻译

---

## 15. 对 anetchat 的集成建议

1. **基础架构**：把 `<Excalidraw />` 包成 anetchat 的 `<AIWhiteboard />` 客户端组件，对外只暴露 `value`（elements + files）+ `onChange` + `aiBus`（指令流）。
2. **AI 下发链路**：模型输出 → 经 zod 校验 → `convertToExcalidrawElements()` → `excalidrawAPI.updateScene({ elements, appState })`。先不做 reconcile，单端覆盖即可。
3. **图片元素**：模型若要插图，先走 `addFiles([{ id, mimeType, dataURL }])`，再在 element 里引用 `fileId`。
4. **Mermaid 通道**：让模型优先吐 Mermaid（更稳定），前端用 `@excalidraw/mermaid-to-excalidraw` 转换。
5. **AI 能力复用**：保留 `aiEnabled=true`，让 Magic Frame / Diagram-to-Code 直接走 anetchat 后端 LLM endpoint，不重造轮子。
6. **嵌入聊天卡片**：用 `validateEmbeddable` 白名单 + `renderEmbeddable` 把 anetchat 消息卡片塞进画布。
7. **远程驱动**：参考 [C002](./C002-mcp_excalidraw.md) — mcp_excalidraw 已经把"AI Agent → MCP → Canvas REST → WebSocket → updateScene"这条链路完整实现，可以直接复用或裁剪。
8. **协作（可选）**：自带 socket.io 协议复杂，若 anetchat 要做实时多人，建议先用 Liveblocks / Yjs 替代而非套 Firebase。

---

## 16. 参考文件清单（本地）

- `packages/excalidraw/index.tsx` — 主入口、所有命名导出
- `packages/excalidraw/types.ts` — `ExcalidrawProps`、`ExcalidrawImperativeAPI`
- `packages/element/src/types.ts` — 元素数据模型
- `packages/excalidraw/data/` — restore / reconcile / serialize / blob
- `packages/excalidraw/scene/`、`packages/excalidraw/renderer/` — 渲染管线
- `packages/excalidraw/mermaid.ts` — Mermaid 检测
- `excalidraw-app/collab/Collab.tsx`、`Portal.tsx` — 协作
- `excalidraw-app/data/firebase.ts` — Firebase 持久化
- `firebase-project/` — Firestore + Storage 安全规则
- `examples/with-nextjs/` — Next.js 集成示例（anetchat 复用基线）
- `dev-docs/` — 官方开发者文档（Docusaurus）

---

## 17. 风险与注意事项

- **React 19 依赖**：v0.18+ 已经迁到 React 19；anetchat 若在 React 18 项目里集成需固定 v0.17 或同步升级。
- **包体积**：完整组件 ~600KB gzipped，含 Rough.js + i18n + Mermaid lazy chunk；首屏要懒加载。
- **字体许可**：自带 Virgil/Cascadia 等字体走 SIL OFL，自托管要把字体文件随包发出。
- **SSR 严格不可用**：任何 `import { Excalidraw }` 在 SSR 路径上都会立即报错。
- **API breaking change 频率中等**：v0.17 → v0.18 改了 imperative API 形状（`excalidrawAPI` 取代了旧的 `excalidrawRef`），升级时注意。
