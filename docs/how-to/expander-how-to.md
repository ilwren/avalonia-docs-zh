---
id: expander-how-to
title: "操作指南：使用 Expander"
description: 学会用 Avalonia 的 Expander 控件做可折叠内容区、手风琴式面板、带动画的展开、状态绑定与自定义标题。
doc-type: how-to
---

本指南介绍 [`Expander`](/api/avalonia/controls/expander) 的常见场景，包括基本用法、手风琴式面板、带动画的展开、绑定状态以及自定义标题。

## 基本的 Expander {#basic-expander}

最简单的 `Expander` 就是把你想展示或隐藏的内容，收在一个可点击的标题后面：

```xml
<Expander Header="Advanced Options">
    <StackPanel Spacing="8" Margin="8">
        <CheckBox Content="Enable logging" />
        <CheckBox Content="Verbose output" />
    </StackPanel>
</Expander>
```

`Expander` 只能承载单个子元素。若要放多个控件，请先用 `StackPanel` 或 `Grid` 之类的布局面板把它们包起来。

## 初始即展开 {#initially-expanded}

把 `IsExpanded` 设为 `True`，控件首次加载时内容就是展开可见的：

```xml
<Expander Header="Details" IsExpanded="True">
    <TextBlock Text="This content is visible by default." TextWrapping="Wrap" />
</Expander>
```

:::tip
对于大多数用户一上来就得看到的内容，可以让 `Expander` 默认展开，同时仍允许他们折叠起来腾出空间。
:::

## Binding `IsExpanded`

你可以在视图模型中跟踪展开状态，好让界面其他部分随之响应：

```csharp
[ObservableProperty]
private bool _showAdvanced;
```

```xml
<Expander Header="Advanced" IsExpanded="{Binding ShowAdvanced}">
    <StackPanel Spacing="8">
        <TextBox PlaceholderText="Custom path" />
    </StackPanel>
</Expander>
```

有了这个双向绑定，无论用户何时展开或折叠 `Expander`，视图模型的属性都会保持同步。

## 展开方向 {#expand-direction}

[`ExpandDirection`](/api/avalonia/controls/expanddirection) 属性决定内容相对标题朝哪个方向展开：

```xml
<!-- Expands upward -->
<Expander ExpandDirection="Up" Header="Details" VerticalAlignment="Bottom">
    <TextBlock Text="Content above the header" />
</Expander>

<!-- Expands to the right -->
<Expander ExpandDirection="Right" Header="More">
    <TextBlock Text="Content beside the header" />
</Expander>
```

| 值 | 说明 |
|---|---|
| `Down` | 内容出现在标题下方（默认）。 |
| `Up` | 内容出现在标题上方。 |
| `Left` | 内容出现在标题左侧。 |
| `Right` | 内容出现在标题右侧。 |

:::note
用 `Up` 时，请把 `Expander` 放在父容器的底部（比如配合 `VerticalAlignment="Bottom"`），好让展开的内容有向上生长的空间。`Left` 和 `Right` 同理，只是换成水平方向的对齐。
:::

## 带图标的自定义标题 {#custom-header-with-icon}

用 `Expander.Header` 可以在标题区放入丰富的内容：

```xml
<Expander>
    <Expander.Header>
        <StackPanel Orientation="Horizontal" Spacing="8">
            <PathIcon Data="{StaticResource settings_regular}" Width="16" />
            <TextBlock Text="Settings" VerticalAlignment="Center" />
        </StackPanel>
    </Expander.Header>
    <StackPanel Spacing="8" Margin="8">
        <TextBlock Text="Configuration options here" />
    </StackPanel>
</Expander>
```

由于 `Header` 的类型是 `object`，你可以塞进任意控件树。常见做法有图标配文字、角标，或者状态指示器。

## 手风琴效果（同时只开一个） {#accordion-pattern-single-open}

要让同时只有一个 `Expander` 处于展开状态，请把各个 `IsExpanded` 属性绑定到视图模型中共用的后备字段：

```csharp
public partial class AccordionViewModel : ObservableObject
{
    [ObservableProperty]
    private int _openSection = -1;

    public bool IsSection0Open
    {
        get => OpenSection == 0;
        set { if (value) OpenSection = 0; else if (OpenSection == 0) OpenSection = -1; }
    }

    public bool IsSection1Open
    {
        get => OpenSection == 1;
        set { if (value) OpenSection = 1; else if (OpenSection == 1) OpenSection = -1; }
    }

    public bool IsSection2Open
    {
        get => OpenSection == 2;
        set { if (value) OpenSection = 2; else if (OpenSection == 2) OpenSection = -1; }
    }

    partial void OnOpenSectionChanged(int value)
    {
        OnPropertyChanged(nameof(IsSection0Open));
        OnPropertyChanged(nameof(IsSection1Open));
        OnPropertyChanged(nameof(IsSection2Open));
    }
}
```

