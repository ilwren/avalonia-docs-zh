---
id: positioning-controls
title: 控件定位
description: 用 HorizontalAlignment、VerticalAlignment、Margin 和 Padding 精确摆放控件。
doc-type: explanation
---

import LayoutMarginsPaddingAlignmentBasicScreenshot from '/img/reference/layout/positioning/layout-margins-padding-alignment-graphic1.png';
import LayoutMarginsPaddingAlignmentBasicAnnotatedScreenshot from '/img/reference/layout/positioning/layout-margins-padding-alignment-graphic2.png';
import LayoutHorizontalAlignmentScreenshot from '/img/reference/layout/positioning/layout-horizontal-alignment-graphic.png';
import LayoutVerticalAlignmentScreenshot from '/img/reference/layout/positioning/layout-vertical-alignment-graphic.png';
import LayoutMarginsPaddingAlignmentComplexAnnotatedScreenshot from '/img/reference/layout/positioning/layout-margins-padding-alignment-graphic3.png';

Avalonia 控件提供了若干用于精确摆放子元素的属性。本文讨论其中最重要的四个：[`HorizontalAlignment`](/api/avalonia/layout/horizontalalignment)、`Margin`、`Padding` 和 [`VerticalAlignment`](/api/avalonia/layout/verticalalignment)。理解这些属性的效果很有必要 —— 在 Avalonia 应用中控制元素位置，靠的就是它们。

## 元素定位入门 {#introduction-to-element-positioning}

在 Avalonia 中摆放元素的办法很多，但要做出理想的布局，光挑对 `Panel` 元素还不够。精细的定位控制，需要你理解 `HorizontalAlignment`、`Margin`、`Padding` 和 `VerticalAlignment` 这几个属性。

下图展示了一个用到多个定位属性的布局场景。

<Image light={LayoutMarginsPaddingAlignmentBasicScreenshot} alt="Positioning Example" position="center" maxWidth={400} cornerRadius="true"/>

乍一看，图中的 [`Button`](/api/avalonia/controls/button) 元素像是随手摆上去的。其实它们的位置都由外边距、对齐方式和内边距的组合精确控制着。

下面这个例子演示如何做出上图的布局。一个 [`Border`](/api/avalonia/controls/border) 元素包裹着父级 [`StackPanel`](/api/avalonia/controls/stackpanel)，其 `Padding` 为 15 个设备无关像素 —— 这就是围在子 `StackPanel` 四周的那圈窄边 `LightBlue`。`StackPanel` 的各个子元素分别用来演示本文讲到的各种定位属性，其中三个 `Button` 元素同时演示了 `Margin` 和 `HorizontalAlignment` 两个属性。

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="AvaloniaApplication2.MainWindow"
        Title="AvaloniaApplication2">
  <Border Background="LightBlue"
          BorderBrush="Black"
          BorderThickness="2"
          Padding="15">
    <StackPanel Background="White"
                HorizontalAlignment="Center"
                VerticalAlignment="Top">
      <TextBlock Margin="5,0"
                 FontSize="18"
                 HorizontalAlignment="Center">
        Alignment, Margin and Padding Sample
      </TextBlock>
      <Button HorizontalAlignment="Left" Margin="20">Button 1</Button>
      <Button HorizontalAlignment="Right" Margin="10">Button 2</Button>
      <Button HorizontalAlignment="Stretch">Button 3</Button>
    </StackPanel>
  </Border>
</Window>

