---
id: expander
title: Expander
description: 一个容器控件：标题始终可见，内容区则可以折叠，随手一点即可展开或收起。
doc-type: reference
---

[`Expander`](/api/avalonia/controls/expander) 控件有一个始终可见的标题区，以及一个可折叠的内容区，后者可以放一个子控件。用户点击标题即可切换内容的显示与隐藏。当你想让用户在不离开当前视图的前提下自行展开或收起补充信息（比如搜索筛选、高级设置、选填字段）时，它正合适。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
|---|---|---|
| `Header` | `object` | 显示在始终可见的标题区中的内容，可以是字符串、控件或数据模板。 |
| `IsExpanded` | `bool` | 内容区当前是否可见，默认值为 `false`。 |
| [`ExpandDirection`](/api/avalonia/controls/expanddirection) | `ExpandDirection` | 内容展开的方向：`Down`（默认）、`Up`、`Left` 或 `Right`。 |
| `ContentTransition` | `IPageTransition` | 内容展开或折叠时播放的过渡动画。 |

## 事件 {#events}

| 事件 | 说明 |
|---|---|
| `Expanding` | 内容区开始展开时引发。 |
| `Collapsed` | 内容区折叠完毕时引发。 |

## 基本示例 {#basic-example}

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             Padding="5">
  <Expander VerticalAlignment="Top">
      <Expander.Header>
          Hidden Search
      </Expander.Header>
      <Grid RowDefinitions="*,*" ColumnDefinitions="150,*">
        <TextBlock Grid.Row="0" Grid.Column="0"
                   VerticalAlignment="Center">Search</TextBlock>
        <TextBox Grid.Row="0" Grid.Column="1"
                 PlaceholderText="Search text" Width="200" />
        <TextBlock Grid.Row="1" Grid.Column="0"
                   VerticalAlignment="Center">Case sensitive?</TextBlock>
        <CheckBox Grid.Row="1" Grid.Column="1" />
      </Grid>
  </Expander>
</UserControl>
```

</XamlPreview>

## 初始即展开 {#initially-expanded}

把 `IsExpanded` 设为 `True`，控件首次加载时就会显示内容：

```xml
<Expander Header="Details" IsExpanded="True">
    <TextBlock Text="This content is visible by default." TextWrapping="Wrap" />
</Expander>
```

## 展开方向 {#expand-direction}

设置 `ExpandDirection` 即可控制内容区从哪个方向展开。默认是 `Down`，也可以用 `Up`、`Left` 或 `Right`：

```xml
<Expander ExpandDirection="Up" Header="Expand Upward" VerticalAlignment="Bottom">
    <TextBlock Text="Content above the header" />
</Expander>
```

用 `Left` 或 `Right` 时，标题会旋转，内容横向展开。做侧边面板或工具抽屉时很好用。

## 自定义标题内容 {#custom-header-content}

`Header` 属性接受任意内容，不限于字符串。你可以借此做出带图标、徽标或其他控件的丰富标题：

```xml
<Expander>
    <Expander.Header>
        <StackPanel Orientation="Horizontal" Spacing="8">
            <PathIcon Data="{StaticResource settings_regular}" Width="16" />
            <TextBlock Text="Settings" VerticalAlignment="Center" />
        </StackPanel>
    </Expander.Header>
    <StackPanel Spacing="8" Margin="8">
        <CheckBox Content="Enable notifications" />
        <CheckBox Content="Auto-save" />
    </StackPanel>
</Expander>
```

## Binding `IsExpanded`

把展开状态绑定到视图模型的属性，就能在代码中控制它，随时展开或收起内容区：

```xml
<Expander Header="Advanced" IsExpanded="{Binding ShowAdvanced}">
    <TextBox PlaceholderText="Custom path" />
</Expander>
```

```csharp
public class MyViewModel : ViewModelBase
{
    private bool _showAdvanced;

    public bool ShowAdvanced
    {
        get => _showAdvanced;
        set => this.RaiseAndSetIfChanged(ref _showAdvanced, value);
    }
}
```

## 内容过渡 {#content-transition}

展开和折叠动作可以配上页面过渡动画。设置 `ContentTransition` 属性即可控制动画效果：

```xml
<Expander Header="Animated Section">
    <Expander.ContentTransition>
        <CrossFade Duration="0:0:0.2" />
    </Expander.ContentTransition>
    <TextBlock Text="Fades in and out" />
</Expander>
```

## 嵌套 Expander {#nesting-expanders}

`Expander` 控件可以嵌套，从而做出可折叠的层级结构：把内层 `Expander` 放进外层的内容区即可：

```xml
<Expander Header="General Settings" IsExpanded="True">
    <StackPanel Spacing="8" Margin="8">
        <CheckBox Content="Enable dark mode" />
        <Expander Header="Advanced">
            <StackPanel Spacing="8" Margin="8">
                <CheckBox Content="Hardware acceleration" />
                <CheckBox Content="Verbose logging" />
            </StackPanel>
        </Expander>
    </StackPanel>
</Expander>
```

:::tip
嵌套 expander 时，层级尽量浅（最多两层），免得用户眼花缭乱。
:::

## 无障碍 {#accessibility}

`Expander` 通过它的 `ExpanderAutomationPeer` 内置了无障碍支持。屏幕阅读器会把它报告为可展开/可折叠控件，并播报当前状态。展开和折叠动作通过 `IExpandCollapseProvider` 模式暴露给辅助技术，用户不用指针也能切换内容。

为了让应用更易用，请把 `Header` 设成一个有意义的标签，好让屏幕阅读器说清每个可折叠区块的用途。

## 另请参阅 {#see-also}

- [Expander API 参考](/api/avalonia/controls/expander)
- [GitHub 上的 `Expander.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Expander.cs)
- [SplitView](/controls/layout/containers/splitview)
- [GroupBox](/controls/layout/containers/groupbox)
