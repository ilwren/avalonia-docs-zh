---
id: configure-vscode-debug-linux
title: 在 Linux 上配置 Android 调试
sidebar_label: Android 调试（Linux）
description: 在 Linux 上配置 Visual Studio Code，用 Mono 调试器构建、部署并调试 Avalonia Android 项目。
doc-type: how-to
---

# 在 Linux 上配置 Android 调试 {#configure-android-debugging-on-linux}

本指南带你在 Linux 上配置 Visual Studio Code，以便构建、部署和调试基于 Avalonia 的 Android 项目。整套流程借助 Mono Debug 扩展，通过本地端口挂接到运行中的 Android 应用。

## 前置条件 {#prerequisites}

动手之前，请确认你具备：

- Linux 上已安装 Visual Studio Code。
- 已安装 .NET SDK（6.0 或更高），且在你的 `PATH` 中可用。
- 有一个正在运行的 Android 模拟器，或一台已开启开发者模式、通过 USB 连接的真机。
- 已从 [Visual Studio 市场](https://marketplace.visualstudio.com/items?itemName=ms-vscode.mono-debug)安装 **Mono Debug** 扩展。

## 配置启动配置文件 {#configure-the-launch-profile}

打开（或新建）工作区中的 `.vscode/launch.json` 文件，添加两项配置：一项先构建部署再挂接，另一项直接挂接到已在运行的应用。

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug - Android",
      "type": "mono",
      "preLaunchTask": "run-debug-android",
      "request": "attach",
      "address": "localhost",
      "port": 10000
    },
    {
      "name": "Attach - Android",
      "type": "mono",
      "request": "attach",
      "address": "localhost",
      "port": 10000
    }
  ]
}
```

`port` 的值可以是任何没被其他应用或系统占用的端口。上面的例子用的是 `10000`。

- **Debug - Android** 会先跑一个预启动任务来构建并部署你的应用，然后挂接调试器。
- **Attach - Android** 跳过构建步骤，直接连上设备或模拟器中已在运行的应用。

## 配置构建任务 {#configure-the-build-task}

打开（或新建）`.vscode/tasks.json` 文件，添加一个在开启 Mono 调试服务器的前提下构建并部署 Android 项目的任务。

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "run-debug-android",
      "command": "dotnet",
      "type": "shell",
      "args": [
        "build",
        "--no-restore",
        "-t:Run",
        "${workspaceFolder}/<ProjectName>.Android.csproj",
        "-p:TargetFramework=net6.0-android",
        "-p:Configuration=Debug",
        "-p:AndroidAttachDebugger=true",
        "-p:AndroidSdbHostPort=10000",
        "-p:AndroidSdbTargetPort=10000"
      ],
      "problemMatcher": "$msCompile"
    }
  ]
}
```

把 `<ProjectName>` 换成你那个 Android 专属 Avalonia 项目的名称。

:::info
`launch.json` 中的 `port` 值必须与 `tasks.json` 中的 `AndroidSdbHostPort` 和 `AndroidSdbTargetPort` 保持一致。若对不上，调试器就连不上。
:::

## 开始调试 {#start-debugging}

1. 在 Visual Studio Code 中打开**运行和调试**面板（Ctrl+Shift+D）。
2. 在配置下拉框中选 **Debug - Android**。
3. 按 **F5** 或点击绿色的播放按钮。

.NET 运行时会构建你的应用并部署到已连接的设备或模拟器上。应用启动后，Mono 调试器便挂接到配置好的端口，你就能照常下断点、查看变量、单步执行了。

若应用已在设备上运行，改选 **Attach - Android** 即可跳过构建、直接连上。

## 另请参阅 {#see-also}

- [IDE 支持](/tools/ide/)
- [Avalonia 工具概述](/tools/)
- [Visual Studio 扩展](/tools/visual-studio-extension)
