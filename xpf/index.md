---
id: index
title: Avalonia XPF
sidebar_label: Avalonia XPF
---

<head>
  <title>Avalonia 文档：XPF</title>
  <meta
    name="description"
    content="Avalonia XPF runs your existing WPF applications on macOS, Linux, iOS, Android, and WebAssembly with minimal code changes."
  />
</head>

import TierBadge from '@site/src/components/global/TierBadge';

你的 WPF 应用是多年打磨出来的。它运转良好，团队对这份代码了如指掌，客户也离不开它。而现在，有人要你支持 macOS，或者 Linux，又或者 Web。

彻底重写可不是几个迭代的事，少说几个月，常常得耗上几年。每一个界面、每一处边界情况、每一个团队早已忘到脑后的变通办法，都得重新挖出来再实现一遍。若你的应用还依赖 DevExpress、Telerik、Syncfusion 这类第三方控件套件，代价还要翻几番：这些集成搬不过去，换掉它们意味着重新评估厂商、重新学 API，还得眼睁睁看着已经交付的功能缩水。与此同时，团队被两份做着同一件事的代码撕成两半——每个功能做两遍，每个修复也做两遍。拖得越久，真正重要的产品工作就落下得越多。

Avalonia XPF 是另一条路。它把 WPF 底下的渲染层换成 Avalonia 的跨平台引擎，同时保住你的代码所依赖的 API 与二进制兼容性。你的 XAML、你的视图模型、来自 Telerik、DevExpress、Infragistics、Actipro、Syncfusion 等厂商的第三方控件，统统照常工作。你不是在重写应用，你只是把它搬到了新地方跑。

## 运作原理 {#how-it-works}

XPF 把 WPF 的底层渲染组件（MilCore）换成了 Avalonia 的渲染引擎，这一层之上的一切原封不动。你的应用看到的还是那套熟悉的 WPF API，只不过这些 API 如今在 macOS、Linux 乃至更多平台上都管用了。

这意味着：

- **多数应用一行代码都不用改。**今天它能对着 WPF 编译通过，那么对着 XPF 多半也能。
- **第三方控件照常可用。**XPF 保持二进制兼容，主流厂商的控件不加改动就能跑。
- **你只维护一份代码。**不分叉、不另写一套、各平台也不会渐行渐远。

## Hybrid XPF

XPF 并非要你一步到位。借助 [Hybrid XPF](/xpf/interop/using-xpf-in-avalonia)，你可以在同一个应用里混用 Avalonia 控件和 WPF 控件。也就是说，你可以先用 XPF 把跨平台拿下，再按自己的节奏逐步把 WPF 视图换成原生的 Avalonia 视图。久而久之，XPF 便成了通往完整 Avalonia 迁移的垫脚石——不必来一场大爆炸式的重写，应用也从不会有停摆的时候。

反过来也成立。若你本就在用 Avalonia 开发，Hybrid XPF 让你直接用上 Telerik、DevExpress、Infragistics、Actipro、Syncfusion 等厂商的 700 多个现成 WPF 控件，不必苦等原生 Avalonia 版本。

## 平台支持 {#platform-support}

| 平台 | Internal | Business | Enterprise |
|---|---|---|---|
| [Windows](/docs/supported-platforms#windows) | <TierBadge tier={1} /> | <TierBadge tier={1} /> | <TierBadge tier={1} /> <TierBadge tier={2} /> <TierBadge tier={3} /> |
| [macOS](/docs/supported-platforms#macos) | <TierBadge tier={1} /> | <TierBadge tier={1} /> | <TierBadge tier={1} /> <TierBadge tier={2} /> <TierBadge tier={3} /> |
| [Desktop Linux](/docs/supported-platforms#desktop-linux) | <TierBadge tier={1} /> | <TierBadge tier={1} /> | <TierBadge tier={1} /> <TierBadge tier={2} /> <TierBadge tier={3} /> |
| [Embedded Linux](/docs/supported-platforms#embedded-linux) | | 付费附加项 | <TierBadge tier={1} /> <TierBadge tier={2} /> <TierBadge tier={3} /> |
| [iOS](/xpf/platforms/mobile-and-browser) | | | <TierBadge tier={1} /> <TierBadge tier={2} /> <TierBadge tier={3} /> |
| [Android](/xpf/platforms/mobile-and-browser) | | | <TierBadge tier={1} /> <TierBadge tier={2} /> <TierBadge tier={3} /> |
| [WebAssembly](/xpf/platforms/mobile-and-browser) | | | <TierBadge tier={1} /> |

所有档位都支持 Avalonia 的[一级平台](/docs/supported-platforms)。Enterprise 许可证包含二级平台支持，三级平台可按具体情况另行安排。

## Licensing

XPF 是商业产品，分 **Internal**、**Business** 和 **Enterprise** 三档。所有许可证都是永久的——无论许可证状态如何，你的应用都能继续运行。

| | Internal | Business | Enterprise |
|---|---|---|---|
| macOS, Desktop Linux | Yes | Yes | Yes |
| 与 Avalonia 控件混搭 | | Yes | Yes |
| Cross-platform System.Drawing | | Yes | Yes |
| Embedded Linux | | 付费附加项 | Yes |
| iOS, Android, WebAssembly | | | Yes |
| SLA | 10 个工作日 | 5 个工作日 | 3 个工作日 |

每份许可证都包含：

- 全功能的 **30 天免费试用**
- 一份用 XPF 开发的永久许可
- 12 个月的更新与工程支持

Enterprise 试用请联系销售。价格详见 [Avalonia 官网](https://avaloniaui.net/xpf?av_source=docs&av_medium=doc_link&av_content=xpf-index#pricing)。

## 开始上手 {#get-started}

[快速上手指南](/xpf/getting-started)会带你把 WPF 应用跑到新平台上。多数团队几分钟就能跑通，而不是几个月。
