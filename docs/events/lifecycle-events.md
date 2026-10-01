---
id: lifecycle-events
title: 生命周期事件
description: Avalonia 中控件的初始化、挂载到视觉树以及销毁相关的事件。
doc-type: reference
---

Avalonia 控件在创建、挂载到视觉树以及被移除的过程中会引发若干事件。弄清这些事件的顺序和用途，对于初始化控件、加载数据和清理资源都很重要。

## 生命周期事件的顺序 {#lifecycle-event-order}

### 控件创建 {#control-creation}

控件被创建并加入视觉树时，事件按以下顺序触发：

| 顺序 | Event / Method | 定义于 | 说明 |
|---|---|---|---|
| 1 | `Initialized` | `StyledElement` | XAML 中的所有属性值都已设置完毕。此时控件还不属于视觉树。 |
| 2 | `AttachedToVisualTree` | `Visual` | 控件已加入一棵有根的视觉树，但布局尚未发生。 |
| 3 | `Loaded` | `Control` | 控件已完全挂载，可以开始交互。该事件在视觉树挂载全部完成之后触发。 |

### 控件移除 {#control-removal}

控件被移除时：

| 顺序 | Event / Method | 定义于 | 说明 |
|---|---|---|---|
| 1 | `Unloaded` | `Control` | 控件即将从视觉树中移除。 |
| 2 | `DetachedFromVisualTree` | `Visual` | 控件已从视觉树中移除。 |

### 布局的应用 {#layout-application}

除了上述事件，布局类控件还可以通过下面这些方法参与改变视觉树。

