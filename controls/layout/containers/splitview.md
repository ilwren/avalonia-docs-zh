---
id: splitview
title: SplitView
description: 了解如何用 SplitView 控件在 Avalonia UI 中做出可折叠的侧边面板和导航侧栏。
doc-type: reference
---

import SplitViewCompactScreenshot from '/img/controls/splitview/splitview-expander.gif';

`SplitView` 呈现的容器分为两部分：主内容区和侧边面板。主内容区始终可见，面板则可以展开和收起。收起后的面板既可以完全隐藏，也可以留出一条缝——比如刚好放得下几个图标按钮。 

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性            | 说明                                                                      |
| ------------------- | -------------------------------------------------------------------------------- |
| `PanePlacement`     | 设置面板的位置：`Left`、`Right`、`Top` 或 `Bottom`。              |
| `IsPaneOpen`        | 布尔值，默认为 true。面板是否处于展开状态？                         |
| `DisplayMode`       | 控制面板在展开和收起两种状态下如何绘制，详见下文。         |
| `OpenPaneLength`    | 面板展开时的宽度（上下放置时则为高度）。        |
| `CompactPaneLength` | 面板收起、且显示模式为紧凑时的宽度（上下放置时则为高度）。 |

显示模式属性控制面板在展开和收起两种状态下如何绘制，共有四个选项：

*   **Overlay**

    面板在展开之前完全隐藏；展开时覆盖在内容区之上。
*   **Inline**

    面板始终可见、宽度固定，且不覆盖内容区。面板和内容区分享可用的屏幕空间；容器宽度变化时，被调整的是内容区。
*   **Compact Overlay**

    此模式下面板始终露出窄窄的一条，刚好放得下图标。收起时的默认宽度为 48px，可用 `CompactPaneLength` 属性修改。面板展开时会覆盖在内容区之上。
*   **Compact Inline**

    此模式下面板始终露出窄窄的一条，刚好放得下图标。收起时的默认宽度为 48px，可用 `CompactPaneLength` 属性修改。面板展开时会压缩内容区的尺寸。

## Example

<XamlPreview>

```xml
<SplitView xmlns="https://github.com/avaloniaui"
           IsPaneOpen="True"
           DisplayMode="Inline"
           OpenPaneLength="100">
    <SplitView.Pane>
        <TextBlock Text="Pane"
                   FontSize="24"
                   VerticalAlignment="Center"
                   HorizontalAlignment="Center"/>
    </SplitView.Pane>

    <Grid>
        <TextBlock Text="Content"
                   FontSize="24"
                   VerticalAlignment="Center"
                   HorizontalAlignment="Center"/>
    </Grid>
</SplitView>
```

</XamlPreview>

## 紧凑显示模式 {#compact-display-mode}

把 split view 控件、某种紧凑显示模式和 MVVM 模式搭在一起，就能做出「工具面板」式的界面：面板收起时仍有足够空间放一个图标按钮，点它即可展开面板。

<Image light={SplitViewCompactScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 导航侧栏范式 {#navigation-sidebar-pattern}

`SplitView` 的一种常见用法，是做成带图标按钮、可折叠的导航侧栏：

```xml
<SplitView IsPaneOpen="{Binding IsPaneOpen}"
           DisplayMode="CompactInline"
           CompactPaneLength="48"
           OpenPaneLength="200">
    <SplitView.Pane>
        <StackPanel>
            <Button Content="☰" Command="{Binding TogglePaneCommand}"
                    Width="48" HorizontalAlignment="Left" />
            <ListBox ItemsSource="{Binding NavItems}"
                     SelectedItem="{Binding SelectedNavItem}"
                     Background="Transparent">
                <ListBox.ItemTemplate>
                    <DataTemplate>
                        <StackPanel Orientation="Horizontal" Spacing="12" Height="40">
                            <PathIcon Data="{Binding Icon}" Width="16" />
                            <TextBlock Text="{Binding Title}" VerticalAlignment="Center" />
                        </StackPanel>
                    </DataTemplate>
                </ListBox.ItemTemplate>
            </ListBox>
        </StackPanel>
    </SplitView.Pane>
    <SplitView.Content>
        <ContentControl Content="{Binding CurrentPage}" />
    </SplitView.Content>
</SplitView>
```

```csharp
[ObservableProperty]
private bool _isPaneOpen = true;

[RelayCommand]
private void TogglePane() => IsPaneOpen = !IsPaneOpen;
```

## 面板位置 {#pane-placement}

面板可以摆在内容区的任意一侧：

```xml
<!-- Pane on the right -->
<SplitView PanePlacement="Right"
           IsPaneOpen="True"
           DisplayMode="Inline"
           OpenPaneLength="250">
```

`Top` 和 `Bottom` 会形成上下分割，面板位于内容上方或下方。这两种方向下，面板的高度由 `OpenPaneLength` 和 `CompactPaneLength` 控制：

```xml
<!-- Pane on top -->
<SplitView PanePlacement="Top"
           IsPaneOpen="True"
           DisplayMode="Inline"
           OpenPaneLength="150">
    <SplitView.Pane>
        <TextBlock Text="Top pane" Margin="8" />
    </SplitView.Pane>
    <TextBlock Text="Main content" Margin="8" />
</SplitView>
```

## 另请参阅 {#see-also}

- [SplitView API 参考](/api/avalonia/controls/splitview)
- [GitHub 上的 `SplitView.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/SplitView/SplitView.cs)
