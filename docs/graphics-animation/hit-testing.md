---
id: hit-testing
title: 命中测试
description: Avalonia 如何判定某个屏幕坐标上是哪个视觉元素。
doc-type: explanation
---

命中测试用来判定屏幕上某一点位于哪个视觉元素之上。Avalonia 在内部靠它处理指针事件，但你也可以为自定义控件和进阶交互场景主动调用命中测试。

## 命中测试的运作原理 {#how-hit-testing-works}

指针事件发生时，Avalonia 自最顶层元素起向下遍历视觉树，逐个检查该点是否落在元素的边界及其渲染内容之内。第一个通过检查的元素就成为事件目标。

命中测试会考虑这几点：

1. **可见性**：`IsVisible="False"` 的元素会被跳过。
2. **IsHitTestVisible**：`IsHitTestVisible="False"` 的元素会被跳过，但它的子元素仍可能参与测试。
3. **边界**：该点必须落在元素的布局边界之内。
4. **渲染内容**：对于形状和自绘控件，检查的是实际渲染出的像素，而不只是外接矩形。

## IsHitTestVisible

设置 `IsHitTestVisible="False"` 可让控件对指针事件「透明」：它照常渲染，但指针事件会穿过去落到它后面的控件上：

```xml
<!-- This overlay displays text but passes clicks through to controls underneath -->
<Panel>
    <Button Content="Click Me" />
    <TextBlock Text="Overlay label" IsHitTestVisible="False"
               HorizontalAlignment="Right" VerticalAlignment="Top"
               Foreground="Gray" Margin="8" />
</Panel>
```

常见用途：
- 不该拦截点击的装饰性覆盖层
- 盖在可交互内容之上的水印或状态文字
- 动画图层

## 背景与命中测试 {#background-and-hit-testing}

没有 `Background` 的控件（或 `Background` 设为 `null` 的控件），其空白区域不参与命中测试，只有子内容才收得到指针事件。

若希望面板的整片区域都响应指针事件，请设置 `Background="Transparent"`：

```xml
<!-- This panel does NOT receive clicks in empty areas -->
<StackPanel PointerPressed="OnPressed">
    <TextBlock Text="Only this text is clickable" />
</StackPanel>

<!-- This panel receives clicks anywhere within its bounds -->
<StackPanel PointerPressed="OnPressed" Background="Transparent">
    <TextBlock Text="Click anywhere in the panel" />
</StackPanel>
```

## 以编程方式做命中测试 {#programmatic-hit-testing}

### InputHitTest

在任意控件上调用 `InputHitTest`，即可找出指定点上的元素：

```csharp
// Point is relative to the control you call InputHitTest on
var result = myPanel.InputHitTest(new Point(50, 30));

if (result is Control hitControl)
{
    Debug.WriteLine($"Hit: {hitControl.GetType().Name}");
}
```

### 找出指针下方的元素 {#finding-the-element-under-the-pointer}

在指针事件处理程序中，事件参数的 `Source` 属性会告诉你最初的那个元素：

```csharp
private void OnPointerPressed(object? sender, PointerPressedEventArgs e)
{
    // e.Source is the element that was directly hit
    if (e.Source is Border border)
    {
        border.Background = Brushes.Yellow;
    }
}
```

## 自定义控件中的命中测试 {#hit-testing-in-custom-controls}

当你编写用 `DrawingContext` 自绘内容的自定义控件时，可能需要重写命中测试，让它与实际画出的形状吻合。

### 自定义命中测试几何 {#custom-hit-test-geometry}

重写 `HitTestCore` 方法来定义自定义的命中区域：

```csharp
public class CircleControl : Control
{
    public override void Render(DrawingContext context)
    {
        var radius = Math.Min(Bounds.Width, Bounds.Height) / 2;
        var center = new Point(Bounds.Width / 2, Bounds.Height / 2);
        context.DrawEllipse(Brushes.Blue, null, center, radius, radius);
    }

    protected override bool HitTest(Point point)
    {
        // Only hit test within the circle, not the full bounding box
        var radius = Math.Min(Bounds.Width, Bounds.Height) / 2;
        var center = new Point(Bounds.Width / 2, Bounds.Height / 2);
        var distance = Point.Distance(point, center);
        return distance <= radius;
    }
}
```

有了这个重写，只有用户点在圆内时才会触发指针事件，点在外接矩形的四角上则不会。

## 命中测试的先后顺序 {#hit-testing-order}

当同一点上有多个控件重叠时，命中测试返回视觉树中最靠上的那个。顺序由以下两点决定：

