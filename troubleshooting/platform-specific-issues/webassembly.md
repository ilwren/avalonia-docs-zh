---
id: webassembly
title: WebAssembly 问题
sidebar_label: WebAssembly
description: 排查在浏览器中以 WebAssembly 方式运行 Avalonia 应用时的常见问题，包括原生库报错、构建失败和性能方面的考量。
doc-type: troubleshooting
---

## `System.DllNotFoundException: libSkiaSharp`

这个错误通常意味着 `wasm-tools` 工作负载没装。装上它再重新构建：

```bash
dotnet workload install wasm-tools
```

若装了工作负载仍然报错，请在项目文件中加上 `WasmBuildNative` 属性：

```xml
<PropertyGroup>
    <WasmBuildNative>true</WasmBuildNative>
</PropertyGroup>
```

然后彻底清理并重新构建：

```bash
dotnet clean
dotnet build
```

:::tip
若你用的是 CI/CD 流水线，请确保构建步骤之前，构建环境中已装好 `wasm-tools` 工作负载。
:::

## 构建因 `wasm-tools` 版本不匹配而失败 {#build-fails-with-wasm-tools-version-mismatch}

当你的 .NET SDK 版本与已装的 `wasm-tools` 工作负载版本对不上时，构建可能抛出一堆莫名其妙的错误。把两者都更新到彼此兼容的版本即可：

```bash
dotnet workload update
```

若你在 `global.json` 文件中固定了某个 .NET SDK 版本，请确认它与你装的工作负载相匹配。

## 应用加载了，却是一片空白 {#app-loads-but-displays-a-blank-screen}

若应用编译无误、浏览器也顺利打开了页面，屏幕上却什么都没渲染出来，请逐项排查：

1. **浏览器控制台错误。**打开浏览器开发者工具（F12），看看有没有 JavaScript 异常或失败的网络请求。
2. **静态资产缺失。**确认所需的静态 Web 资产（字体、图片、样式表）都包含在发布输出里，核对一下 `wwwroot` 文件夹的内容。
3. **入口点不对。**确认你的 `index.html` 引用的是构建生成的那个正确的 `.js` 引导文件。
4. **内容安全策略（CSP）限制。**若你把应用部署在反向代理或 CDN 后面，请确认 CSP 头放行了 .NET WebAssembly 运行时所需的 `wasm-eval` 或 `unsafe-eval`。

## 调试 WebAssembly 应用 {#debugging-webassembly-applications}

在浏览器里调试 Avalonia WebAssembly 应用需要基于 Chromium 的浏览器（Chrome 或 Edge）。启用调试的步骤：

1. 以启用调试代理的方式启动应用：

    ```bash
    dotnet run --configuration Debug
    ```

2. 在 Chrome 或 Edge 中打开控制台输出里给出的 URL。
3. 按 **Shift+Alt+D** 打开调试面板。

:::note
断点、变量查看和单步调试都能用，只是比原生平台慢一些。热重载也支持，但某些类型的改动可能需要整页刷新。
:::

## 调用外部 API 时报 CORS 错误 {#cors-errors-when-calling-external-apis}

由于应用跑在浏览器里，所有 HTTP 请求都受跨源资源共享（CORS）策略约束。若 API 调用因 CORS 报错失败：

- 确认目标 API 服务器返回了恰当的 `Access-Control-Allow-Origin` 响应头。
- 若 API 在你手上，请为你应用的来源加上 CORS 中间件或响应头。
- 若改不了目标 API 的 CORS 配置，不妨用一个后端代理来转发请求。

## 下载体积过大 {#large-download-size}

WebAssembly 应用首次下载的体积往往不小，因为 .NET 运行时和所有引用的程序集都得送到浏览器。想把体积压下来：

- 在项目文件中启用裁剪：

    ```xml
    <PropertyGroup>
        <PublishTrimmed>true</PublishTrimmed>
    </PropertyGroup>
    ```

- 在 Web 服务器上为 `.wasm` 和 `.dll` 文件启用 Brotli 或 Gzip 压缩。
- 删掉用不上的 NuGet 包引用，尽量减少程序集数量。
- 用 AOT 编译改善启动性能，代价是二进制更大（但加载更快）：

    ```xml
    <PropertyGroup>
        <RunAOTCompilation>true</RunAOTCompilation>
    </PropertyGroup>
    ```

:::caution
裁剪可能把应用通过反射用到的代码一并剪掉。若启用裁剪后运行时出现 `MissingMethodException` 或 `TypeLoadException` 错误，你可能需要添加 trim-root 程序集或 `DynamicDependency` 特性，把必需的类型保住。
:::

## 总体限制 {#general-limitations}

WebAssembly 是个沙箱环境，天生就有一些限制：

- 应用跑在浏览器沙箱里，文件系统访问、网络访问以及其他系统级 API 都只能在浏览器允许的范围内施展。
- 浏览器中的 .NET 多线程自 .NET 8 起才可用，且需要浏览器配合——并非所有浏览器都支持线程所需的 `SharedArrayBuffer`。
- 图形界面性能可能不如原生平台，在较老的浏览器或低功耗设备上尤其明显。
- 在多数浏览器中，剪贴板访问仅限于由用户操作触发的场景。
- 没有原生文件对话框。请用浏览器的文件输入元素，或通过 JavaScript 互操作来处理文件选择。

## 另请参阅 {#see-also}

- [Avalonia WebAssembly 概述](/docs/platform-specific-guides/webassembly)
- [应用性能问题](/docs/app-development/performance)