首次运行时（也就是控件初次挂载到视觉树时），这些事件按上述顺序，发生在[前文所述](#control-creation)的 `AttachedToVisualTree` 与 `Loaded` 两个事件之间。不过 `MeasureOverride` 和 `ArrangeOverride` 在控件的一生中可能跑很多次 —— 只要布局更新（比如调整窗口大小）就会触发。

| 顺序 | Event / Method | 定义于 | 说明 |
|---|---|---|---|
| 1 | `ApplyTemplate` | `Control` | 套用[控件模板](/docs/styling/control-template-walkthrough)，创建模板所需的各个视觉部件。 |
| 2 | `MeasureOverride` | `Control` | 在布局的[测量阶段](/docs/layout/#measuring-and-arranging-children)被调用，用于确定控件期望的尺寸。 |
| 3 | `ArrangeOverride` | `Control` | 在布局的[排列阶段](/docs/layout/#measuring-and-arranging-children)被调用，用于确定控件的最终尺寸。 |

## Initialized

当 XAML 加载器把标记中定义的所有属性都设置完毕时，就会触发 `Initialized` 事件。此时控件的属性值已就位，但它可能还不属于任何视觉树。

```csharp
public class MyControl : Control
{
    protected override void OnInitialized()
    {
        base.OnInitialized();
        // Properties from XAML are set
        // Visual tree may not be available yet
    }
}
```

也可以在外部订阅：

```csharp
myControl.Initialized += (sender, e) =>
{
    // Control is initialized
};
```

**适用场景**：初始化那些依赖 XAML 属性值、但不需要视觉树的内部状态。

## AttachedToVisualTree / DetachedFromVisualTree

当控件被加入或移出一棵有根的视觉树（即根部有 `TopLevel` 的树）时，这些事件会触发。

```csharp
public class MyControl : Control
{
    protected override void OnAttachedToVisualTree(VisualTreeAttachmentEventArgs e)
    {
        base.OnAttachedToVisualTree(e);
        // e.RootVisual is the root of the visual tree
        // Start listening to external services, timers, etc.
    }

    protected override void OnDetachedFromVisualTree(VisualTreeAttachmentEventArgs e)
    {
        base.OnDetachedFromVisualTree(e);
        // Clean up external subscriptions, timers, etc.
    }
}
```

`VisualTreeAttachmentEventArgs` 提供了：

| 属性 | 类型 | 说明 |
|---|---|---|
| `RootVisual` | `Visual` | 控件所挂载到的那棵树的根视觉元素。 |
| `AttachmentPoint` | `Visual` | 控件直接挂载到、或从中分离的那个视觉元素。 |
| `PresentationSource` | `IPresentationSource` | 承载该视觉树的呈现源。 |

**适用场景**：订阅或退订那些只应在控件可见期间保持活跃的外部服务、平台 API 或事件。

## Loaded / Unloaded

`Loaded` 事件在控件挂载到视觉树、且相关初始化全部完成之后触发；控件被移除时则触发 `Unloaded` 事件。

```csharp
public class MyControl : Control
{
    protected override void OnLoaded(RoutedEventArgs e)
    {
        base.OnLoaded(e);
        // Control is fully ready
        // Layout has occurred, bindings are active
    }

    protected override void OnUnloaded(RoutedEventArgs e)
    {
        base.OnUnloaded(e);
        // Clean up
    }
}
```

也可以通过 XAML 或代码订阅：

```csharp
myControl.Loaded += (sender, e) =>
{
    // Control is loaded and ready
};
```

**适用场景**：执行那些要求控件已完全就绪、且视觉树处于活跃状态的操作，比如启动动画、测量布局或拉取数据。

### Loaded 与 AttachedToVisualTree 的区别 {#loaded-vs-attachedtovisualtree}

这两个事件都表示控件已经进入视觉树，关键差别在于：

- `AttachedToVisualTree` 在控件一进入树时就立即触发，它是 `Visual` 上的普通 CLR 事件。
- `Loaded` 则在挂载彻底完成之后才触发，它是 `Control` 上的 `RoutedEvent`。

大多数场景下选 `Loaded` 就对了。只有当你需要拿到 `Root` 引用、或者要处理非 `Control` 的视觉元素时，才用 `AttachedToVisualTree`。

## ApplyTemplate

该方法负责套用控件的控件模板。

```csharp
public class MyControl : Control
{
    protected override void OnApplyTemplate(TemplateAppliedEventArgs e)
    {
        base.OnApplyTemplate(e);
    }
}
```

## MeasureOverride / ArrangeOverride

每当控件需要走一遍[两阶段布局流程](/docs/layout/#measuring-and-arranging-children)来确定自身在布局中的尺寸和位置时，布局系统就会调用这些可重写的方法。

```csharp
public class MyControl : Control
{
    protected override Size MeasureOverride(Size availableSize)
    {
        // Calculates the desired size
        return base.MeasureOverride(availableSize);
    }

    protected override Size ArrangeOverride(Size finalSize)
    {
        // Allocates the final size
        return base.ArrangeOverride(finalSize);
    }
}
```

## DataContextChanged

每当 `StyledElement` 上的 `DataContext` 属性发生变化，就会触发 `DataContextChanged` 事件：

```csharp
myControl.DataContextChanged += (sender, e) =>
{
    var newContext = ((Control)sender!).DataContext;
    // React to the new data context
};
```

该事件在以下情况下触发：
- 直接在控件上设置了 `DataContext`。
- 父级的 `DataContext` 变了，导致继承而来的 `DataContext` 随之改变。
- 控件被移动到视觉树的另一处，而那里继承到的 `DataContext` 不同。

:::warning
切勿在 `DataContextChanged` 或 `OnPropertyChanged` 中改动逻辑树！

`DataContext` 是可继承属性，它一变就会引发一次沿逻辑树向下的遍历，把新值传播给后代。若在遍历进行期间改动 `LogicalChildren`，就可能引发绑定错误。

更多说明请见[改动逻辑树](/docs/fundamentals/visual-and-logical-trees#mutating-the-logical-tree)。
:::

## 常见的初始化套路 {#typical-initialization-patterns}

### 在视图中加载数据 {#loading-data-in-a-view}

```csharp
public partial class CustomerView : UserControl
{
    public CustomerView()
    {
        InitializeComponent();
    }

    protected override void OnLoaded(RoutedEventArgs e)
    {
        base.OnLoaded(e);

        if (DataContext is CustomerViewModel vm)
        {
            vm.LoadCustomersCommand.Execute(null);
        }
    }
}
```

### 管理订阅 {#managing-subscriptions}

```csharp
public class StatusMonitor : Control
{
    private IDisposable? _subscription;

    protected override void OnAttachedToVisualTree(VisualTreeAttachmentEventArgs e)
    {
        base.OnAttachedToVisualTree(e);
        _subscription = StatusService.StatusChanged.Subscribe(OnStatusChanged);
    }

    protected override void OnDetachedFromVisualTree(VisualTreeAttachmentEventArgs e)
    {
        _subscription?.Dispose();
        _subscription = null;
        base.OnDetachedFromVisualTree(e);
    }

    private void OnStatusChanged(string status)
    {
        // Update the control
    }
}
```

## 另请参阅 {#see-also}

- [事件总览](/docs/events)：路由事件系统的工作方式。
- [应用程序生命周期](/docs/fundamentals/application-lifetimes)：应用级的生命周期事件。
- [界面组合](/docs/fundamentals/ui-composition)：控件在视觉树中如何组合。
