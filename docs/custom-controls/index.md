---
id: index
title: 创建自定义控件
sidebar_position: 1
description: 在 Avalonia 中编写自定义控件的几种思路概览。
doc-type: overview
---

## 自定义控件 {#custom-controls}

除了[内置控件库](/controls)提供的控件，Avalonia 还允许你创建自己的控件：定义专属的属性、事件和[伪类](/docs/styling/pseudoclasses)，甚至可以重写视觉渲染，画出完全独一无二的控件。

## 自定义控件的类型 {#types-of-custom-controls}

动手之前，先挑一类最契合你需求的控件。Avalonia 中主要有三类控件：

1. [用户控件](#user-controls)
2. [模板化控件](#templated-controls)
3. [自绘控件](#custom-drawn-controls)

除了这三类，你还可以派生[内容控件、带标题的内容控件或项控件](#other-customizable-controls)来做自定义控件。

### 用户控件 {#user-controls}

用户控件的写法和你自定义 `Window` 时别无二致：从模板新建一个 `UserControl`，再往里添控件。`UserControl` 就像一个容器，把多个现有控件组合成一个浑然一体的元素。

这类控件最适合做应用专属的可复用「视图」或「页面」，比如用户资料视图；不太适合做通用的 UI 元素。

创建自定义用户控件的步骤：

1. **写 XAML。**在 XAML 中新建一个 `UserControl`，通过摆放现有控件、设置属性和套用样式，定下这个自定义控件的布局和外观。
2. **加代码隐藏。**视需要编写代码隐藏逻辑，用来处理事件、调整行为或添加样式化属性。

更详细的指引记录在 [UserControl 参考](/controls/primitives/usercontrol)中。

一个自定义 `UserControl` 的示例[可以从 GitHub 克隆下来](https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/CustomControl)。

### 模板化控件 {#templated-controls}

模板化控件是无外观的，也就是说控件的行为逻辑与外观相互分离。于是同一个模板化控件可以为不同主题或不同应用重新设样式。`TemplatedControl` 的行为和属性在代码中定义，视觉呈现则在 XAML 中以 `ControlTheme` 的形式设计。

这类控件最适合做那种想在多个应用间共享的通用 UI 元素。[Avalonia 的标准控件](/controls)大多都是模板化控件。

:::info
在 Avalonia 中，自定义模板化控件继承自 `TemplatedControl`。这一点与 WPF 或 UWP 不同——在那边你继承的是 `Control` 类。
:::

创建自定义模板化控件的步骤：

1. **定义控件类。**新建一个派生自 `TemplatedControl` 的类，定下这个自定义控件的行为、属性和事件。
2. **添加控件模板。**创建一个[控件主题](/docs/styling/control-themes) XAML 文件，定下控件的视觉外观。
3. **继续打磨样式。**如有需要，可进一步调整控件模板或套用额外样式来细化外观。

更详细的指引记录在[模板化控件](/docs/custom-controls/templated-controls)中。

### 自绘控件 {#custom-drawn-controls}

自绘控件通过重写 `Visual.Render` 方法，用几何图形把自己画出来。借助 `DrawingContext` API，你可以精确指定控件的外观。[Avalonia 内置控件](/controls)中就有一些是这么画的，比如 `TextBlock` 和 `Image`。

这种办法让你对控件视觉呈现的每一个细节都了如指掌。那些不需要换主题的非交互式图形元素，适合做成自绘控件。

:::info
在 Avalonia 中，自绘控件继承自 `Control`。这一点与 WPF 或 UWP 不同——在那边你继承的是 `FrameworkElement` 类。
:::

创建自绘控件的步骤：

1. **定义控件类。**新建一个派生自 `Control` 的类，定下控件的行为和渲染方式。
2. **重写 `Render` 方法。**在控件类中重写 `Render` 方法，用 `DrawingContext` 把控件画出来。

更详细的指引记录在[自绘控件](/docs/custom-controls/custom-drawn-controls)中。

### 其他可定制的控件 {#other-customizable-controls}

除了上面这三条路，你还可以派生下列类型来做自定义控件类：

- `ContentControl`，承载单块内容的控件。
- `HeaderedContentControl`，带标题区和内容区的控件。
- `ItemsControl`，显示一组项的控件。

这些控件都派生自 `Control`，因此 `Width`、`Height`、`Margin`、`DataContext` 等属性默认就能用。

## 另请参阅 {#see-also}

- [用户控件](/controls/primitives/usercontrol)：用 XAML 加代码隐藏，把现有控件组合成可复用的视图。
- [自定义模板化控件](/docs/custom-controls/templated-controls)：编写外观完全交由控件主题决定的无外观控件。
- [自绘控件](/docs/custom-controls/custom-drawn-controls)：通过重写 `Render` 让控件自己画自己。
- [定义属性](/docs/custom-controls/defining-properties)：为自定义控件添加样式化属性、直接属性和附加属性。
- [定义事件](/docs/custom-controls/defining-events)：给自定义控件添加路由事件。
- [自定义控件库](/docs/custom-controls/custom-control-library)：把自定义控件打进类库，再从别的项目引用。