---
index: cross-platform-solution-setup
title: 搭建跨平台解决方案
description: 用一个共享的核心项目加上各平台专属的项目头，来组织 Avalonia 解决方案。
doc-type: explanation
---

尽管目标平台五花八门，Avalonia 项目都使用同一种解决方案文件格式（Visual Studio 的 `.SLN` 格式）。解决方案可以在不同开发环境之间共用，让多平台应用开发有一套统一的做法。

创建跨平台应用的第一步是创建解决方案。本节接着讲下一步：如何组织项目，以便用 Avalonia 构建跨平台应用。

## 往解决方案里添内容 {#populating-the-solution}

`Avalonia Cross Platform Application` 模板创建的解决方案结构包含下列项目，以便在多个平台之间共享和复用代码：

:::info
[请先确认已安装 Avalonia 模板。](/docs/get-started/install-avalonia)
:::

### 核心项目 {#core-project}
它是整个应用的心脏，设计上与平台无关，包含应用中所有可复用的部分：业务逻辑、视图模型和视图。其他所有项目都引用这个核心项目。你的大部分开发工作都应落在这里。

### 桌面项目 {#desktop-project}
这个项目让应用能跑在 Windows、macOS 和 Linux 上，输出类型为 `WinExe`。

### Android 项目 {#android-project}
这是一个基于 `NET-Android` 的项目，引用核心项目。它含有一个继承自 `AvaloniaMainActivity` 的 `MainActivity`，作为 Android 应用的入口点。

### iOS 项目 {#ios-project}
这是一个面向 iOS 和 iPadOS 的 `NET-iOS` 项目。它的入口点是继承自 `AvaloniaAppDelegate` 的 `AppDelegate`。

### 浏览器项目 {#browser-project}
这个 WebAssembly（WASM）项目让你的 Avalonia 应用能在网页浏览器中运行，它的 `RuntimeIdentifier` 为 `browser-wasm`。

## 核心项目 {#core-project-1}

共享代码项目只应引用在所有平台上都存在的程序集，通常也就是 `System`、`System.Core`、`System.Xml` 这类通用框架命名空间。

这些共享项目的目标是尽可能多地实现应用功能（包括 UI 部分），从而把代码复用率拉到最高。 

把功能拆进不同层次之后，代码更易于维护、测试，也更容易在多个平台间复用。Avalonia 项目采用的这种分层架构，让应用开发既高效又易于扩展。

## 平台专属的应用项目 {#platform-specific-application-projects}

平台专属项目必须引用核心项目。它们的存在是为了让应用能跑在 iOS、Android、WASM 等各具特点的平台上。

桌面平台虽然可以共用一个项目，但为 macOS 单独建一个采用 [Xamarin.Mac 目标框架](https://learn.microsoft.com/en-us/xamarin/mac/platform/target-framework)的项目往往更划算，这样分发和打包都更省事。

## 另请参阅 {#see-also}

- [跨平台架构](/docs/fundamentals/cross-platform-architecture)：解决方案结构与平台分支模式。