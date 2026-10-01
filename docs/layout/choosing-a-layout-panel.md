---
id: choosing-a-layout-panel
title: 如何挑选布局面板
description: 对比 Avalonia 的各个面板控件，为你的布局策略挑出最合适的那一个。
doc-type: how-to
---

Avalonia 提供了多种布局面板，各自承担不同的界面职责。本文帮你为心中的布局策略选出最合适的面板控件。

## 决策流程 {#decision-flowchart}

1. 需要尺寸各异的行与列？**请用 [Grid](#grid)**。
2. 需要在内容区周围放页眉、页脚或侧边栏？**请用 [DockPanel](#dockpanel)**。
3. 需要把元素沿单一方向依次排开？**请用 [StackPanel](#stackpanel)**。
4. 需要在空间不够时自动换行？**请用 [WrapPanel](#wrappanel)**。
5. 需要大小一致的均匀网格？**请用 [UniformGrid](#uniformgrid)**。
6. 需要让元素相对彼此定位？**请用 [RelativePanel](#relativepanel)**。
7. 需要精确到像素的绝对定位？**请用 [Canvas](#canvas)**。
8. 需要把子元素层层叠放？**请用 [Panel](#panel)**。

## 速查对比 {#quick-comparison}

| 面板 | 排布方式 | 是否随窗口尺寸自适应 | 适用场景 |
|---|---|---|---|
| [Grid](/controls/layout/panels/grid) | 行与列 | Yes | 绝大多数通用布局、表单、仪表板 |
| [DockPanel](/controls/layout/panels/dockpanel) | 贴边（上、下、左、右）加填充 | Yes | 带页眉、侧边栏和内容区的应用外壳 |
| [StackPanel](/controls/layout/panels/stackpanel) | 单行或单列（纵向或横向） | 部分支持（垂直方向拉伸，沿排布方向可滚动） | 工具栏、菜单、一串简单控件 |
| [WrapPanel](/controls/layout/panels/wrappanel) | 顺序排列并自动换行 | Yes | 标签云、图标网格、随空间自适应的条目集合 |
| [UniformGrid](/controls/layout/panels/uniformgrid) | 大小相等的单元格 | Yes | 计算器键盘、图片画廊、等大磁贴的仪表板 |
| [RelativePanel](/controls/layout/panels/relativepanel) | 相对于兄弟元素或面板边缘 | Yes | 随可用空间重新编排的自适应布局 |
| [Canvas](/controls/layout/panels/canvas) | 绝对坐标 | No | 绘图画布、示意图、自定义覆盖层 |
| [Panel](/controls/layout/panels/panel) | 彼此叠放 | Yes | 覆盖层，在同一位置堆叠视觉元素 |

## Grid

一个用途广泛的面板，适合许多常见布局。可以定义固定尺寸、按比例（`*`）或自动（`Auto`）的行与列，再把子元素放进指定的单元格。

<XamlPreview>

```xml
<Grid xmlns="https://github.com/avaloniaui"
      ColumnDefinitions="100,*"
      RowDefinitions="Auto,*"
      ShowGridLines="true">
    <TextBlock Grid.Row="0" Grid.Column="0" Text="Label" />
    <TextBox Grid.Row="0" Grid.Column="1" />
    <Button Grid.Row="1" Grid.Column="0" Grid.ColumnSpan="2" HorizontalAlignment="Center">
      Button spanning two columns
    </Button>
</Grid>
```

</XamlPreview>

**适用于：** 需要行列尺寸各异的结构化布局，比如表单、仪表板，或任何固定区域与弹性区域混排的布局。

**不适用于：** 所有子元素只需沿一个方向排开（请改用 [`StackPanel`](#stackpanel)）；所有单元格大小一致（请改用 [`UniformGrid`](#uniformgrid)）。另外 `Grid` 比简单面板更重，用不上 `Grid` 那套复杂能力时，请选更轻量的面板。

更多内容请见 [Grid](/controls/layout/panels/grid) 页面。

## DockPanel

把子元素停靠到面板的各条边上，最后一个子元素填满剩余空间。

<XamlPreview>

```xml
<DockPanel xmlns="https://github.com/avaloniaui">

    <Menu DockPanel.Dock="Top" Background="Gray">
      <MenuItem Header="_File" />
      <MenuItem Header="_Edit" />
    </Menu>

    <TextBlock DockPanel.Dock="Bottom" Background="Lime" Text="Ready" />

    <StackPanel DockPanel.Dock="Right" Width="100">
      <Button Content="Zoom in" />
      <Button Content="Zoom out" />
    </StackPanel>

    <ContentControl Background="Beige" />  <!-- fills remaining space -->

</DockPanel>
```

</XamlPreview>

**适用于：** 构建应用外壳 —— 中间是内容区，周围有固定的页眉、页脚和/或侧边栏。

**不适用于：** 需要子元素按比例分享空间时（请改用 [`Grid`](#grid)）。`DockPanel` 优先满足先声明的子元素。

更多内容请见 [DockPanel](/controls/layout/panels/dockpanel) 页面。

## StackPanel

把子元素排成一行（横向）或一列（纵向，默认）。子元素在垂直于排布的方向上拉伸填满。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Spacing="8">
    <TextBlock Text="Name" />
    <TextBox />
    <TextBlock Text="Email" />
    <TextBox />
    <Button Content="Submit" HorizontalAlignment="Right" />
</StackPanel>
```

</XamlPreview>

**适用于：** 一串简短的线性控件，比如工具栏、设置表单或菜单。

**不适用于：** 条目很多、超出可用空间的场合。`StackPanel` 给子元素的空间是无限的，并不会触发滚动。可以考虑把它套进 `ScrollViewer`，或者改用带虚拟化的 `ItemsControl`。

更多内容请见 [StackPanel](/controls/layout/panels/stackpanel) 页面。

## WrapPanel

把子元素从左到右（或从上到下）排布，碰到边缘就换到下一行。

<XamlPreview>

```xml
<WrapPanel xmlns="https://github.com/avaloniaui" 
           ItemSpacing="8" LineSpacing="8">
    <Button Content="One" />
    <Button Content="Two" />
    <Button Content="Three" />
    <Button Content="Four" />
    <Button Content="Five" />
</WrapPanel>
```

</XamlPreview>

**适用于：** 希望条目随可用空间自动流动的场合，比如标签、缩略图或可自适应的按钮栏。

**不适用于：** 需要条目严格对齐的场合。`WrapPanel` 中不同行的条目各自独立排布，不会对齐成整齐的列。

更多内容请见 [WrapPanel](/controls/layout/panels/wrappanel) 页面。

## UniformGrid

把可用空间等分成若干单元格，子元素依次填入。

<XamlPreview>

```xml
<UniformGrid xmlns="https://github.com/avaloniaui" 
             Columns="3">
    <Button Content="7" />
    <Button Content="8" />
    <Button Content="9" />
    <Button Content="4" />
    <Button Content="5" />
    <Button Content="6" />
    <Button Content="1" />
    <Button Content="2" />
    <Button Content="3" />
</UniformGrid>
```

</XamlPreview>

**适用于：** 所有条目大小一致的场合，比如计算器键盘、调色板，或等大磁贴的仪表板。

**不适用于：** 条目尺寸各异的场合（请改用 [`Grid`](#grid)）。

更多内容请见 [UniformGrid](/controls/layout/panels/uniformgrid) 页面。

## RelativePanel

用附加属性，把子元素相对于兄弟控件或面板边缘定位。

<XamlPreview>

```xml
<RelativePanel xmlns="https://github.com/avaloniaui">
    <TextBlock Name="TitleText" Text="Title"
               RelativePanel.AlignTopWithPanel="True"
               RelativePanel.AlignLeftWithPanel="True" />
    <TextBox Name="SearchBox"
             RelativePanel.Below="TitleText"
             RelativePanel.AlignLeftWith="TitleText"
             RelativePanel.AlignRightWithPanel="True"
             Margin="0,8,0,0" />
    <Button Content="Search"
            RelativePanel.Below="SearchBox"
            RelativePanel.AlignRightWithPanel="True"
            Margin="0,8,0,0" />
</RelativePanel>
```

</XamlPreview>

**适用于：** 需要描述控件之间的布局关系时，比如「把这个按钮放在那个文本框下面，并靠右对齐」。对于需要随可用空间调整关系的自适应布局，它尤其好用。

**不适用于：** 更简单的面板就能搞定你的布局时。`RelativePanel` 虽灵活但啰嗦 —— 若 [`Grid`](#grid) 或 [`StackPanel`](#stackpanel) 就能胜任，请优先用它们。

更多内容请见 [RelativePanel](/controls/layout/panels/relativepanel) 页面。

## Canvas

用 `Canvas.Left`、`Canvas.Top`、`Canvas.Right` 和 `Canvas.Bottom` 把子元素放在精确的像素坐标上。

<XamlPreview>

```xml
<Canvas xmlns="https://github.com/avaloniaui">
    <Ellipse Canvas.Left="50" Canvas.Top="30"
             Width="80" Height="80" Fill="Blue" />
    <Rectangle Canvas.Left="150" Canvas.Top="60"
               Width="100" Height="50" Fill="Red" />
</Canvas>
```

</XamlPreview>

**适用于：** 绘图画布或示意图这类需要绝对定位的场合；或者需要把对象拖放到指定坐标的交互界面。

**不适用于：** 构建常规的应用界面。`Canvas` 不会随窗口缩放自适应，窗口尺寸一变，内容就可能被裁掉或者留下空白。

更多内容请见 [Canvas](/controls/layout/panels/canvas) 页面。

## Panel

一个极简容器，按声明顺序把子元素层层叠放。用 `ZIndex` 控制哪个子元素显示在最上层。

<XamlPreview>

```xml
<Panel xmlns="https://github.com/avaloniaui">
    <ContentControl Name="BG" Background="Gray" />
    <TextBlock Text="Overlay text"
                HorizontalAlignment="Center"
                VerticalAlignment="Center" />
</Panel>
```

</XamlPreview>

**适用于：** 想把一个控件叠在另一个之上，比如图片上的水印、内容之上的加载指示器。

**不适用于：** 希望子元素并排或依次排列的场合。

更多内容请见 [Panel](/controls/layout/panels/panel) 页面。

## 面板的嵌套 {#nesting-panels}

复杂布局可以多种面板混用：把面板一层层嵌套起来，每一层都挑最简单的那个。

<XamlPreview>

```xml
<DockPanel xmlns="https://github.com/avaloniaui">

    <!-- App shell: header + sidebar + content -->
    <Menu DockPanel.Dock="Top"
          Background="Gray">
      <MenuItem Header="_File" />
      <MenuItem Header="_Edit" />
    </Menu>

    <StackPanel DockPanel.Dock="Left"
                Width="100"
                Spacing="4"
                Background="Navy">
        <!-- Sidebar: vertical list of navigation items -->
        <Button Content="Home" />
        <Button Content="Settings" />
    </StackPanel>

    <Grid RowDefinitions="*,Auto">
        <!-- Content area: main content + status bar -->
        <ContentControl Grid.Row="0" />
        <TextBlock Grid.Row="1" Background="Lime" Text="Ready" />
    </Grid>

</DockPanel>
```

</XamlPreview>

### 性能建议 {#performance-tips}

- 能用简单面板就别用复杂的。[`StackPanel`](#stackpanel) 和 [`Panel`](#panel) 都比 [`Grid`](#grid) 轻。
- 避免面板层层深套。一旦发现自己嵌套超过三层，就该想想：换成单个 [`Grid`](#grid)，配上合适的行列定义，是不是就能替掉整棵树？
- 条目很多的列表请用 `ListBox`，别往 `StackPanel` 里塞一大堆控件。

## 另请参阅 {#see-also}

- [布局](/docs/layout) —— 测量与排列机制的工作方式。
- [控件定位](/docs/layout/positioning-controls) —— 对齐、外边距与内边距。
- [响应式布局指南](/docs/how-to/responsive-layout-how-to) —— 自适应布局的各种技巧。
- 各面板的参考页：
  - [Grid](/controls/layout/panels/grid)
  - [DockPanel](/controls/layout/panels/dockpanel)
  - [StackPanel](/controls/layout/panels/stackpanel)
  - [WrapPanel](/controls/layout/panels/wrappanel)
  - [Canvas](/controls/layout/panels/canvas)
  - [RelativePanel](/controls/layout/panels/relativepanel)
  - [UniformGrid](/controls/layout/panels/uniformgrid)
  - [Panel](/controls/layout/panels/panel).
