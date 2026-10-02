---
id: layout
title: 布局
description: Avalonia 布局系统如何借助面板和边界框来测量、排列控件。
doc-type: explanation
---

import LayoutZonesDiagram from '/img/concepts/ui-concepts/layout/layout-zones.png';

Avalonia 布局系统通过「测量 + 排列」两个阶段来确定控件的位置和尺寸。本文讲解这套机制的工作方式、可用的面板类型，以及边界框模型。

## Panels

Avalonia 中有一组派生自 `Panel` 的元素，这些 `Panel` 元素可以实现许多复杂布局。比如堆叠元素用 `StackPanel` 轻而易举，而更复杂、更自由的布局则可以借助 [`Canvas`](/api/avalonia/controls/canvas) 来完成。

下表汇总了可用的 `Panel` 控件：

| 名称            | 说明                                                                                                                                                                                                                                                               |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Panel`         | 把所有子元素铺开，填满 `Panel` 的范围                                                                                                                                                                                                                   |
| `Canvas`        | 划定一块区域，在其中按相对于 Canvas 区域的坐标显式摆放子元素。                                                                                                                                                       |
| `DockPanel`     | 划定一块区域，在其中让子元素横向或纵向相对排布。                                                                                                                                                    |
| [`Grid`](/api/avalonia/controls/grid)          | 定义一块由行与列组成的弹性网格区域。                                                                                                                                                                                                           |
| `RelativePanel` | 把子元素相对于其他元素或面板自身来排布。                                                                                                                                                                                                   |
| `StackPanel`    | 把子元素排成一行，可以是横向，也可以是纵向。                                                                                                                                                                               |
| `WrapPanel`     | 把子元素从左到右依次摆放，到达容器边缘时换到下一行。后续的排列顺序是自上而下还是从右到左，取决于 Orientation 属性的取值。 |

在 WPF 中 `Panel` 是抽象类，要让多个控件铺满可用空间，通常得用一个不设行列的 `Grid`。而在 Avalonia 中 `Panel` 是可以直接使用的控件，布局行为和不设行列的 `Grid` 一致，但运行时开销更小。

## 元素的边界框 {#element-bounding-boxes}

思考 Avalonia 布局时，弄明白包裹每个元素的那个边界框很重要。布局系统处理的每个 `Control`，都可以看作嵌进布局里的一个矩形；`Bounds` 属性返回的就是元素所分到的那块布局区域的边界。矩形的大小由这些因素共同决定：可用的屏幕空间、各种约束的尺寸、布局相关的属性（如外边距和内边距），以及父级 `Panel` 元素自身的行为。把这些数据算完，布局系统就能确定某个 `Panel` 下所有子元素的位置。要记住，父元素上定义的尺寸特性（比如 `Border`）会影响到它的子元素。

## 布局系统 {#the-layout-system}

往简单里说，布局就是一套递归机制，最终把元素的尺寸、位置定下来并画出去。说得更具体些，布局描述的是测量并排列某个 `Panel` 元素 `Children` 集合中各成员的过程。布局是个重活：`Children` 集合越大，要做的计算就越多。拥有该集合的 `Panel` 元素所定义的布局行为，也会带来额外的复杂度。相对简单的 `Panel`（如 `Canvas`），性能可以明显优于更复杂的 `Panel`（如 `Grid`）。

子控件每改变一次位置，都有可能触发布局系统再跑一轮。因此，弄清哪些事件会唤起布局系统很重要 —— 不必要的触发会拖垮应用性能。下面描述布局系统被唤起时所发生的流程。

1. 子 `Control` 的布局流程从测量它的核心属性开始。
2. 求值 `Control` 上定义的尺寸属性，如 `Width`、`Height` 和 `Margin`。
3. 套用 `Panel` 特有的逻辑，比如 `Dock` 的方向，或是 `Orientation` 的堆叠方式。
4. 所有子元素测量完毕后，开始排列内容。
5. 把 `Children` 集合绘制到屏幕上。
6. 若集合中又添了新的 `Children`，整个流程会再跑一遍

下面几节会更详细地说明这个流程，以及它是如何被唤起的。

## 测量与排列子元素 {#measuring-and-arranging-children}

布局系统会为 `Children` 集合中的每个成员跑两趟：测量阶段和排列阶段。每个子 `Panel` 都提供自己的 `MeasureOverride` 和 `ArrangeOverride` 方法，以实现各自特有的布局行为。

测量阶段会对 `Children` 集合中的每个成员求值，流程始于对 `Measure` 方法的调用。该方法由父级 `Panel` 元素在其内部实现中调用，布局要发生并不需要你显式调用它。

首先求值 `Visual` 的原生尺寸属性，如 `Clip` 和 `IsVisible`。若 `IsVisible` 为 `false`，该控件会被完全排除在布局之外：布局系统把它的 `DesiredSize` 设为零并跳过它的整棵子树，渲染器自然也就不会绘制它。关于把 `IsVisible` 和 `Opacity` 作为隐藏手段的对比，请见 [IsVisible 与 Opacity 的取舍](/docs/graphics-animation/effects#isvisible-vs-opacity)。这些原生属性求值之后，会生成一个约束，传给 `MeasureCore`。

接着处理那些会影响约束取值的框架属性。它们通常描述底层 `Control` 的尺寸特性，比如 `Height`、`Width` 和 `Margin` —— 每一个都可能改变显示该元素所需的空间。随后以这个约束为参数调用 `MeasureOverride`。

由于 `Bounds` 是算出来的值，要留意：布局系统的各种操作可能导致它被多次、或者增量式地更新。布局系统可能正在计算子元素所需的测量空间、父元素施加的约束，等等。

测量阶段的最终目的，是让子元素在 `MeasureCore` 调用过程中确定自己的 `DesiredSize`。这个 `DesiredSize` 值由 `Measure` 保存下来，供内容排列阶段使用。

排列阶段始于对 `Arrange` 方法的调用。在这一阶段，父级 `Panel` 元素生成一个代表子元素边界的矩形，并把它传给 `ArrangeCore` 方法去处理。

`ArrangeCore` 方法会求值子元素的 `DesiredSize`，并把可能影响最终渲染尺寸的各项外边距一并算进去。`ArrangeCore` 生成一个排列尺寸，作为参数传给 `Panel` 的 `ArrangeOverride` 方法；`ArrangeOverride` 则生成子元素的 finalSize。最后，`ArrangeCore` 方法对外边距、对齐方式等偏移属性做最终求值，把子元素摆进它的布局槽位。子元素不一定要填满分到的全部空间（通常也确实不会）。随后控制权交回父级 `Panel`，布局流程至此结束。

## 布局区域 {#layout-zones}

<Image light={LayoutZonesDiagram} maxWidth="400" alignment="center" alt="A diagram with four overlapping rectangles, representing the layout zones of a UI window." />

## 覆盖层 {#overlay-layers}

除了常规布局系统之外，Avalonia 还提供了覆盖层 —— 它们渲染在窗口内常规控件内容之上。当你需要把某些内容显示在一切之上时（比如加载指示器、浮动工具栏或通知面板），它们就派上用场了。

用 `OverlayLayer.GetOverlayLayer(visual)` 获取给定视觉元素所对应的覆盖面。加进 `OverlayLayer` 的内容会显示在所有常规控件之上，但位于弹出窗口、菜单和工具提示之下。

细节与代码示例请见[覆盖层](/docs/fundamentals/visual-and-logical-trees#overlay-layers)。

## 另请参阅 {#see-also}

- [控件定位](/docs/layout/positioning-controls)：对齐、外边距与定位。
- [响应式布局](/docs/layout/responsive-layouts)：用容器查询和自动重排的面板，让布局适应不同尺寸。
- [覆盖层](/docs/fundamentals/visual-and-logical-trees#overlay-layers)：在常规控件之上添加自定义覆盖内容。
