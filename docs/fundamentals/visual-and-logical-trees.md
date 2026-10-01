---
id: visual-and-logical-trees
title: 视觉树与逻辑树
description: 理解用于布局、渲染和事件的两套树形结构：逻辑树与视觉树。
doc-type: explanation
video:
  src: https://youtu.be/1cY3LKDBCz8
  title: Avalonia 视觉树与逻辑树 —— DataContext 继承、样式与树的遍历
---

Avalonia 把控件组织成两棵并行的树：逻辑树和视觉树。资源查找、事件路由、样式以及自定义控件开发，都离不开对这两棵树的理解。

想查看应用的逻辑树和视觉树，可以使用 Avalonia 开发者工具的 [Elements 工具](/tools/developer-tools/elements-tool)。

## 逻辑树 {#logical-tree}

逻辑树表示的是你在 XAML 中定义的界面层次结构。它只包含你显式声明的控件，不含模板内部的结构。

逻辑树用于：
- **资源查找：** `StaticResource` 和 `DynamicResource` 沿逻辑树向上查找。
- **数据上下文继承：** `DataContext` 沿逻辑树向下传播。
- **属性继承：** `FontSize`、`Foreground`、`FlowDirection` 这类可继承属性沿逻辑树向下流动。
- **具名元素查找：** `x:Name` 引用在逻辑树的作用域内解析。

举例来说，下面这段 XAML —— 一个 [`Window`](/controls/primitives/window) 里套一个 [`StackPanel`](/controls/layout/panels/stackpanel)，其中放了三个控件 —— 对应的逻辑树如图所示。

<Tabs>
<TabItem value="xaml" label="XAML">

```xml
<Window>
    <StackPanel>
        <TextBlock Text="Name:" />
        <TextBox Text="{Binding Name}" />
        <Button Content="Save" />
    </StackPanel>
</Window>
```

</TabItem>

<TabItem value="logical-tree" label="Logical tree">

```text
Window
  └─ StackPanel
       ├─ TextBlock
       ├─ TextBox
       └─ Button
```

</TabItem>
</Tabs>

### 遍历逻辑树 {#navigating-the-logical-tree}

```csharp
// Get the logical parent
var parent = myControl.GetLogicalParent();

// Get logical children
var children = myControl.GetLogicalChildren();

// Find an ancestor of a specific type
var window = myControl.FindLogicalAncestorOfType<Window>();

// Get all logical descendants
var allTextBlocks = myPanel.GetLogicalDescendants().OfType<TextBlock>();
```

### 改动逻辑树 {#mutating-the-logical-tree}

只有当框架没有正在遍历这棵树时，增删 `LogicalChildren` 才是安全的。好几种常见操作都会引发这类遍历，最典型的就是 `DataContext` 等可继承属性的传播。在遍历进行期间改动 `LogicalChildren`，可能破坏迭代过程，表现出来就是各种绑定错误。

**可以安全增删逻辑子元素的时机：**

- 控件的构造函数中 —— 此时它还没挂到任何树上。
- `OnApplyTemplate` 中，且在调用 `base.OnApplyTemplate(e)` 之后。
- 路由输入或命令的处理程序中（例如 `Click` 或 `Tapped` 的处理程序）。
- `Loaded` 事件的处理程序中。

**不要在以下场合改动逻辑子元素：**

- `OnPropertyChanged` 或 `PropertyChanged` 回调中 —— 框架可能正把某个可继承属性传播给你即将改动的那些子元素，而且传播还没走完。
- `DataContextChanged` 中，原因同上。

## 视觉树 {#visual-tree}

视觉树表示 Avalonia 实际在跑的全部内容，也就是所有参与渲染的视觉元素，既包括控件上设置的属性，也包括控件模板内部的各个部件。

视觉树用于：
- **渲染：** 渲染器遍历视觉树来绘制界面。
- **命中测试：** 指针事件靠视觉树判断光标下面是哪个元素。
- **布局：** 测量与排列两个阶段都遍历视觉树。
- **事件路由：** 路由事件沿视觉树向下隧道传播、或向上冒泡。

