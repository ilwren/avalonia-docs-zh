---
id: listbox
title: ListBox
---

import ListBoxStringScreenshot from '/img/controls/listbox/listbox-string.gif';
import ListBoxDataTemplateScreenshot from '/img/controls/listbox/listbox-datatemplate.gif';
import ListBoxDevToolsScreenshot from '/img/controls/listbox/listbox-devtools.png';
import ListBoxItemStyleScreenshot from '/img/controls/listbox/listbox-item-style.gif';

`ListBox` 把条目源集合中的各项分多行显示出来，并支持单选或多选。

列表中的条目可以自行组合、绑定，也可以套用模板。

列表的高度会自动撑开以容纳全部条目，除非你显式指定（用 height 特性），或由 [DockPanel](/controls/layout/panels/dockpanel) 这类父容器控件决定。

当高度受限而条目总高度又超出时，列表框内置的滚动查看器会显示一条垂直滚动条。

同样，当某个条目的宽度超出列表框宽度时，内置的滚动查看器会显示一条水平滚动条（除非被禁用，详见下文）。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table>
  <thead>
    <tr><th width="289">Property</th>
    <th>说明</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><code>Items</code></td>
      <td></td>
    </tr>
    <tr>
      <td><code>SelectedIndex</code></td>
      <td>选中项的索引（从零开始）；多选时则是第一个选中项的索引。</td>
    </tr>
    <tr>
      <td><code>SelectedItem</code></td>
      <td>条目集合中被选中的那一项（对象）；多选时则是第一个选中项。</td>
    </tr>
    <tr>
      <td><code>SelectedItems</code></td>
      <td>列表中的所有选中项。</td>
    </tr>
    <tr>
      <td><code>Selection</code></td>
      <td>An <code>ISelectionModel</code> 该对象提供多种方法来跟踪多个选中项，并针对大型条目集合作了优化。</td>
    </tr>
    <tr>
      <td><code>SelectionMode</code></td>
      <td>选择模式，详见下表。</td>
    </tr>
    <tr>
      <td><p><code>ScrollViewer.Horizontal</code></p><p><code>ScrollBarVisibility</code></p></td>
      <td>内置滚动查看器的水平滚动条可见性。可选值有「Disabled」（默认）、「Auto」、「Hidden」和「Visible」。设为 Disabled 时，溢出内容会被隐藏。 </td>
    </tr>
    <tr>
      <td><p><code>ScrollViewer.Vertical</code></p><p><code>ScrollBarVisibility</code></p></td>
      <td>内置滚动查看器的垂直滚动条可见性。可选值有「Disabled」、「Auto」（默认）、「Hidden」和「Visible」。设为 Disabled 时，溢出内容会被隐藏。 </td>
    </tr>
    <tr>
      <td><code>ItemsPanel</code></td>
      <td>用于摆放条目的容器面板。定制 `ItemsPanel` 的做法请参阅[自定义面板](/docs/how-to/itemscontrol-how-to#custom-panel)。</td>
    </tr>
    <tr>
      <td><code>Styles</code></td>
      <td>应用到 ItemControl 任意子元素上的样式。</td>
    </tr>
  </tbody>
</table>

:::info
条目集合很大时，建议使用 `ISelectionModel` 以优化性能。
:::

## 选择模式 {#selection-mode}

在触摸和手写笔设备上，选择发生在指针抬起时而非按下时。这样用户就能从某个条目上开始滑动或滚动，而不会误改选择。

列表框支持下列几种选择模式：

<table><thead><tr><th width="237">Selection Mode</th><th>说明</th></tr></thead><tbody><tr><td><code>Single</code></td><td>只能选中一项（默认）。</td></tr><tr><td><code>Multiple</code></td><td>可以选中多项。</td></tr><tr><td><code>Toggle</code></td><td>点按或按空格键即可切换条目的选中状态。未启用时，必须配合 Shift 或 Ctrl 才能多选。</td></tr><tr><td><code>AlwaysSelected</code></td><td>只要还有条目可选，就始终保持有一项处于选中状态。</td></tr></tbody></table>

这些取值可以组合使用，例如：

```xml
<ListBox SelectionMode="Multiple,Toggle">
```

## Example

下面这个例子在 C# 代码隐藏中把 `ItemsSource` 属性设成了一个数组。

```xml
<StackPanel Margin="20">
  <TextBlock Margin="0 5">Choose an animal:</TextBlock>
  <ListBox x:Name="animals"/>
</StackPanel>
```

```csharp title='C#'
using Avalonia.Controls;
using System.Linq;

namespace AvaloniaControls.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            animals.ItemsSource = new string[]
                {"cat", "camel", "cow", "chameleon", "mouse", "lion", "zebra" }
            .OrderBy(x => x);
        }
    }
}
```

<Image light={ListBoxStringScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 条目模板 {#item-template}

在列表框的 `ItemTemplate` 元素内放一个**数据模板**，即可自定义条目的呈现方式。

:::info
若想回顾**数据模板**背后的概念，请参阅[数据模板简介](/docs/data-templates/introduction-to-data-templates)。
:::

下面这个例子把每个条目放进一个圆角蓝色边框里。C# 代码隐藏与前面相同：

```xml
<DockPanel Margin="20">
  <TextBlock Margin="0 5" DockPanel.Dock="Top">Choose an animal:</TextBlock>
  <ListBox x:Name="animals">
    <ListBox.ItemTemplate>
      <DataTemplate>
        <Border BorderBrush="Blue" BorderThickness="1" 
                CornerRadius="4" Padding="4">
          <TextBlock Text="{Binding}"/>
        </Border>
      </DataTemplate>
    </ListBox.ItemTemplate>
  </ListBox>
</DockPanel>
```

```csharp title='C#'
using Avalonia.Controls;
using System.Linq;

namespace AvaloniaControls.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            animals.ItemsSource = new string[]
                {"cat", "camel", "cow", "chameleon", "mouse", "lion", "zebra" }
            .OrderBy(x => x);
        }
    }
}
```

这里列表是停靠面板的填充区域，高度取剩余空间，于是列表框中就出现了滚动条。

<Image light={ListBoxDataTemplateScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 条目样式 {#item-styling}

列表框中显示的每个条目，都绘制在一个 [`ListBoxItem`](/api/avalonia/controls/listboxitem) 元素里。按 F12 打开 **Avalonia Dev Tools**，切到 **Visual Tools** 选项卡就能看到，例如：

<Image light={ListBoxDevToolsScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

`ListBoxItem` 元素充当 `ListBox.ItemTemplate` 元素中所指定内容的容器；它从不出现在 XAML 里，而是由 _Avalonia_ 自动生成。

也就是说，你可以写一条样式来定制列表框中的 `ListBoxItem` 元素。比如把列表项的宽度固定为 200 并右对齐：

```xml
<DockPanel Margin="20">
  <TextBlock Margin="0 5" DockPanel.Dock="Top">Choose an animal:</TextBlock>
  <ListBox x:Name="animals">
    <ListBox.Styles>
      <Style Selector="ListBoxItem">
        <Setter Property="Width" Value="200"/>
        <Setter Property="HorizontalAlignment" Value="Right"/>
      </Style>
    </ListBox.Styles>
  </ListBox>
</DockPanel>
```

```csharp title='C#'
using Avalonia.Controls;
using System.Linq;

namespace AvaloniaControls.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            animals.ItemsSource = new string[]
                {"cat", "camel", "cow", "chameleon", "mouse", "lion", "zebra" }
            .OrderBy(x => x);
        }
    }
}
```

<Image light={ListBoxItemStyleScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [ListBox API 参考](/api/avalonia/controls/listbox)
- [GitHub 上的 `ListBox.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ListBox.cs)
