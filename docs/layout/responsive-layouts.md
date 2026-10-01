---
id: responsive-layouts
title: 响应式布局
description: 借助容器查询、外形规格扩展和自动重排的面板，做出能适应不同尺寸的布局。
doc-type: explanation
---

Avalonia 提供了多种技术，让布局能随可用空间的变化而调整：你可以响应容器的尺寸、设备的类型，或是某个重排面板的尺寸。本文逐一讲解这些做法，以及各自的适用场合。

## 各种做法一览 {#approaches-at-a-glance}

| 技术 | 响应对象 | 生效时机 | 适用场景 |
|-----------|-------------|----------|----------|
| [容器查询](#container-queries) | 某个祖先控件的尺寸 | 实时，随控件尺寸变化 | 会被放进不同宽度面板中的可复用组件 |
| [`OnFormFactor`](#onformfactor) | 设备类型（桌面、移动） | 一次性，在启动时 | 各平台之间的布局差异 |
| [重排面板](#reflowing-panels) | 可用宽度 | 实时，随面板尺寸变化 | 卡片网格与流式内容 |
| [断点视图模型](#breakpoint-view-models) | 窗口宽度（或任何可测量的值） | 实时，通过属性变更 | 由代码驱动、牵涉多个属性的复杂切换 |

## 容器查询 {#container-queries}

容器查询让你在某个祖先控件达到特定尺寸时激活相应样式。由于查询针对的是控件而非窗口，同一个组件无论出现在整宽页面、窄侧边栏还是对话框中，都能正确自适应。

### 声明一个容器 {#declaring-a-container}

设置 `Container.Name` 和 `Container.Sizing` 这两个附加属性，就能把任意祖先标记为容器：

```xml
<Border Container.Name="main"
        Container.Sizing="Width">
    <!-- child content here -->
</Border>
```

`Container.Sizing` 决定跟踪哪些维度：

| 值 | 跟踪的维度 |
|-------|--------------------|
| `Normal` | 无（默认） |
| `Width` | 仅宽度 |
| `Height` | 仅高度 |
| `WidthAndHeight` | 宽度与高度 |

### 编写容器查询 {#writing-a-container-query}

`ContainerQuery` 元素位于容器某个祖先控件的 `Styles` 集合中。查询条件满足时，它就激活自己内部的样式：

```xml
<Window>
    <Window.Styles>
        <ContainerQuery Name="main" Query="max-width:600">
            <Style Selector="StackPanel#sidebar">
                <Setter Property="IsVisible" Value="False" />
            </Style>
        </ContainerQuery>
    </Window.Styles>

    <Grid ColumnDefinitions="200,*">
        <StackPanel x:Name="sidebar" Grid.Column="0">
            <!-- sidebar content -->
        </StackPanel>
        <ContentControl Grid.Column="1"
                        Content="{Binding CurrentPage}" />
    </Grid>
</Window>
```

本例中，当名为 `main` 的容器宽度不超过 600 像素时，侧边栏就隐藏起来。

### 用断点调整布局结构 {#adjusting-layout-structure-with-breakpoints}

可以在同一个容器上写多个容器查询，划分出若干断点档位。下例随着容器变宽，逐级增加 `UniformGrid` 的列数：

```xml
<Panel Container.Name="content" Container.Sizing="Width">
    <Panel.Styles>
        <ContainerQuery Name="content" Query="max-width:400">
            <Style Selector="UniformGrid#cards">
                <Setter Property="Columns" Value="1" />
            </Style>
        </ContainerQuery>
        <ContainerQuery Name="content" Query="min-width:400">
            <Style Selector="UniformGrid#cards">
                <Setter Property="Columns" Value="2" />
            </Style>
        </ContainerQuery>
        <ContainerQuery Name="content" Query="min-width:800">
            <Style Selector="UniformGrid#cards">
                <Setter Property="Columns" Value="3" />
            </Style>
        </ContainerQuery>
    </Panel.Styles>

    <UniformGrid x:Name="cards">
        <!-- card items -->
    </UniformGrid>
</Panel>
```

### 调整布局以外的属性 {#customising-non-layout-properties}

容器查询并不局限于布局属性。凡是 `Style` 能设置的属性，它都能调整，包括字号、间距、可见性和颜色：

```xml
<Panel Container.Name="content" Container.Sizing="Width">
    <Panel.Styles>
        <!-- Default heading size -->
        <Style Selector="TextBlock.heading">
            <Setter Property="FontSize" Value="24" />
        </Style>

        <!-- Smaller heading when the container is narrow -->
        <ContainerQuery Name="content" Query="max-width:500">
            <Style Selector="TextBlock.heading">
                <Setter Property="FontSize" Value="18" />
            </Style>
            <Style Selector="StackPanel.toolbar">
                <Setter Property="Orientation" Value="Vertical" />
            </Style>
        </ContainerQuery>
    </Panel.Styles>

    <StackPanel>
        <TextBlock Classes="heading" Text="Dashboard" />
        <StackPanel Classes="toolbar" Orientation="Horizontal" Spacing="8">
            <Button Content="New" />
            <Button Content="Refresh" />
        </StackPanel>
    </StackPanel>
</Panel>
```

### 组合多个条件 {#combining-queries}

用 `and`（所有条件都要满足）或 `,`（任一条件满足即可）把多个条件组合进同一个查询：

```xml
<!-- Both conditions must be true -->
<ContainerQuery Name="main" Query="min-width:400 and max-width:800">
    <!-- styles for medium widths -->
</ContainerQuery>

<!-- Either condition can be true -->
<ContainerQuery Name="main" Query="max-width:300,min-height:600">
    <!-- styles for narrow OR tall containers -->
</ContainerQuery>
```

完整的查询语法、可用的查询类型以及各项限制，请见[容器查询](/docs/styling/container-queries)。

:::tip
若把 `TopLevel`（你的窗口或主视图）设为容器，容器查询的表现就和 CSS 媒体查询一样 —— 直接响应窗口尺寸。
:::

## OnFormFactor

`OnFormFactor` 标记扩展按设备类型选取取值。它在启动时解析一次，因此不会响应运行时的窗口缩放。

### 外形规格取值 {#form-factor-values}

| 参数 | 匹配 | 典型平台 |
|-----------|---------|-------------------|
| `Desktop` | 桌面系统 | Windows, macOS, Linux |
| `Mobile` | 移动系统 | iOS, Android |
| `TV` | 电视系统 | tvOS, Android TV |
| `Default` | 当前外形规格未被列出时的回退值 | Any |

若当前外形规格与所给的参数都不匹配，就采用 `Default` 的值。如果没有设置 `Default`，该属性则取其类型的默认值。

```xml
<Grid ColumnDefinitions="{OnFormFactor Desktop='250,*', Mobile='*'}">
    <Border Grid.Column="0"
            IsVisible="{OnFormFactor Desktop=True, Mobile=False}">
        <ListBox ItemsSource="{Binding MenuItems}" />
    </Border>
    <ContentControl Grid.Column="{OnFormFactor Desktop=1, Mobile=0}"
                    Content="{Binding CurrentPage}" />
</Grid>
```

当桌面与移动端的布局在结构上就不一样、且无需响应实时缩放时，用 `OnFormFactor` 正合适。若布局必须随用户缩放窗口而调整，请改用容器查询。

### OnPlatform

与之相关的 `OnPlatform` 标记扩展，是按操作系统而非设备类型来选取取值，同样在启动时解析一次。

| 参数 | 匹配 |
|-----------|---------|
| `Windows` | Windows |
| `macOS` | macOS |
| `Linux` | Linux |
| `iOS` | iOS |
| `Android` | Android |
| `Browser` | 浏览器中的 WebAssembly（WASM） |
| `Default` | 当前平台未被列出时的回退值 |

```xml
<TextBlock FontFamily="{OnPlatform macOS='San Francisco',
                                   Windows='Segoe UI',
                                   Default='Inter'}" />
```

`OnFormFactor` 和 `OnPlatform` 用途不同。设备类别（桌面与移动）之间的结构性布局差异，用 `OnFormFactor`；而原生字体族、特定系统的样式之类平台专有的调整，则用 `OnPlatform`。

## 重排面板 {#reflowing-panels}

有些面板会根据可用空间自动重排子元素，让你不必显式设断点也能做出流式内容。

例如 `WrapPanel` 把子元素排成一行，碰到面板边缘就自动换到下一行：

<XamlPreview>

```xml
<WrapPanel xmlns="https://github.com/avaloniaui"
           Orientation="Horizontal">
    <Button Content="One" Margin="4" />
    <Button Content="Two" Margin="4" />
    <Button Content="Three" Margin="4" />
    <Button Content="Four" Margin="4" />
    <Button Content="Five" Margin="4" />
    <Button Content="Six" Margin="4" />
    <!-- Wraps to the next row when the panel is too narrow -->
</WrapPanel>
```

</XamlPreview>

## 断点视图模型 {#breakpoint-view-models}

当你的响应式逻辑牵涉多个属性的协同变化、或者超出尺寸之外的条件（比如要同时判断屏幕方向和平台）时，可以在视图模型中观察窗口宽度，并为每个档位暴露一个布尔属性：

```csharp
public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private bool _isCompact;

    [ObservableProperty]
    private bool _isWide;

    public void UpdateLayout(double windowWidth)
    {
        IsCompact = windowWidth < 640;
        IsWide = windowWidth >= 1024;
    }
}
```

在窗口的尺寸变化处理程序中调用 `UpdateLayout`：

```csharp
protected override void OnSizeChanged(SizeChangedEventArgs e)
{
    base.OnSizeChanged(e);
    if (DataContext is MainViewModel vm)
        vm.UpdateLayout(e.NewSize.Width);
}
```

然后把布局属性绑定到这些断点标志上：

```xml
<StackPanel IsVisible="{Binding IsCompact}" Spacing="8">
    <views:SidebarView />
    <views:ContentView />
</StackPanel>

<Grid IsVisible="{Binding !IsCompact}" ColumnDefinitions="280,*">
    <views:SidebarView Grid.Column="0" />
    <views:ContentView Grid.Column="1" />
</Grid>
```

这种做法可以完全由代码掌控，但需要写代码隐藏或视图模型接线。若切换逻辑纯粹由尺寸决定、且能在 XAML 中表达，还是优先用容器查询。

## 该选哪种办法 {#choosing-an-approach}

按下面的思路来挑选合适的技术：

1. **组件需要根据自身（而非窗口）的尺寸自适应？** 用容器查询。这样组件自成一体，也便于复用。
2. **桌面与移动端布局在结构上就不同，且不需要响应实时缩放？** 用 `OnFormFactor`。
3. **有一组条目需要自动排成多行？** 用 `WrapPanel` 或 `UniformGridLayout`。
4. **切换逻辑牵涉多个条件、平台判断，或尺寸以外的触发因素？** 用断点视图模型。

这些技术可以混用。例如先用 `OnFormFactor` 处理顶层的结构差异（侧边栏还是底部标签页），再在各个面板内部用容器查询，让它们随实际渲染尺寸自适应。

## 另请参阅 {#see-also}

- [容器查询](/docs/styling/container-queries)：完整的查询语法、容器尺寸模式与各项限制。
- [如何构建响应式布局](/docs/how-to/responsive-layout-how-to)：常见响应式套路的分步实践。
- [布局](/docs/layout)：Avalonia 测量与排列机制的工作方式。
- [如何挑选布局面板](/docs/layout/choosing-a-layout-panel)：为你的场景选对面板。
- [`OnFormFactorExtension` API 参考](/api/avalonia/markup/xaml/markupextensions/onformfactorextension)
- [`OnPlatformExtension` API 参考](/api/avalonia/markup/xaml/markupextensions/onplatformextension)
