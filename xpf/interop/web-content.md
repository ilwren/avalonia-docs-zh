---
id: web-content
title: Web Content Embedding
---

XPF 提供了好几种在应用中嵌入网页内容的方案，选哪一种取决于你面向的平台和嵌入方式上的要求。

## 平台对照 {#platform-comparison}

| 特性 | CefSharp | NativeWebView | NativeWebDialog | DotNetBrowser |
|---|---|---|---|---|
| Windows | Supported | Supported | Supported | Supported |
| macOS | 不支持 | Supported | Supported | Supported |
| Linux | 不支持 | 不支持 | Supported | Supported |
| Embedding | 窗口内控件 | 窗口内控件 | 独立对话框 | 窗口内控件 |
| 键盘输入 | Full | Full | Limited | Full |
| 样式/CSS 控制 | Full | Full | Limited | Full |
| Engine | Chromium | WebView2 / WebKit | WebKit / WebView2 | Chromium |

## XPF WebView（NativeWebView 和 NativeWebDialog） {#xpf-webview-nativewebview-and-nativewebdialog}

`Avalonia.Xpf.Controls.WebView` NuGet 包提供两个控件：

- **NativeWebView**：可嵌入的网页控件，内联渲染在你的窗口里。支持 Windows 和 macOS。
- **NativeWebDialog**：一个独立的浏览器对话框窗口。所有平台（含 Linux）均支持。

这两个控件的 Avalonia 文档请见[嵌入网页内容](/docs/app-development/embedding-web-content)。

### Linux 上的要求 {#linux-requirements}

Linux 上的 `NativeWebDialog` 需要 webkit2gtk 4.1 版：

**Debian / Ubuntu:**
```bash
sudo apt install libwebkit2gtk-4.1-dev
```

**Fedora:**
```bash
sudo dnf install webkit2gtk4.1-devel
```

**RHEL / CentOS:**
```bash
sudo dnf install webkit2gtk4.1-devel
```

:::note
必须是 webkit2gtk 4.1 版。更老的版本（4.0）支持不了 `NativeWebDialog` 所需的全部功能。
:::

## CefSharp

`CefSharp.Wpf.NetCore` 在 XPF 中只支持 Windows。它自带 Windows 原生的 Chromium 二进制文件，在 Linux 和 macOS 上用不了。

若 CefSharp 针对 `CursorInteropHelper.Create()` 抛出 `NotImplementedException`，请升级到 XPF 1.6.0 或更高版本，那里提供了回退方案。老版本上的变通办法是：从 `ChromiumWebBrowser` 派生并重写 `OnCursorChange`，把 CefSharp 的光标类型映射到 WPF 的 `Cursors`。

## DotNetBrowser

TeamDev 的 DotNetBrowser 在 XPF 的所有平台上都受支持。配置方法可参考 [XpfDotNetBrowserApp 示例](https://github.com/AvaloniaUI/Avalonia-XPF-Samples/tree/master/src/XpfDotNetBrowserApp)。

## 怎么挑网页控件 {#choosing-a-web-control}

- **只部署到 Windows**：CefSharp 的 Chromium 集成最完整，键盘、样式和 DevTools 支持一应俱全。
- **Windows + macOS**：窗口内嵌入用 `NativeWebView`，想要基于 Chromium 的方案则用 DotNetBrowser。
- **所有平台（含 Linux）**：若对话框式的方案可以接受，用 `NativeWebDialog`；若要窗口内嵌入，用 DotNetBrowser。
