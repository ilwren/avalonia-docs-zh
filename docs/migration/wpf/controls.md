---
id: controls
title: 控件
description: WPF 与 Avalonia 在控件层次结构、命名和行为上的差异。
doc-type: migration
---

import RenderTransformOriginWpfScreenshot from '/img/guides/migration/wpf/rendertransformorigin-wpf.png';
import RenderTransformOriginAvaloniaScreenshot from '/img/guides/migration/wpf/rendertransformorigin-avalonia.png';

本页介绍从 WPF 迁到 Avalonia 时会碰上的主要控件差异，包括基类变化、改了名的控件，以及行为上的不同。

## UIElement 与 FrameworkElement {#uielement-and-frameworkelement}

WPF 的 `UIElement` 和 `FrameworkElement` 是非模板化的控件基类，大体相当于 Avalonia 的 `Control` 类。而 WPF 的 `Control` 类则是模板化控件，Avalonia 中与之对应的是 `TemplatedControl`。

- 在 WPF/UWP 中，你会继承 `Control` 类来做新的模板化控件；在 Avalonia 中，则应当继承 `TemplatedControl.`
- 在 WPF/UWP 中，你会继承 `FrameworkElement` 类来做新的自绘控件；在 Avalonia 中，则应当继承 `Control.`

小结一下：

* `UIElement` 🠞 `Control`
* `FrameworkElement`🠞 `Control`
* `Control` 🠞 `TemplatedControl`

## RenderTransform 与 RenderTransformOrigin {#rendertransforms-and-rendertransformorigin}

WPF 和 Avalonia 的 RenderTransformOrigin 并不相同：若你要施加 `RenderTransform`，请记住 Avalonia 中 RenderTransformOrigin 的默认值是 `RelativePoint.Center`，而 WPF 的默认值是 `RelativePoint.TopLeft` \(0, 0\)。在 Viewbox 这类控件上，同样的代码会渲染出不同的结果：

**在 WPF 中：**
<Image light={RenderTransformOriginWpfScreenshot} alt="WPF" position="center" maxWidth={400} cornerRadius="true"/>

**在 Avalonia 中：**
<Image light={RenderTransformOriginAvaloniaScreenshot} alt="Avalonia" position="center" maxWidth={400} cornerRadius="true"/>

在 AvaloniaUI 中，若想得到同样的缩放效果，就得把 RenderTransformOrigin 指明为该视觉元素的左上角。

## Grid

在 Avalonia 中，行列定义可以用字符串写出来，省去了 WPF 那套笨重的语法：

```xml
<Grid ColumnDefinitions="Auto,*,32" RowDefinitions="*,Auto">
```

在 WPF 中，`Grid` 常被用来把两个控件叠在一起。在 Avalonia 里，这种场合可以改用 `Panel`，它比 `Grid` 轻量。

## ToolTip

WPF 用的是 `ToolTip` 属性或子元素，Avalonia 用的则是 `ToolTip.Tip` 附加属性：

```xml title="WPF"
<Button ToolTip="Save the document" Content="Save" />
```

```xml title="Avalonia"
<Button ToolTip.Tip="Save the document" Content="Save" />
```

## ItemsControl 与 ItemsSource {#itemscontrol-and-itemssource}

WPF 的 `ItemsControl.Items` 可以直接赋值。在 Avalonia 中，数据绑定请用 `ItemsSource`，或者直接在 XAML 里添加子元素：

```xml title="Avalonia"
<ListBox ItemsSource="{Binding MyItems}">
    <ListBox.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Name}" />
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

注意：在 Avalonia 中，`ItemsSource` 取代了 `ItemsSource`（名字相同），但 `Items` 是只读的——你不能给 `Items` 赋一个新集合。

## DataGrid

在 Avalonia 中，DataGrid 是单独的 NuGet 包：

```xml
<PackageReference Include="Avalonia.Controls.DataGrid" Version="$(AvaloniaVersion)" />
```

你还必须在 `App.axaml` 中引入 DataGrid 主题：

```xml
<Application.Styles>
    <FluentTheme />
    <StyleInclude Source="avares://Avalonia.Controls.DataGrid/Themes/Fluent.axaml" />
</Application.Styles>
```

## StatusBar

Avalonia 没有 `StatusBar` 控件。你可以在窗口底部放一个带样式的 `DockPanel` 或 `StackPanel`：

```xml
<DockPanel>
    <Border DockPanel.Dock="Bottom" Background="{DynamicResource SystemChromeLowColor}" Padding="8,4">
        <TextBlock Text="Ready" />
    </Border>
    <!-- Main content -->
</DockPanel>
```

## RichTextBox

Avalonia 不内置 `RichTextBox`。若需要富文本编辑，请使用 AvalonEdit 之类的第三方控件。

## 另请参阅 {#see-also}

- [WPF 到 Avalonia 速查表](/docs/migration/wpf/cheat-sheet)：全部控件映射的快速参考。
- [控件参考](/controls)：Avalonia 控件的完整文档。