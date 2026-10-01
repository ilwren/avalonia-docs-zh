---
id: grid-how-to
title: "操作指南：使用 Grid 布局"
description: 行列定义、尺寸模式、跨行跨列、共享尺寸，以及响应式的 Grid 用法。
doc-type: how-to
---

本指南介绍 [`Grid`](/api/avalonia/controls/grid) 布局的常见场景，包括行列定义、尺寸模式、跨行跨列、共享尺寸和响应式写法。

## 行列定义 {#row-and-column-definitions}

你可以用简写语法定义行和列：

```xml
<Grid ColumnDefinitions="200,*,Auto" RowDefinitions="Auto,*,Auto">
    <TextBlock Grid.Row="0" Grid.Column="0" Text="Sidebar Header" />
    <ListBox Grid.Row="1" Grid.Column="0" />
    <ContentControl Grid.Row="0" Grid.RowSpan="3" Grid.Column="1"
                    Content="{Binding MainContent}" />
    <TextBlock Grid.Row="2" Grid.Column="0" Grid.ColumnSpan="2"
               Text="Status Bar" />
</Grid>
```

若需要对单条定义作更多控制（比如设置 `MinWidth` 或 `MaxWidth`），则改用完整语法：

```xml
<Grid>
    <Grid.ColumnDefinitions>
        <ColumnDefinition Width="200" />
        <ColumnDefinition Width="*" />
        <ColumnDefinition Width="Auto" />
    </Grid.ColumnDefinitions>
    <Grid.RowDefinitions>
        <RowDefinition Height="Auto" />
        <RowDefinition Height="*" />
    </Grid.RowDefinitions>
</Grid>
```

:::tip
简写语法更紧凑，而完整语法让你能给每条定义设上 `MinWidth`、`MaxWidth`、`MinHeight`、`MaxHeight`、`SharedSizeGroup` 等额外属性。
:::

## 尺寸模式 {#sizing-modes}

### 按像素定尺寸 {#pixel-sizing}

以设备无关像素给出固定尺寸：

```xml
<Grid ColumnDefinitions="200,300">
    <!-- Column 0 is exactly 200px, Column 1 is exactly 300px -->
</Grid>
```

当你希望某行某列不论内容多少都保持固定大小时，就用像素尺寸。侧边栏、工具栏和图标列常常这么写。

### 自动尺寸 {#auto-sizing}

让行或列的尺寸随内容而定：

```xml
<Grid ColumnDefinitions="Auto,*">
    <!-- Column 0 shrinks to fit its content -->
    <TextBlock Grid.Column="0" Text="Label:" />
    <!-- Column 1 fills remaining space -->
    <TextBox Grid.Column="1" Text="{Binding Value}" />
</Grid>
```

:::note
`Auto` 的行或列会测量全部子元素，并撑到足以容纳最大的那个。若内容会动态变长（比如运行时加载的长文本），这一列也会跟着变宽，有可能把其他列挤出屏幕。想给尺寸设上限，可以用完整语法把 `Auto` 与 `MaxWidth` 或 `MaxHeight` 搭配起来。
:::

### 星号尺寸 {#star-sizing}

在 `Auto` 列和像素列都量好之后，按比例分配剩下的空间：

```xml
<Grid ColumnDefinitions="*,2*,*">
    <!-- Column 0: 25% of remaining space (1/4) -->
    <!-- Column 1: 50% of remaining space (2/4) -->
    <!-- Column 2: 25% of remaining space (1/4) -->
</Grid>
```

星号值可以和其他尺寸模式混用。星号的比例只作用于固定列和 `Auto` 列分配完之后剩下的那部分空间：

```xml
<Grid ColumnDefinitions="100,*,2*">
    <!-- Column 0: fixed 100px -->
    <!-- Remaining space split 1:2 between columns 1 and 2 -->
</Grid>
```

### MinWidth 与 MaxWidth 约束 {#minwidth-and-maxwidth-constraints}

用完整语法可以给行列尺寸加上约束：

```xml
<Grid>
    <Grid.ColumnDefinitions>
        <ColumnDefinition Width="*" MinWidth="200" MaxWidth="400" />
        <ColumnDefinition Width="2*" />
    </Grid.ColumnDefinitions>
</Grid>
```

这对星号列尤其有用——你既想要弹性尺寸，又不希望它窄得没法看或宽得离谱。行也一样，换成 `MinHeight` 和 `MaxHeight` 即可。

## 行间距与列间距 {#row-and-column-spacing}

用 `RowSpacing` 和 `ColumnSpacing` 为行列之间加上均匀的间距：