```

下图近距离展示了上例中用到的各个定位属性。本文后续几节会逐一详述每个定位属性的用法。

<Image light={LayoutMarginsPaddingAlignmentBasicAnnotatedScreenshot} alt="Positioning Properties" position="center" maxWidth={400} cornerRadius="true"/>

## 理解对齐属性 {#understanding-alignment-properties}

`HorizontalAlignment` 和 `VerticalAlignment` 这两个属性，描述的是子元素该如何摆放在父元素分配给它的布局空间里。两者配合使用，就能精确定位子元素。例如 `DockPanel` 的子元素可以指定四种水平对齐方式：`Left`、`Right`、`Center`，或者 [`Stretch`](/api/avalonia/media/stretch) 以填满可用空间。垂直方向也有一组类似的取值。

元素上显式设置的 `Height` 和 `Width` 属性，优先级高于 `Stretch` 属性的取值。若你同时设置了 `Height`、`Width` 和取值为 `Stretch` 的 `HorizontalAlignment`，那么 `Stretch` 的请求会被忽略。

### `HorizontalAlignment` property

`HorizontalAlignment` 属性声明子元素所采用的水平对齐方式。下表列出 `HorizontalAlignment` 属性的全部可选值。

| 成员 | 说明 |
| :--- | :--- |
| `Left` | 子元素在父元素分配的布局空间内靠左对齐。 |
| `Center` | 子元素在父元素分配的布局空间内居中对齐。 |
| `Right` | 子元素在父元素分配的布局空间内靠右对齐。 |
| `Stretch` \(Default\) | 子元素被拉伸以填满父元素分配的布局空间。显式设置的 `Width` 和 `Height` 取值优先。 |

下例演示如何把 `HorizontalAlignment` 属性应用到 `Button` 元素上。每个取值都写了出来，以便更清楚地对比各自的渲染效果。

```xml
<Button HorizontalAlignment="Left">Button 1 (Left)</Button>
<Button HorizontalAlignment="Right">Button 2 (Right)</Button>
<Button HorizontalAlignment="Center">Button 3 (Center)</Button>
<Button HorizontalAlignment="Stretch">Button 4 (Stretch)</Button>
```

上面的代码产出的布局大致如下图。图中可以看到每个 `HorizontalAlignment` 取值所带来的定位效果。

<Image light={LayoutHorizontalAlignmentScreenshot} alt="HorizontalAlignment Sample" position="center" maxWidth={400} cornerRadius="true"/>

### `VerticalAlignment` property

`VerticalAlignment` 属性描述子元素所采用的垂直对齐方式。下表列出 `VerticalAlignment` 属性的全部可选值。

| 成员 | 说明 |
| :--- | :--- |
| `Top` | 子元素在父元素分配的布局空间内靠上对齐。 |
| `Center` | 子元素在父元素分配的布局空间内居中对齐。 |
| `Bottom` | 子元素在父元素分配的布局空间内靠下对齐。 |
| `Stretch` \(Default\) | 子元素被拉伸以填满父元素分配的布局空间。显式设置的 `Width` 和 `Height` 取值优先。 |

下例演示如何把 `VerticalAlignment` 属性应用到 `Button` 元素上。每个取值都写了出来，以便更清楚地对比各自的渲染效果。为了把各取值的布局行为看得更分明，本例用一个显示了网格线的 [`Grid`](/api/avalonia/controls/grid) 元素作为父级。

```xml
<Border Background="LightBlue" BorderBrush="Black" BorderThickness="2" Padding="15">
    <Grid Background="White" ShowGridLines="True">
      <Grid.RowDefinitions>
        <RowDefinition Height="25"/>
        <RowDefinition Height="50"/>
        <RowDefinition Height="50"/>
        <RowDefinition Height="50"/>
        <RowDefinition Height="50"/>
      </Grid.RowDefinitions>
      <TextBlock Grid.Row="0" Grid.Column="0"
                 FontSize="18"
                 HorizontalAlignment="Center">
        VerticalAlignment Sample
      </TextBlock>
      <Button Grid.Row="1" Grid.Column="0" VerticalAlignment="Top">Button 1 (Top)</Button>
      <Button Grid.Row="2" Grid.Column="0" VerticalAlignment="Bottom">Button 2 (Bottom)</Button>
      <Button Grid.Row="3" Grid.Column="0" VerticalAlignment="Center">Button 3 (Center)</Button>
      <Button Grid.Row="4" Grid.Column="0" VerticalAlignment="Stretch">Button 4 (Stretch)</Button>
    </Grid>
</Border>
```

上面的代码产出的布局大致如下图。图中可以看到每个 `VerticalAlignment` 取值所带来的定位效果。

<Image light={LayoutVerticalAlignmentScreenshot} alt="VerticalAlignment property sample" position="center" maxWidth={400} cornerRadius="true"/>

## 理解外边距属性 {#understanding-margin-properties}

`Margin` 属性描述元素与其子元素或同级元素之间的距离。`Margin` 的取值可以是统一的，写成 `Margin="20"` 这样 —— 此时元素四周会套用 20 个设备无关像素的统一 `Margin`。`Margin` 也可以写成四个不同的值，依次表示左、上、右、下四个方向的外边距，比如 `Margin="0,10,5,25"`。用好 `Margin` 属性，就能非常精细地控制元素自身以及它的相邻元素、子元素的渲染位置。

非零的外边距会在元素 `Bounds` 之外留出空间。外边距也允许为负值 —— 它会把元素往反方向拉，使其与相邻元素重叠，或者越出父级的边界。

下例演示如何给一组 `Button` 元素套用统一的外边距。这些 `Button` 元素四个方向上都留出十像素的空隙，彼此间距均匀。

```xml
<Button Margin="10">Button 7</Button>
<Button Margin="10">Button 8</Button>
<Button Margin="10">Button 9</Button>
```

很多时候统一的外边距并不合适，这时就可以用不均匀的间距。下例演示如何给子元素套用不均匀的外边距。外边距按左、上、右、下的顺序书写。

```xml
<Button Margin="0,10,0,10">Button 1</Button>
<Button Margin="0,10,0,10">Button 2</Button>
<Button Margin="0,10,0,10">Button 3</Button>
```

### 理解内边距属性 {#understanding-the-padding-property}

内边距在多数方面与 `Margin` 相似。Padding 属性只在少数几个类上暴露出来，主要是出于方便，例如 `Border`、`TemplatedControl` 和 [`TextBlock`](/api/avalonia/controls/textblock) 都提供了 Padding 属性。`Padding` 属性会按指定的 `Thickness` 把子元素的有效尺寸撑大。

下例演示如何给父级 `Border` 元素套用 `Padding`。

```xml
<Border Background="LightBlue"
        BorderBrush="Black"
        BorderThickness="2"
        CornerRadius="45"
        Padding="25">
