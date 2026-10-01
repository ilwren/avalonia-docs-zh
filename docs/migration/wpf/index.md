---
id: index
title: 从 WPF 迁移
description: 把 WPF 应用迁移到 Avalonia，控件、绑定和 MVVM 套路都有对应物。
doc-type: migration
---

Avalonia 与 WPF 共享许多概念，你现有的知识可以直接迁移过来。多数控件、布局面板、数据绑定和 MVVM 套路要么用法一致，要么有明确的对应物。两个框架分道扬镳的地方，主要在样式、数据模板、属性系统和事件命名上。

:::tip[已经有一大摊 WPF 代码了？]
如果你的目标只是让现有的 WPF 应用跑在 macOS、Linux 或 Web 上，未必非得全盘重写。[XPF](/xpf) 能让 WPF 应用以极少的代码改动跨平台运行，于是你既能进军新平台，又能留着手上这套代码库。
:::

## 主要差异 {#key-differences}

**样式**是观念上最大的转变。Avalonia 用一套带选择器、样式类和伪类的类 CSS 体系，取代了 WPF 的资源字典样式和触发器。完整讲解请见[样式](/docs/styling/styles)。

**数据模板**用法相近，只是放在 `DataTemplates` 集合里而非资源中，并且支持按接口和派生类型匹配。请见[数据模板](/docs/data-templates/introduction-to-data-templates)。

**属性系统**用的是强类型泛型（`StyledProperty`、`DirectProperty`、`AttachedProperty`），而不是单一的 `DependencyProperty` 类。请见[属性](/docs/properties)。

**事件**沿用同样的路由事件模型，但名字以 pointer 为准（用 `PointerPressed` 而非 `MouseLeftButtonDown`），隧道也靠路由策略标志来处理，而非另设 `Preview*` 事件。请见[事件](/docs/events)。

**控件**大体相同，个别换了名字或需要单独的 NuGet 包。请见[控件](controls)。

**布局**面板（`Grid`、`StackPanel`、`DockPanel` 等）都一样，只是多了点小东西，比如 `StackPanel` 上的 `Spacing` 和 `ColumnDefinitions` 简写语法。请见[布局](/docs/layout)。

## 从哪儿入手 {#where-to-start}

若你想要一份快速对照，请从**[速查表](/docs/migration/wpf/cheat-sheet)**开始。它用紧凑的表格覆盖了 XAML 命名空间、属性系统、样式、数据绑定、控件、事件、命令、模板、线程、动画、图形和文件结构。

想深入了解某个主题，请看上面链接的各篇指南。

## 另请参阅 {#see-also}

- [WPF 到 Avalonia 速查表](/docs/migration/wpf/cheat-sheet)：快速的左右对照参考。
- [样式](/docs/styling/styles)：类 CSS 样式系统的迁移指南。
- [控件](controls)：控件名称对照。
- [属性](/docs/properties)：属性系统的差异。