```xml
<Grid ColumnDefinitions="*,*,*" RowDefinitions="Auto,Auto,Auto"
      ColumnSpacing="8" RowSpacing="8">
    <!-- 8px gap between all rows and columns -->
</Grid>
```

:::note
`RowSpacing` 和 `ColumnSpacing` 只在单元格之间加空隙，不会在网格的外缘留白。若需要外侧留白，请在 `Grid` 本身上设置 `Margin` 或 `Padding`。
:::

## 跨行与跨列 {#spanning-rows-and-columns}

用 `Grid.RowSpan` 和 `Grid.ColumnSpan` 让控件横跨多行或多列：

```xml
<Grid ColumnDefinitions="200,*" RowDefinitions="Auto,*,Auto">
    <!-- Header spans both columns -->
    <TextBlock Grid.Row="0" Grid.ColumnSpan="2" Text="Header"
               FontSize="20" FontWeight="Bold" />

    <!-- Sidebar spans rows 1 and 2 -->
    <ListBox Grid.Row="1" Grid.Column="0" Grid.RowSpan="2" />

    <!-- Content area -->
    <ContentControl Grid.Row="1" Grid.Column="1" />

    <!-- Footer in column 1 only -->
    <TextBlock Grid.Row="2" Grid.Column="1" Text="Footer" />
</Grid>
```

:::tip
`Grid.RowSpan` 和 `Grid.ColumnSpan` 的默认值都是 `1`。若你给出的跨度大于剩余的行数或列数，控件会一直铺到网格边缘，并不会报错。
:::

## 行列的默认值 {#default-row-and-column-values}

子控件上若省略 `Grid.Row` 或 `Grid.Column`，两者都默认为 `0`。也就是说，往 `Grid` 里放单个子元素时，一个附加属性都不用写：

```xml
<Grid>
    <!-- This control is placed at Row 0, Column 0 by default -->
    <TextBlock Text="Hello" />
</Grid>
```

如果你压根没定义 `RowDefinitions` 或 `ColumnDefinitions`，网格就会创建一行一列、均为星号尺寸，填满全部可用空间。

## 表单布局 {#form-layout}

标签配输入框是个常见套路：标签用 `Auto` 列，输入框用星号列：

```xml
<Grid ColumnDefinitions="Auto,*" RowDefinitions="Auto,Auto,Auto,Auto"
      RowSpacing="8" ColumnSpacing="12">
    <TextBlock Grid.Row="0" Grid.Column="0" Text="Name:"
               VerticalAlignment="Center" />
    <TextBox Grid.Row="0" Grid.Column="1" Text="{Binding Name}" />

    <TextBlock Grid.Row="1" Grid.Column="0" Text="Email:"
               VerticalAlignment="Center" />
    <TextBox Grid.Row="1" Grid.Column="1" Text="{Binding Email}" />

    <TextBlock Grid.Row="2" Grid.Column="0" Text="Department:"
               VerticalAlignment="Center" />
    <ComboBox Grid.Row="2" Grid.Column="1" ItemsSource="{Binding Departments}"
              SelectedItem="{Binding Department}" />

    <StackPanel Grid.Row="3" Grid.Column="1" Orientation="Horizontal"
                Spacing="8" HorizontalAlignment="Right">
        <Button Content="Cancel" Command="{Binding CancelCommand}" />
        <Button Content="Save" Command="{Binding SaveCommand}" />
    </StackPanel>
</Grid>
```

给标签设上 `VerticalAlignment="Center"`，即便输入控件比标签高，二者在垂直方向上也能对齐。

## SharedSizeGroup

用 `SharedSizeGroup` 可以让多个 `Grid` 控件的列宽（或行高）对齐。把这个属性设在各个 `ColumnDefinition` 或 `RowDefinition` 元素上：

```xml
<StackPanel Grid.IsSharedSizeScope="True" Spacing="4">
    <Grid ShowGridLines="False">
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="Auto" SharedSizeGroup="Labels" />
            <ColumnDefinition Width="*" />
        </Grid.ColumnDefinitions>
        <TextBlock Grid.Column="0" Text="Name:" Margin="0,0,8,0" />
        <TextBox Grid.Column="1" Text="{Binding Name}" />
    </Grid>
    <Grid ShowGridLines="False">
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="Auto" SharedSizeGroup="Labels" />
            <ColumnDefinition Width="*" />
        </Grid.ColumnDefinitions>
        <TextBlock Grid.Column="0" Text="Email Address:" Margin="0,0,8,0" />
        <TextBox Grid.Column="1" Text="{Binding Email}" />
    </Grid>
</StackPanel>
```

两个「Labels」列虽然分属不同的 `Grid` 控件，却共享同一宽度（即较宽那个标签的宽度）。父级 `StackPanel` 通过设置 `Grid.IsSharedSizeScope="True"` 划定了共享的范围。