```

### 在应用中综合运用对齐、外边距和内边距 {#using-alignment-margins-and-padding-in-an-application}

`HorizontalAlignment`、`Margin`、`Padding` 和 `VerticalAlignment` 提供了构建复杂界面所需的定位控制。用好它们各自的效果来调整子元素的位置，你就能灵活地做出动态的应用与用户体验。

下面这个例子把本文讲到的概念都演示了一遍。它沿用本文第一个示例的骨架，在原来的 `Border` 中添加了一个 `Grid` 元素作为子元素；父级 `Border` 元素上套用了 `Padding`；`Grid` 把空间划分给三个子 `StackPanel` 元素；`Button` 元素再次用于展示 `Margin` 和 `HorizontalAlignment` 的各种效果；每个 `ColumnDefinition` 中还加了 `TextBlock` 元素，以便更清楚地标明该列 `Button` 元素上所套用的各项属性。

```xml
<Border Background="LightBlue"
        BorderBrush="Black"
        BorderThickness="2"
        CornerRadius="45"
        Padding="25">
    <Grid Background="White" ShowGridLines="True">
      <Grid.ColumnDefinitions>
        <ColumnDefinition Width="Auto"/>
        <ColumnDefinition Width="*"/>
        <ColumnDefinition Width="Auto"/>
      </Grid.ColumnDefinitions>

    <StackPanel Grid.Column="0" Grid.Row="0"
                HorizontalAlignment="Left"
                Name="StackPanel1"
                VerticalAlignment="Top">
        <TextBlock FontSize="18" HorizontalAlignment="Center" Margin="0,0,0,15">StackPanel1</TextBlock>
        <Button Margin="0,10,0,10">Button 1</Button>
        <Button Margin="0,10,0,10">Button 2</Button>
        <Button Margin="0,10,0,10">Button 3</Button>
        <TextBlock>ColumnDefinition.Width="Auto"</TextBlock>
        <TextBlock>StackPanel.HorizontalAlignment="Left"</TextBlock>
        <TextBlock>StackPanel.VerticalAlignment="Top"</TextBlock>
        <TextBlock>StackPanel.Orientation="Vertical"</TextBlock>
        <TextBlock>Button.Margin="0,10,0,10"</TextBlock>
    </StackPanel>

    <StackPanel Grid.Column="1" Grid.Row="0"
                HorizontalAlignment="Stretch"
                Name="StackPanel2"
                VerticalAlignment="Top"
                Orientation="Vertical">
        <TextBlock FontSize="18" HorizontalAlignment="Center" Margin="0,0,0,15">StackPanel2</TextBlock>
        <Button Margin="10,0,10,0">Button 4</Button>
        <Button Margin="10,0,10,0">Button 5</Button>
        <Button Margin="10,0,10,0">Button 6</Button>
        <TextBlock HorizontalAlignment="Center">ColumnDefinition.Width="*"</TextBlock>
        <TextBlock HorizontalAlignment="Center">StackPanel.HorizontalAlignment="Stretch"</TextBlock>
        <TextBlock HorizontalAlignment="Center">StackPanel.VerticalAlignment="Top"</TextBlock>
        <TextBlock HorizontalAlignment="Center">StackPanel.Orientation="Horizontal"</TextBlock>
        <TextBlock HorizontalAlignment="Center">Button.Margin="10,0,10,0"</TextBlock>
    </StackPanel>

    <StackPanel Grid.Column="2" Grid.Row="0"
                HorizontalAlignment="Left"
                Name="StackPanel3"
                VerticalAlignment="Top">
        <TextBlock FontSize="18" HorizontalAlignment="Center" Margin="0,0,0,15">StackPanel3</TextBlock>
        <Button Margin="10">Button 7</Button>
        <Button Margin="10">Button 8</Button>
        <Button Margin="10">Button 9</Button>
        <TextBlock>ColumnDefinition.Width="Auto"</TextBlock>
        <TextBlock>StackPanel.HorizontalAlignment="Left"</TextBlock>
        <TextBlock>StackPanel.VerticalAlignment="Top"</TextBlock>
        <TextBlock>StackPanel.Orientation="Vertical"</TextBlock>
        <TextBlock>Button.Margin="10"</TextBlock>
    </StackPanel>
  </Grid>
</Border>
```

编译之后，上面这个应用呈现出的界面如下图所示。各属性取值的效果从元素之间的间距上一目了然，每一列中元素的关键属性值则写在 `TextBlock` 元素里。

<Image light={LayoutMarginsPaddingAlignmentComplexAnnotatedScreenshot} alt="Several positioning properties in one application" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [布局](/docs/layout)：测量与排列机制的工作方式。
- [如何挑选布局面板](/docs/layout/choosing-a-layout-panel)：为你的场景选对面板。
