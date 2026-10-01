---
id: ui-composition
title: 界面组合
description: 用窗口、内置控件、用户控件和自定义控件组合出完整布局。
doc-type: explanation
video:
  src: https://youtu.be/meSx__KuuSc
  title: 详解 Avalonia 界面组合 —— 控件类型、控件树与布局层次
---

import CompositionBasicLayoutDiagram from '/img/concepts/core-concepts/ui-composition/composition-basic-layout.png';
import CompositionTreesDiagram from '/img/concepts/core-concepts/ui-composition/composition-trees.png';
import CompositionUserControlsDiagram from '/img/concepts/core-concepts/ui-composition/composition-usercontrol.png';
import CompositionCollectionControlsDiagram from '/img/concepts/core-concepts/ui-composition/composition-collection-controls.png';

界面组合，就是搭建应用所需布局的过程：把若干组件编排起来，构建出复杂的视图。好处在于：

* _封装_ —— 把每个组件的 XAML 和代码限定在它自己需要的范围内，从而降低复杂度，代码也更好懂、更好维护。
* _复用_ —— 让应用中反复出现的部件在外观和行为上保持一致。

Avalonia 支持界面组合，你可以借此搭建出应用所需的各种布局与功能。

用 Avalonia 构建应用时，有好几类组件可供选择：

* Windows
* 内置控件
* User Controls
* Custom Controls
* Template Controls

## 窗口与内置控件 {#windows-and-built-in-controls}

在 Avalonia 中，窗口是布局的基本单元（就带窗口系统的平台而言）。

Avalonia 内置了大量控件，足以覆盖你绝大多数界面需求。   

<Image light={CompositionBasicLayoutDiagram} alt="Diagram showing a single control and a multi-control layout inside a window" position="center" maxWidth={400} cornerRadius="true"/>

初识 Avalonia 时，你可能会在窗口的内容区里放上单个内置控件（上图左）。这是界面组合最简单的形态：窗口带着应用标题，通常还有若干窗口状态按钮（视目标平台而定），而那个内置控件让应用得以接收用户输入，或是带着布局和样式呈现输出。

稍复杂一点的应用，可能需要在窗口内容区里用一个内置的布局控件，来安排多个其他内置控件（上图右）。

:::info
Avalonia 内置控件的完整清单，请见[控件参考](/controls)。
:::

## 逻辑树与视觉树 {#logical-and-visual-trees}

无论你怎样编排控件，Avalonia 都会把它们之间的关系表示成一棵树，最「外层」的控件就是根。比方说，前面那个界面组合可以表示成这样一棵树：

<Image light={CompositionTreesDiagram} alt="Diagram showing the logical control tree for a window with nested controls" position="center" maxWidth={400} cornerRadius="true"/>

这就是**逻辑控件树**，它按 XAML 中定义的层次关系来表示应用的各个控件（含主窗口）。Avalonia 中有许多机制都要处理逻辑控件树，以及与之相伴的**视觉控件树**。

:::info
关于控件树这一概念的更多说明，请见[控件树](/docs/custom-controls/control-trees)。
:::

## 用户控件 {#user-controls}

用户控件是 Avalonia 界面组合的主力。

<Image light={CompositionUserControlsDiagram} alt="Diagram showing user controls used as page views and reusable components" position="center" maxWidth={400} cornerRadius="true"/>

你可以把一个用户控件放进主窗口的内容区，让它充当「页面视图」（上图左）。这样就能做出多页面的复杂应用 —— 每个页面的布局和功能都待在各自的用户控件（XAML 与代码）文件里。   

用户控件的另一种用法是作为组件控件（上图右）。你一开始这么做也许只是为了给窗口或页面视图减负；但之后（或许过些时候）往往还会在别的页面上复用这个组件。

## Tutorial

:::info
关于 `DataTemplates` 的教程，请见 [Avalonia.Samples](https://github.com/AvaloniaUI/Avalonia.Samples/tree/main?tab=readme-ov-file#%EF%B8%8F-datatemplate-samples)。  
:::

## 集合类控件 {#collection-controls}

界面组合还有一种形态：你需要展示一组条目。

<Image light={CompositionCollectionControlsDiagram} alt="Diagram showing a collection control with a data template rendering items" position="center" maxWidth={400} cornerRadius="true"/>

这种场景要用到某个内置的重复型控件，把它绑定到集合上，再配一个数据模板来呈现集合中的每一项。

:::info
关于数据模板和集合类控件，请见 [DataTemplate 示例](https://github.com/AvaloniaUI/Avalonia.Samples/tree/main?tab=readme-ov-file#%EF%B8%8F-datatemplate-samples)。
:::

## 自定义控件 {#custom-controls}

万一哪天 Avalonia 的内置控件实在满足不了你的界面需求（这种情况并不多见），你也可以从零「手搓」一个自定义控件。这样你能自行定义属性、事件和方法，但代价是控件的绘制也得从头实现。

:::info
自定义控件的实现方法，请见[自定义控件](/docs/custom-controls)。
:::

## 模板化控件 {#templated-controls}

模板化控件借助 Avalonia 的**样式**系统，创建出一个外观由控件模板决定的可复用控件。你可以借此改变控件的视觉结构，而不触及它的行为。

:::info
关于 Avalonia **样式**系统背后的理念，请见[样式](/docs/styling/styles)。
:::

## 另请参阅 {#see-also}

- [Avalonia XAML](/docs/fundamentals/avalonia-xaml)
- [Code-behind](/docs/fundamentals/code-behind)
- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)
- [控件参考](/controls)