```xml
<StackPanel Spacing="4">
    <Expander Header="General" IsExpanded="{Binding IsSection0Open}">
        <TextBlock Text="General content" Margin="8" />
    </Expander>
    <Expander Header="Appearance" IsExpanded="{Binding IsSection1Open}">
        <TextBlock Text="Appearance content" Margin="8" />
    </Expander>
    <Expander Header="Advanced" IsExpanded="{Binding IsSection2Open}">
        <TextBlock Text="Advanced content" Margin="8" />
    </Expander>
</StackPanel>
```

把 `OpenSection` 设为 `-1` 表示所有区块都折叠。用户展开某个区块时，之前展开的那个会自动合上。

## 带动画的内容过渡 {#animated-content-transition}

加上 `ContentTransition`，展开和折叠就有了平滑的动画：

```xml
<Expander Header="Animated Section">
    <Expander.ContentTransition>
        <CrossFade Duration="0:0:0.2" />
    </Expander.ContentTransition>
    <StackPanel Spacing="8" Margin="8">
        <TextBlock Text="This content fades in and out." />
    </StackPanel>
</Expander>
```

你可以把 `CrossFade` 换成 `PageSlide`、`CompositePageTransition` 等别的过渡类型。内置选项的完整清单请参阅[页面过渡](/docs/graphics-animation/page-transitions)。

## 响应展开与折叠事件 {#responding-to-expand-and-collapse-events}

在代码隐藏中订阅 `IsExpandedChanged` 事件，即可处理展开状态的变化：

```csharp
private void Expander_IsExpandedChanged(object sender, RoutedEventArgs e)
{
    if (sender is Expander expander && expander.IsExpanded)
    {
        // Load data when first expanded
    }
}
```

```xml
<Expander Header="Lazy Content"
          PropertyChanged="Expander_IsExpandedChanged" />
```

或者在视图模型里用属性变更回调，不写代码隐藏也能达到同样效果：

```csharp
[ObservableProperty]
private bool _isDetailsOpen;

partial void OnIsDetailsOpenChanged(bool value)
{
    if (value)
        LoadDetails();
}
```

:::tip
对于内容渲染开销很大的 expander，惰性加载是个好办法——等用户真的展开了再干活。
:::

## 为 expander 设置样式 {#styling-the-expander}

### 去掉边框 {#remove-the-border}

你可以把默认的边框和背景抹掉，换一种更素净的观感：

```xml
<Expander.Styles>
    <Style Selector="Expander">
        <Setter Property="BorderThickness" Value="0" />
        <Setter Property="Background" Value="Transparent" />
    </Style>
</Expander.Styles>
```

### 自定义展开图标 {#custom-expand-icon}

重写模板里的切换按钮，即可更换展开/折叠指示符：

```xml
<Expander.Styles>
    <Style Selector="Expander /template/ ToggleButton#PART_toggle">
        <!-- Override the toggle button appearance -->
    </Style>
</Expander.Styles>
```

### 禁用状态 {#disabled-state}

当你给 `Expander` 设上 `IsEnabled="False"` 后，标题就不再可交互，用户也无法切换内容。禁用那一刻的展开/折叠状态会被保留下来。

```xml
<Expander Header="Read-only section" IsEnabled="False" IsExpanded="True">
    <TextBlock Text="This section cannot be collapsed." Margin="8" />
</Expander>
```

## 关键属性速查 {#key-properties-reference}

| 属性 | 类型 | 说明 |
|---|---|---|
| `Header` | `object` | 显示在始终可见的标题区中的内容。 |
| `IsExpanded` | `bool` | 内容区是否可见，默认为 `False`。 |
| `ExpandDirection` | `ExpandDirection` | 内容展开的方向：`Down`、`Up`、`Left`、`Right`，默认为 `Down`。 |
| `ContentTransition` | `IPageTransition` | 展开与折叠所用的动画。 |
| `IsEnabled` | `bool` | 用户能否通过标题来切换展开状态。 |

## 另请参阅 {#see-also}

- [Expander 控件参考](/controls/layout/containers/expander)：完整的属性与事件表。
- [页面过渡](/docs/graphics-animation/page-transitions)：可用于内容动画的各种过渡类型。
- [数据绑定入门](/docs/data-binding/introduction-to-data-binding)：把 `IsExpanded` 这类属性绑定到视图模型的基础知识。