:::note
`SharedSizeGroup` 是 `ColumnDefinition` 和 `RowDefinition` 上的属性，而不是子控件上的。组名是个字符串，同一共享尺寸范围内、组名相同的所有定义都会采用同一个测量结果。
:::

## 嵌套网格 {#nested-grids}

布局复杂时，你可以把网格一层层嵌起来。每个内层 `Grid` 都独立管理自己的行和列：

```xml
<Grid ColumnDefinitions="250,*">
    <!-- Sidebar -->
    <Grid Grid.Column="0" RowDefinitions="Auto,*,Auto">
        <TextBlock Grid.Row="0" Text="Navigation" FontWeight="Bold" />
        <ListBox Grid.Row="1" ItemsSource="{Binding MenuItems}" />
        <Button Grid.Row="2" Content="Settings" />
    </Grid>

    <!-- Main content -->
    <Grid Grid.Column="1" RowDefinitions="Auto,*">
        <TextBlock Grid.Row="0" Text="{Binding Title}" FontSize="24" />
        <ContentControl Grid.Row="1" Content="{Binding CurrentPage}" />
    </Grid>
</Grid>
```

:::tip
嵌套网格写起来不难，但会抬高布局的复杂度。若内层网格要的只是简单的纵向或横向排列，不妨改用 `StackPanel` 或 `DockPanel`，可读性和性能都更好。
:::

## 用 Grid 做响应式布局 {#responsive-layout-with-grid}

你可以把 `Grid` 与 `OnFormFactor` 结合起来，按设备调整列定义，做出响应式设计：

```xml
<Grid ColumnDefinitions="{OnFormFactor Desktop='250,*', Mobile='*'}">
    <!-- On desktop: two-column layout -->
    <!-- On mobile: single column (sidebar hidden or placed in a drawer) -->
</Grid>
```

## 内容叠放 {#overlapping-content}

当你把多个子元素放进同一个单元格时，它们在视觉上会互相重叠，标记中写在最后的那个显示在最上面：

```xml
<Grid>
    <!-- Background image -->
    <Image Source="background.jpg" Stretch="UniformToFill" />

    <!-- Overlay gradient -->
    <Border>
        <Border.Background>
            <LinearGradientBrush StartPoint="0%,0%" EndPoint="0%,100%">
                <GradientStop Color="Transparent" Offset="0.5" />
                <GradientStop Color="#CC000000" Offset="1.0" />
            </LinearGradientBrush>
        </Border.Background>
    </Border>

    <!-- Text on top -->
    <TextBlock Text="Hello World"
               VerticalAlignment="Bottom"
               Margin="16"
               Foreground="White"
               FontSize="24" />
</Grid>
```

省略 `Grid.Row` 和 `Grid.Column` 时，子元素默认落在第 0 行第 0 列。你可以用 `ZIndex` 来控制堆叠顺序，不必受书写顺序摆布：

```xml
<Grid>
    <Border ZIndex="1" Background="Red" Opacity="0.5" />
    <Border ZIndex="2" Background="Blue" Opacity="0.5" />
    <!-- Blue border appears on top despite any markup order changes -->
</Grid>
```

### 用负外边距实现部分重叠 {#partial-overlap-with-negative-margins}

若想让两个元素按指定的量重叠、又不把它们塞进同一个单元格，可以给第二个元素设一个负外边距：

```xml
<StackPanel Orientation="Horizontal">
    <Border Background="LightBlue" Padding="12">
        <TextBlock Text="First" />
    </Border>
    <Border Background="LightCoral" Padding="12" Margin="-10,0,0,0">
        <TextBlock Text="Second (overlaps by 10px)" />
    </Border>
</StackPanel>
```

负的左外边距把第二个元素往左拉了 10 像素，于是压在第一个元素上。它显示在上层，是因为它在标记中写得更靠后。这一招在任何面板里都管用，不限于 `Grid`。

## 调试网格布局 {#debugging-grid-layouts}

开发阶段给 `Grid` 设上 `ShowGridLines="True"`，就能看清行列的边界：

```xml
<Grid ColumnDefinitions="Auto,*,200" RowDefinitions="Auto,*"
      ShowGridLines="True">
    <!-- Grid lines appear as dashed lines so you can see each cell -->
</Grid>
```

记得在发布应用前去掉 `ShowGridLines`——它只是个开发期的辅助手段。

## 另请参阅 {#see-also}

- [Grid 控件参考](/controls/layout/panels/grid)
- [布局概述](/docs/layout)
- [摆放控件](/docs/layout/positioning-controls)
