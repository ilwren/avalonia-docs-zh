---
id: developer-tools
title: 开发者工具问题
sidebar_label: 开发者工具
description: 排查开发者工具的常见毛病，包括连接失败、日志缺失和诊断配置。
doc-type: troubleshooting
tags:
  - avalonia plus
  - avalonia pro
  - avalonia enterprise
---

## 反馈问题 {#reporting-issues}

开发者工具用一个 GitHub 仓库跟踪缺陷和功能请求：[AvaloniaUI/AvaloniaUI.DeveloperTools](https://github.com/AvaloniaUI/AvaloniaUI.DeveloperTools/issues)。

提交问题之前，请至少把下列信息收集齐：

1. 问题的复现步骤。
2. 你的操作系统及版本。
3. 你的应用所面向的 Avalonia 版本。
4. 你配置过的任何非默认 `DeveloperToolsOptions` 取值。
5. 开发者工具和诊断支持的日志（见下文）。

## 开发者工具起不来或挂接不上 {#developer-tools-does-not-launch-or-attach}

若开发者工具打不开，或挂接不上你的应用，请逐项排查：

- **确认 NuGet 包已安装。**你的项目必须引用 `Avalonia.Diagnostics` 包（若用的是独立版工具，则要确认已单独装好开发者工具）。另请核对包版本与 Avalonia 版本是否相符。
- **确认调用了 `AttachDeveloperTools`。**在 `App.axaml.cs` 或启动代码中，确保你调用了 `application.AttachDeveloperTools()`。少了这一步，诊断支持库根本不会初始化。
- **确认进程没有被防火墙或杀毒软件拦下。**独立的开发者工具进程通过本地连接与你的应用通信，安全软件偶尔会拦住这类流量。
- **留意端口冲突。**若另一个进程占着同一个端口，连接可能悄无声息地失败。请查看诊断支持日志（见下文）中的连接错误。
- **把两个进程都重启一遍。**若你更新过 Avalonia 或开发者工具包，请关掉应用和开发者工具进程，再把两者重新启动。

## 获取开发者工具日志 {#obtaining-developer-tools-logs}

开发者工具进程会收集日志、分批写盘。日志目录因平台而异。

**Windows:**

```text
%LocalAppData%\AvaloniaUI\com.AvaloniaUI.Net.DeveloperTools\Logs\
```

**Linux:**

```text
~/.local/share/AvaloniaUI/com.AvaloniaUI.Net.DeveloperTools/Logs/
```

**macOS:**

```text
~/Library/Application Support/AvaloniaUI/com.AvaloniaUI.Net.DeveloperTools/Logs/
```

若日志目录压根不存在，说明开发者工具可能就没成功跑起来。试着手动启动它，看看终端或控制台输出里有什么报错。

### 日志文件是空的，或者根本没有 {#log-files-are-empty-or-missing}

- 日志是分批写入的，会话太短可能什么都写不出来。关闭之前，至少让开发者工具开上几秒钟。
- 在 Linux 上，请确认 `~/.local/share` 目录对你的用户账户可写。
- 在 macOS 上，请确认 `~/Library/Application Support` 目录没有被系统隐私设置限制。

## 获取诊断支持日志 {#obtaining-diagnostics-support-logs}

诊断支持是跑在你应用进程里的集成库，负责与开发者工具进程建立连接。

它默认不写任何日志。要启用日志，请在挂接时配置 `DeveloperToolsOptions`：

```csharp
application.AttachDeveloperTools(o =>
{
    // CreateConsole returns a built-in implementation that writes to Console.Out and Console.Error.
    o.DiagnosticLogger = DiagnosticLogger.CreateConsole(LogEntryVerbosity.Verbose);
});
```

启用之后，诊断消息会出现在应用的标准输出中。若你从 IDE 里运行，请查看**输出**或**调试控制台**窗口。

### 自定义日志实现 {#custom-logger-implementations}

若往控制台输出不方便（比如在生产环境做诊断），你可以用 `CreateTextWriter` 工厂方法造一个把日志写进文件的 `DiagnosticLogger`：

```csharp
var writer = new StreamWriter("diagnostics.log", append: true);
```

然后把它传进选项里：

```csharp
application.AttachDeveloperTools(o =>
{
    o.DiagnosticLogger = DiagnosticLogger.CreateTextWriter(writer, LogEntryVerbosity.Verbose);
});
```

## 常见问题 {#common-issues}

| 现象 | 可能的原因 | 解决办法 |
|---|---|---|
| 开发者工具窗口开了，却看不到视觉树 | 应用尚未初始化完毕 | 等主窗口出现，或者在 `OnFrameworkInitializationCompleted` 之后再调用 `AttachDeveloperTools` |
| 诊断日志中出现 “Connection refused” | 端口冲突，或防火墙拦下了本地流量 | 检查端口占用情况和防火墙规则 |
| 日志目录在，里面却没有近期的文件 | 开发者工具在把这批日志刷盘之前就崩了 | 复现一次问题，并在关闭前让开发者工具多开一会儿 |
| 断点或属性修改不起作用 | `Avalonia.Diagnostics` 与你的 Avalonia 运行时版本不匹配 | 确保所有 Avalonia 包版本一致 |

## 另请参阅 {#see-also}

- [安装开发者工具](/tools/developer-tools/installation)
- [挂接应用](/tools/developer-tools/attaching-applications)
- [开发者工具选项](/tools/developer-tools/options)
- [元素工具](/tools/developer-tools/elements-tool)
