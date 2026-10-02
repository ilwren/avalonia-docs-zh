---
id: panel
title: 面板
description: 一个基础布局控件：把多个子控件层叠在一起，并按对齐属性摆放它们。
doc-type: reference
---

# Panel

`Panel` 是能容纳多个子控件的最基础布局控件。它按子控件在 XAML 中出现的顺序绘制，一层层叠上去，每个子元素则按自己的 `HorizontalAlignment` 和 `VerticalAlignment` 属性定位。

由于 `Panel` 不会把子元素排成行、列或任何其他结构，它最适合需要内容重叠的场合，比如把文字压在图片上，或堆叠若干装饰元素。

## 常用属性 {#common-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Background` | `IBrush` | 面板的背景画刷。必须设置它（哪怕设成 `Transparent`），面板才能接收指针事件。 |
| `Children` | `Controls` | 面板中所含子控件的集合。 |

## 基本示例 {#basic-example}

这个例子用了几处 50% 的不透明度，好让你看清子控件是重叠的。

<XamlPreview>

```xml
<Panel xmlns="https://github.com/avaloniaui"
       Margin="10">
    <Rectangle Fill="Red" Height="100" VerticalAlignment="Top"/>
    <Rectangle Fill="Green" Height="100" VerticalAlignment="Bottom"/>
    <Rectangle Fill="Blue" Width="100" HorizontalAlignment="Right" />
    <Rectangle Fill="Orange" Width="100" HorizontalAlignment="Left"/>
</Panel>
```

</XamlPreview>

## 用 `ZIndex` 控制重叠关系 {#controlling-overlap-with-zindex}

子元素重叠时，可以用 `ZIndex` 附加属性控制绘制顺序：值大的画在值小的上面。默认情况下所有子元素的 `ZIndex` 都是 0，按它们在标记中出现的顺序绘制。

```xml
<Panel>
    <Border Background="Red" Width="100" Height="100" ZIndex="1" />
    <Border Background="Blue" Width="100" Height="100" Margin="30,30,0,0" ZIndex="2" />
</Panel>
```

本例中蓝色边框渲染在红色边框之上，因为它的 `ZIndex` 更大。

## 设置背景以便命中测试 {#setting-a-background-for-hit-testing}

若不设置 `Background`，面板对指针事件是透明的：点击等指针交互会直接穿透到它背后的内容上。要让面板在整个区域内都响应指针事件，请把 `Background` 设为 `Transparent`：

```xml
<Panel Background="Transparent">
    <TextBlock Text="This panel captures pointer events everywhere." />
</Panel>
```

## 以 `Panel` 为基类做自定义面板 {#using-panel-as-a-base-for-custom-panels}

`Panel` 是所有内置面板控件的基类。如果内置面板都满足不了你的布局需求，可以从 `Panel` 派生并重写它的 `MeasureOverride` 和 `ArrangeOverride` 方法，做一个自定义面板。

```csharp
public class MyCustomPanel : Panel
{
    protected override Size MeasureOverride(Size availableSize)
    {
        foreach (var child in Children)
        {
            child.Measure(availableSize);
        }

        return availableSize;
    }

    protected override Size ArrangeOverride(Size finalSize)
    {
        foreach (var child in Children)
        {
            child.Arrange(new Rect(finalSize));
        }

        return finalSize;
    }
}
```

:::info
完整演练请参阅[自定义面板](/docs/custom-controls/custom-panel)。
:::

## 其他面板控件 {#other-panel-controls}

如果你想更精细地控制子元素的位置，不妨考虑下面这些专门的面板：

- [堆叠面板](/controls/layout/panels/stackpanel)：把子元素横着或竖着排成一条线。
- [停靠面板](/controls/layout/panels/dockpanel)：把子元素停靠到面板的各个边缘。
- [网格](/controls/layout/panels/grid)：把子元素按行列排布。
- [环绕面板](/controls/layout/panels/wrappanel)：把子元素排成一行，到达面板边缘时自动换行。
- [画布](/controls/layout/panels/canvas)：把子元素摆在显式指定的坐标上。
- [相对面板](/controls/layout/panels/relativepanel)：让子元素相对彼此或相对面板本身定位。
- [均分网格](/controls/layout/panels/uniformgrid)：把子元素排进单元格大小相同的网格里。

## 另请参阅 {#see-also}

- [Panel API 参考](/api/avalonia/controls/panel)
- [GitHub 上的 `Panel.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Panel.cs)
- [自定义面板](/docs/custom-controls/custom-panel)