举例来说，逻辑树中一个孤零零的 `Button`，到了视觉树里会展开成 `ContentPresenter`、`Border` 以及其他模板元素。[前面例子](#logical-tree)中的那个 `Button`，其视觉树可能长这样：

```text title="Visual tree"
Button
  └─ ContentPresenter
       └─ Border
            └─ ContentPresenter
                 └─ TextBlock ("Save")
```

### 遍历视觉树 {#navigating-the-visual-tree}

```csharp
// Get the visual parent
var parent = myControl.GetVisualParent();

// Get visual children
var childCount = myControl.VisualChildren.Count;
var firstChild = myControl.VisualChildren[0];

// Find a visual ancestor
var scrollViewer = myControl.FindAncestorOfType<ScrollViewer>(includeSelf: false);

// Find a visual ancestor matching a predicate
var enabledPanel = myControl.FindAncestorOfType<StackPanel>(
    includeSelf: false,
    predicate: panel => panel.IsEnabled);

// Find a visual descendant matching a predicate
var visibleTextBox = myPanel.FindDescendantOfType<TextBox>(
    includeSelf: false,
    predicate: tb => tb.IsVisible);

// Get all visual descendants
var allVisuals = myControl.GetVisualDescendants();
```

## 两棵树的区别 {#differences-between-the-trees}

| &nbsp; | 逻辑树 | 视觉树 |
|---|---|---|
| Contains | 你在 XAML 中声明的控件 | 全部视觉元素，含模板内部结构 |
| 资源查找 | Yes | No |
| 数据上下文继承 | Yes | No |
| 属性继承 | Yes | No |
| 模板展开 | 否（模板只算单个节点） | 是（模板展开为各个部件） |
| 事件路由 | No | 是（隧道与冒泡） |
| Rendering | No | Yes |
| 命中测试 | No | Yes |
| Layout | Partially | Yes |

## 该用哪棵树 {#when-to-use-which-tree}

**以下情形用逻辑树：**
- 查找资源或数据上下文
- 查找具名元素
- 从某个控件向上找它的逻辑父级
- 处理 `ItemsControl` 的子项（这些项位于逻辑树中）

**以下情形用视觉树：**
- 查找控件内部的模板部件
- 遍历已渲染的元素层次
- 实现命中测试
- 在元素之间换算坐标（`TranslatePoint`）

## 在运行时查看这两棵树 {#examining-trees-at-runtime}

用 Avalonia DevTools（调试版中按 F12）可以交互式地查看两棵树。DevTools 的 Logical Tree 和 Visual Tree 标签页会连同属性一起展示完整层次。

```csharp
// Print the logical tree for debugging
static void PrintLogicalTree(StyledElement element, int indent = 0)
{
    Debug.WriteLine($"{new string(' ', indent * 2)}{element.GetType().Name}");
    if (element is ILogical logical)
    {
        foreach (var child in logical.LogicalChildren)
        {
            if (child is StyledElement styledChild)
                PrintLogicalTree(styledChild, indent + 1);
        }
    }
}
```

## 模板部件与视觉树 {#template-parts-and-the-visual-tree}

你创建控件模板时，模板内部的元素会进入视觉树，但不会进入逻辑树。要在自定义控件中访问模板部件，请重写 `OnApplyTemplate`：

```csharp
protected override void OnApplyTemplate(TemplateAppliedEventArgs e)
{
    base.OnApplyTemplate(e);

    // Find a named element from the template
    var border = e.NameScope.Find<Border>("PART_Border");
    var textBlock = e.NameScope.Find<TextBlock>("PART_Text");
}
```

按惯例，模板部件的名称都带 `PART_` 前缀，以便和逻辑子元素区分开。

## 覆盖层 {#overlay-layers}

在每个窗口里，Avalonia 都在常规控件内容之上管理着几个特殊的层。它们分别负责装饰器、自定义覆盖内容和弹出窗口：

| 层 | 用途 | 访问方式 |
|---|---|---|
| `AdornerLayer` | 焦点指示器、拖放装饰器，以及附着在控件上的各种视觉装饰。 | `AdornerLayer.GetAdornerLayer(visual)` |
| `OverlayLayer` | 你自己叠加的覆盖内容，位于常规控件之上、弹出窗口之下。 | `OverlayLayer.GetOverlayLayer(visual)` |
| 弹出层 | 承载弹出窗口（菜单、工具提示、下拉框列表）的内部层，由框架管理。 | 由弹出窗口系统在内部管理。 |

### 添加自定义覆盖内容 {#adding-custom-overlay-content}

用 `OverlayLayer` 可以展示浮在常规视觉树之上的内容，比如加载指示器、浮动工具栏或自定义通知面板：

```csharp
var overlay = OverlayLayer.GetOverlayLayer(myControl);
if (overlay is not null)
{
    var panel = new Border
    {
        Background = Brushes.Black,
        Opacity = 0.5,
        Child = new TextBlock
        {
            Text = "Loading...",
            Foreground = Brushes.White,
            HorizontalAlignment = HorizontalAlignment.Center,
            VerticalAlignment = VerticalAlignment.Center,
        }
    };

    overlay.Children.Add(panel);

    // Remove when done
    overlay.Children.Remove(panel);
}
```

覆盖内容显示在窗口中所有常规控件之上，但位于弹出窗口、菜单和工具提示之下。

## 另请参阅 {#see-also}

- [界面组合](/docs/fundamentals/ui-composition)：控件如何组合成界面。
- [控件树](/docs/custom-controls/control-trees)：自定义控件开发中的视觉树与逻辑树。
- [事件总览](/docs/events)：事件如何沿视觉树路由。
- [模板化控件](/docs/custom-controls/templated-controls)：用模板构建控件。
