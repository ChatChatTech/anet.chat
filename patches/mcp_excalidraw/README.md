# mcp_excalidraw 二次定制 patch

我们用的 [mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) 上游做了几处定制，但因为该仓库 clone 到 `refs/` 后不应被 git 跟踪（外部源码 + 体积大），这里以 patch 形式保留我们的修改。

## 修改清单

| 项 | 文件 | 说明 |
|---|---|---|
| 1 | `frontend/src/App.tsx` | 顶栏 `<h1>` 改 "anet.chat"；引入 `MainMenu` 自定义菜单（删 GitHub/Discord/Follow us，加 "Join Agent Network" 指向 agentnetwork.org.cn）；启动时自动加载 `public/libraries/` 下的 .excalidrawlib |
| 2 | `frontend/index.html` | `<title>anet.chat</title>`；CSS 隐藏 `.HelpDialog__header`（去掉 Documentation / Read our blog / Found an issue / YouTube 一行链接） |
| 3 | `frontend/public/libraries/*.excalidrawlib` | 6 个高价值 Excalidraw libraries 预装（Software Architecture / AWS / Azure / Information Architecture / Lo-Fi Wireframing / Stick Figures） |

## 应用方式

从 anetchat repo 根目录：

```bash
# 1. 应用 frontend 改动（修改 App.tsx + index.html）
cd refs/mcp_excalidraw && git apply ../../patches/mcp_excalidraw/frontend.patch

# 2. 拷贝预装 libraries
mkdir -p refs/mcp_excalidraw/frontend/public
cp -r ../../patches/mcp_excalidraw/public/libraries refs/mcp_excalidraw/frontend/public/

# 3. 重建 canvas 镜像
cd ../.. && docker compose -f refs/mcp_excalidraw/docker-compose.yml --profile full build canvas
```

## 上游 commit 锚点

patch 是从上游 main 分支生成的。如果上游更新，可能需要 `git apply --3way`。
