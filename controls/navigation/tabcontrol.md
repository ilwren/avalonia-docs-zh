---
id: tabcontrol
title: TabControl
description: 介绍 Avalonia 的 TabControl：它把内容组织成可切换的选项卡页。
doc-type: reference
---

[`TabControl`](/api/avalonia/controls/tabcontrol) 可以把一个视图划分成若干选项卡项。

每个选项卡项都有标题和内容区。标题按它们在 XAML 中出现的顺序排成一条。点击某个选项卡标题，它的内容就会显示在选项卡栏下方的内容区里。

标题区和内容区都可以自由编排界面，以满足你的 Avalonia 应用的需要。

:::info
如果你只需要这个控件中选项卡标题那部分的功能，不妨改用 [选项卡栏](/controls/navigation/tabstrip)。
:::

## 常用属性 {#common-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `TabStripPlacement` | `Dock` | 选项卡栏的位置：`Top`、`Bottom`、`Left`、`Right`。默认值是 `Top`。 |
| `SelectedIndex` | `int` | 当前选中选项卡的索引，从 0 开始。 |
| `SelectedItem` | `object` | 当前选中的选项卡项。 |
| `ItemsSource` | `IEnumerable` | 用于动态生成选项卡的集合。 |
| `ItemTemplate` | `IDataTemplate` | 使用 `ItemsSource` 时，选项卡标题所用的模板。 |
| `ContentTemplate` | `IDataTemplate` | 使用 `ItemsSource` 时，选项卡内容所用的模板。 |

## 示例 {#examples}

这是一个简单的选项卡示例，内容只是一些文字：

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <TabControl Margin="5">
    <TabItem Header="Tab 1">
      <TextBlock Margin="5">This is tab 1 content</TextBlock>
    </TabItem>
    <TabItem Header="Tab 2">
      <TextBlock Margin="5">This is tab 2 content</TextBlock>
    </TabItem>
  </TabControl>
</UserControl>
```

</XamlPreview>

## 选项卡位置 {#tab-placement}

设置 `TabStripPlacement` 属性，就能把选项卡摆到内容区的任意一侧。默认值是 `Top`。下面的例子把选项卡放在左侧：

```xml
<TabControl TabStripPlacement="Left">
    <TabItem Header="Page 1"><TextBlock Text="Content 1" Margin="8" /></TabItem>
    <TabItem Header="Page 2"><TextBlock Text="Content 2" Margin="8" /></TabItem>
</TabControl>
```

你也可以用 `Bottom` 或 `Right`，把选项卡放到内容区下方或右侧。

## 从集合动态生成选项卡 {#dynamic-tabs-from-a-collection}

可以用 `ItemsSource` 把 `TabControl` 绑定到视图模型中的集合，再用 `ItemTemplate` 定义选项卡标题的渲染方式、用 `ContentTemplate` 定义内容区的渲染方式：

```xml
<TabControl ItemsSource="{Binding Tabs}"
            SelectedItem="{Binding SelectedTab}">
    <TabControl.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Header}" />
        </DataTemplate>
    </TabControl.ItemTemplate>
    <TabControl.ContentTemplate>
        <DataTemplate>
            <ContentControl Content="{Binding Content}" />
        </DataTemplate>
    </TabControl.ContentTemplate>
</TabControl>
```

对应的视图模型大致是这样：

```csharp
public class MainViewModel : ViewModelBase
{
    public ObservableCollection<TabItemViewModel> Tabs { get; } = new()
    {
        new TabItemViewModel("Settings", "Settings content goes here."),
        new TabItemViewModel("Account", "Account content goes here."),
    };

    public TabItemViewModel? SelectedTab { get; set; }
}

public class TabItemViewModel
{
    public string Header { get; }
    public string Content { get; }

    public TabItemViewModel(string header, string content)
    {
        Header = header;
        Content = content;
    }
}
```

## 延迟加载内容 {#lazy-content-loading}

默认情况下，`TabControl` 在首次加载时就会为每个选项卡创建内容。如果选项卡里装的是复杂视图，可以把每个选项卡的内容包进 `UserControl`，再通过 `DataTemplate` 按需加载，从而把内容创建推迟到选项卡被选中时：

```xml
<TabControl ItemsSource="{Binding Tabs}"
            SelectedItem="{Binding SelectedTab}">
    <TabControl.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Header}" />
        </DataTemplate>
    </TabControl.ItemTemplate>
    <TabControl.ContentTemplate>
        <DataTemplate DataType="vm:TabItemViewModel">
            <views:TabContentView />
        </DataTemplate>
    </TabControl.ContentTemplate>
</TabControl>
```

由于 `ContentTemplate` 会在每次选中选项卡时新建一个视图实例，视觉树中只存在当前可见选项卡的内容。选项卡很多时，这能降低内存占用、改善启动性能。

## 响应选项卡切换 {#responding-to-tab-changes}

把 `SelectedIndex` 或 `SelectedItem` 绑定到视图模型，即可对选项卡切换作出响应：

```xml
<TabControl SelectedIndex="{Binding ActiveTabIndex}">
    <TabItem Header="General"><TextBlock Text="General settings" Margin="8" /></TabItem>
    <TabItem Header="Advanced"><TextBlock Text="Advanced settings" Margin="8" /></TabItem>
</TabControl>
```

```csharp
public class SettingsViewModel : ViewModelBase
{
    private int _activeTabIndex;

    public int ActiveTabIndex
    {
        get => _activeTabIndex;
        set => this.RaiseAndSetIfChanged(ref _activeTabIndex, value);
    }
}
```

## 另请参阅 {#see-also}

- [TabStrip](/controls/navigation/tabstrip)
- [Carousel](/controls/data-display/collections/carousel)
- [TabControl API 参考](/api/avalonia/controls/tabcontrol)
- [GitHub 上的 `TabControl.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/TabControl.cs)