1. **ZIndex**：`ZIndex` 值更大的先被测试。
2. **视觉树顺序**：同一面板中，靠后的子元素渲染（以及命中测试）时位于靠前子元素之上。

```xml
<Panel>
    <Border Background="Red" Width="100" Height="100" />
    <!-- This border is on top and receives the click -->
    <Border Background="Blue" Width="100" Height="100" Margin="30" />
</Panel>
```

## 实用套路 {#practical-patterns}

### 可点穿的覆盖层 {#click-through-overlay}

做一个不挡交互的视觉覆盖层：

```xml
<Grid>
    <ListBox ItemsSource="{Binding Items}" />

    <!-- Semi-transparent loading overlay, clicks pass through when hidden -->
    <Border Background="#80000000"
            IsVisible="{Binding IsLoading}"
            IsHitTestVisible="{Binding IsLoading}">
        <ProgressBar IsIndeterminate="True" Width="200"
                     HorizontalAlignment="Center" VerticalAlignment="Center" />
    </Border>
</Grid>
```

### 检测画布绘图上的点击 {#detecting-clicks-on-a-canvas-drawing}

```csharp
private void OnCanvasPointerPressed(object? sender, PointerPressedEventArgs e)
{
    var pos = e.GetPosition((Visual)sender!);

    // Check against your drawn shapes
    foreach (var shape in _shapes)
    {
        if (shape.Bounds.Contains(pos))
        {
            SelectShape(shape);
            e.Handled = true;
            return;
        }
    }
}
```

## 元素众多时的性能 {#performance-with-many-elements}

Avalonia 的命中测试会遍历视觉树并逐个测试元素，没有内置的空间划分结构（比如四叉树）。面板里子元素不多时这很快；可一旦 `Canvas` 或 `Panel` 上有成百上千个可交互元素，这种线性遍历就会变得明显——尤其是指针按下事件，每个候选元素都得测一遍。

### Symptoms

- 从点击到 `PointerPressed` 事件触发之间出现延迟，且延迟随子元素数量线性增长。
- 这个延迟出在输入环节，不是渲染或布局的问题，帧率依然正常。

### Strategies

**关掉各个元素的命中测试，改用覆盖层。**在所有子元素之上放一层透明覆盖层，在它上面处理 `PointerPressed`，再用你自己的逻辑判断点中的是哪个元素。同时给子元素设上 `IsHitTestVisible="False"`，这样 Avalonia 遍历树时就会跳过它们：

```xml
<Panel>
    <!-- All items have IsHitTestVisible="False" -->
    <Canvas x:Name="ItemsCanvas" IsHitTestVisible="False">
        <!-- Hundreds of child controls -->
    </Canvas>

    <!-- Transparent overlay catches all pointer events -->
    <Border Background="Transparent" PointerPressed="OnOverlayPointerPressed" />
</Panel>
```

```csharp
private void OnOverlayPointerPressed(object? sender, PointerPressedEventArgs e)
{
    var pos = e.GetPosition(ItemsCanvas);

    // Use your own spatial lookup to find the item at this position
    var item = FindItemAt(pos);
    if (item != null)
    {
        SelectItem(item);
        e.Handled = true;
    }
}
```

你的 `FindItemAt` 方法可以采用任何契合你数据的查找策略。若元素呈网格状排列，简单算一下坐标也许就够了；若形状不规则，不妨考虑四叉树或 R 树之类的空间索引。

**改用自定义渲染。**与其为每个元素都建一个控件，不如在单个控件的 `Render` 重写中把所有元素一起画出来。这样逐元素的命中测试就彻底没了，因为参与命中测试的只有这一个父控件。之后你在这个控件上处理指针事件，根据指针位置判断点中的是哪个逻辑元素。详见[自定义渲染](/docs/graphics-animation/custom-rendering)。

**减少参与命中测试的元素数量。**若只有部分元素需要交互，就给其余元素设上 `IsHitTestVisible="False"`。比如在图表编辑器里，背景网格线和标签都可以排除在命中测试之外，只留下可拖动的节点保持交互。

## 另请参阅 {#see-also}

- [指针输入](/docs/input-interaction/pointer)：指针事件与位置。
- [自定义渲染](/docs/graphics-animation/custom-rendering)：用 DrawingContext 作画。
- [形状与几何](/docs/graphics-animation/shapes-and-geometries)：可用作命中区域的几何类型。
- [性能优化](/docs/app-development/performance)：通用的性能建议。
