---
id: tooltip
title: ToolTip
---

import ToolTipTextHoverScreenshot from '/img/reference/controls/tooltip/tooltip-text-hover.gif';
import ToolTipContentScreenshot from '/img/reference/controls/tooltip/tooltip-content-hover.gif';

`ToolTip` 是一个弹出提示：当用户把指针悬停在它所附着的「宿主」控件上时，它就把内容显示出来。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table>
    <thead>
        <tr>
            <th width="298">Property</th>
            <th>说明</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>ToolTip.Tip</code></td>
            <td>承载提示内容的附加属性。</td>
        </tr>
        <tr>
            <td><code>ToolTip.Placement</code></td>
            <td>定义提示相对于宿主或指针的位置，可选 top、bottom、
                left、right、anchor and gravity、pointer。默认值是 pointer，即把提示内容放在指针停下来的位置。</td>
        </tr>
        <tr>
            <td><code>ToolTip.HorizontalOffset</code></td>
            <td>提示相对于定位点的水平偏移（默认 0）。</td>
        </tr>
        <tr>
            <td><code>ToolTip.VerticalOffset</code></td>
            <td>提示相对于定位点的垂直偏移（默认 20）。</td>
        </tr>
        <tr>
            <td><code>ToolTip.ShowDelay</code></td>
            <td>指针需要静止多久提示才会出现，单位毫秒（默认
                400).</td>
        </tr>
        <tr>
            <td><code>ToolTip.BetweenShowDelay</code></td>
            <td>上一次显示之后，多久之内不再弹出提示，单位毫秒（默认 100）。</td>
        </tr>
        <tr>
            <td><code>ToolTip.ShowOnDisabled</code></td>
            <td>决定是否为已禁用的元素显示提示（默认 false）。</td>
        </tr>
        <tr>
            <td><code>ToolTip.ServiceEnabled</code></td>
            <td>决定提示服务是否启用（默认 true）。</td>
        </tr>
    </tbody>
</table>

## 事件 {#events}

| 事件 | 类型 | 说明 |
|---|---|---|
| `ToolTip.ToolTipOpening` | `CancelRoutedEventArgs` | 提示即将打开时引发。设置 `Cancel = true` 可阻止提示显示。 |
| `ToolTip.ToolTipClosing` | `RoutedEventArgs` | 提示即将关闭时引发。 |

它们是附加路由事件，可在 XAML 或代码中订阅：

```xml
<Button Content="Hover me"
        ToolTip.Tip="Dynamic tooltip"
        ToolTip.ToolTipOpening="OnToolTipOpening" />
```

```csharp
private void OnToolTipOpening(object? sender, CancelRoutedEventArgs e)
{
    // Optionally prevent the tooltip from showing
    if (ShouldSuppressTooltip)
    {
        e.Cancel = true;
    }
}
```

## 示例 {#examples}

这是一个简单的纯文本提示，位置和延时都用默认值。把指针悬停到预览里的矩形上就能看到效果。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <Rectangle Fill="Aqua" Height="150" Width="200"
             ToolTip.Tip="This is a rectangle" />
</UserControl>
```

</XamlPreview>

<Image light={ToolTipTextHoverScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

想让提示的呈现更丰富，可以用 `<ToolTip.Tip>` 元素。把指针悬停到预览里的矩形上就能看到效果。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <Rectangle Fill="Aqua" Height="150" Width="200"
             ToolTip.Placement="Bottom">
      <ToolTip.Tip>
        <StackPanel>
          <TextBlock FontSize="16">Rectangle</TextBlock>
          <TextBlock>Some explanation here.</TextBlock>
        </StackPanel>
      </ToolTip.Tip>
  </Rectangle>
</UserControl>
```

</XamlPreview>

<Image light={ToolTipContentScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [ToolTip API 参考](/api/avalonia/controls/tooltip)
- [GitHub 上的 `ToolTip.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ToolTip.cs)
