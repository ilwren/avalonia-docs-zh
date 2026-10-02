---
id: index
title: AI Tools
doc-type: overview
---

Avalonia 提供了若干 MCP（模型上下文协议）服务器，把 AI 编程助手接到文档、运行中的应用和打包流程上。你不必再复制错误信息、用文字描述界面长什么样——AI 助手可以自己检索官方文档、检视视觉树、截图、设置属性，还能替你把应用打包好。

## MCP 是什么？ {#what-is-mcp}

模型上下文协议（MCP）是一项开放标准，让 AI 模型通过统一接口使用外部工具和服务。你不用再手动跑命令、把输出粘进聊天框，MCP 让 AI 助手直接调用工具，结构化的数据来回传递。这样一来反馈闭环更紧凑：助手能看见你的应用、做出修改、验证结果，全程不需要你当中间人。

## 受支持的 AI 助手 {#supported-ai-assistants}

每个 MCP 配置页都为下列编辑器和命令行工具给出了分步配置说明：

- VS Code 搭配 GitHub Copilot
- Visual Studio 搭配 Copilot
- JetBrains Rider（AI Assistant 与 Copilot 插件）
- Cursor
- Windsurf
- Claude Code
- Claude Desktop
- Gemini CLI

## Build MCP

Build MCP 服务器让你的 AI 编程助手直接接触 Avalonia 文档和专家级开发规则。助手可以实时检索指南、教程和 API 参考，加载一整套写出地道 Avalonia 代码的规则，并借助预置提示词完成新建项目、照着截图还原界面、把 WPF 应用迁移到 Avalonia 等常见工作流。

Build MCP **免费使用**，既不需要许可证密钥，也不用在本地安装。它以远程服务器的形式运行、通过 HTTP 连接，配置只需几秒钟。

[配置 Build MCP](/tools/ai-tools/build-mcp)

## Charts MCP

Charts MCP 服务器让 AI 助手能生成 Avalonia 图表预览和代码。它可以从一众图表生成工具中挑选（笛卡尔类、环形类、仪表类、金融类等），然后返回渲染好的 PNG 预览图以及生成的 C# 和 XAML 代码片段。

当你想试试有哪些图表类型、验证数据结构、挑一套配色，或是想要一份 Avalonia 图表实现的起步代码时，就用 Charts MCP。

[配置 Charts MCP](/tools/ai-tools/charts-mcp)

## DevTools MCP

DevTools MCP 服务器让 AI 助手直接接触你正在运行的 Avalonia 应用。它可以连上运行中的应用或 XAML 预览器，检视视觉树，按类型或名称查找元素，读取和修改属性，截图，还能发送输入事件。

这在排查布局问题时尤其管用。你不用费口舌描述问题，AI 助手自己就能看见它、查看相关属性，并在同一段对话里给出甚至直接应用修复。

[配置 DevTools MCP](/tools/developer-tools/mcp)

## Parcel MCP

Parcel MCP 服务器让 AI 助手接手应用打包的活儿。它可以从你的 .NET 项目生成 Parcel 配置，配置代码签名与公证，并为 Windows、macOS 和 Linux 构建安装包。

有了 Parcel MCP 服务器，你只需用大白话说清想要什么，配置和执行（包括 macOS 的签名与公证）都由 AI 助手搞定。

[配置 Parcel MCP](/tools/parcel/mcp)

## 另请参阅 {#see-also}

- [Build MCP](/tools/ai-tools/build-mcp)
- [Charts MCP](/tools/ai-tools/charts-mcp)
- [DevTools MCP](/tools/developer-tools/mcp)
- [Parcel MCP](/tools/parcel/mcp)
- [Avalonia 工具概述](/tools/)
