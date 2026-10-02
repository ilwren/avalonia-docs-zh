---
id: app-performance-issues
title: 应用性能问题
---

你的应用跑得太慢？只要在开发过程中留心几个要点，Avalonia 应用的性能往往能有不小的提升。本文就来说说可以从哪些地方着手优化。

## Use CompiledBindings

在 Avalonia 中提升性能最立竿见影的办法之一，就是在应用里用 [`CompiledBindings`](/docs/data-binding/compiled-bindings)。编译绑定在编译期就把绑定路径解析好，省去了运行时反射的开销，数据绑定自然更快。 

## 按数据展示需求挑对控件 {#choose-the-right-control-for-data-display}

当你需要在 `DataGrid` 中展示大量数据，或者 `TreeView` 里节点众多时，推荐用 `TreeDataGrid` 控件。`TreeDataGrid` 是从零写起的，性能比普通的 `DataGrid` 更好。它支持虚拟化，还带有层级数据模板，若你需要一棵虚拟化的树，它尤其合用。

若用不上编辑功能，就别用 `DataGrid` 控件——论性能，它一向算不上优选。

:::caution
自 2025 年 10 月起，[`TreeDataGrid`](/controls/data-display/structured-data/treedatagrid) 作为 Avalonia Pro 的一部分维护。面对大数据集，它目前仍是推荐选择。
:::

## Virtualization

处理大量数据时，启用虚拟化能让 Avalonia 应用跑得更快。所谓虚拟化，就是只渲染控件中可见的那些项；当要显示的项数庞大时，性能提升相当可观。

### TreeDataGrid

`TreeDataGrid` 支持虚拟化，哪怕成千上万行、单元格还挺复杂，也应付得来。

:::caution
自 2025 年 10 月起，[`TreeDataGrid`](/controls/data-display/structured-data/treedatagrid) 作为 Avalonia Pro 的一部分维护。面对大数据集，它目前仍是推荐选择。
:::

## 精简视觉树结构 {#optimize-your-visual-tree-structure}

嵌套过深、结构复杂的布局常常是性能的绊脚石。尽量把 XAML 标记写得简单、扁平些。每把一个 UI 元素渲染到屏幕上，都要为它跑两趟“布局过程”（先测量，后排列）。

这个布局过程相当吃算力：一个元素的子级越多，要算的账就越多。所以在 Avalonia 中把视觉树的复杂度压下来，往往能显著改善应用性能。

## 少用 Run 来设置文本属性 {#minimize-use-of-run-for-setting-text-properties}

建议尽量少在 TextBlock 里使用 Run，它会带来更吃资源的操作。若你只是用 Run 来设定文本属性，不妨把那些属性直接设在 TextBlock 上，这么做有助于提升应用性能。

## 用 StreamGeometry 而非 PathGeometry {#use-streamgeometries-over-pathgeometries}

在 Avalonia 中处理几何图形时，`StreamGeometry` 比 `PathGeometry` 更高效。`StreamGeometry` 专为应付大量 `PathGeometry` 对象而优化，占内存更少、性能更佳。因此在两者可选时，推荐用 `StreamGeometry` 而非 `PathGeometry`，应用性能会更好看。

## 改用尺寸更小的图片 {#use-reduced-image-sizes}

当应用只需显示小图或缩略图时，不妨另外生成一份小尺寸图片来用。Avalonia 默认会按原始尺寸加载并解码图片；若你加载的是大图，却在 `ItemsControl` 这类控件里缩成缩略图显示，性能很可能因此吃紧。

## 把绑定错误都解决掉 {#resolve-your-binding-errors}

绑定错误是 Avalonia 应用中常见的性能杀手。每出现一次绑定错误，应用都要尝试解析该绑定并把错误写进跟踪日志，性能随之一沉。绑定错误越多，拖累自然越重。 

绑定错误的一大来源是在 `DataTemplates` 中使用 `RelativeSource` 绑定——在 `DataTemplate` 初始化完成之前，这类绑定通常解析不出正确结果。建议干脆别用 `RelativeSource.FindAncestor`。更高效的做法是定义一个附加属性，借助属性继承把值沿视觉树往下推，而不是反过来去视觉树里查找。

## 异步加载数据 {#asynchronously-load-data}

性能问题、界面卡死、应用无响应，往往都出在数据加载的方式上。别让 UI 线程不堪重负——务必让数据异步加载。





























