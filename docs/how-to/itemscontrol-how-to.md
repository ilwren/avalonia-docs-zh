---
id: itemscontrol-how-to
title: "操作指南：使用 ItemsControl"
description: 用 ItemsControl 自定义集合的排布方式
doc-type: how-to
---

本指南介绍如何用 [`ItemsControl`](/controls/data-display/collections/itemscontrol) 做出自定义的集合布局。

## `ItemsControl` vs. `ListBox`

当你要展示中小规模的集合、又不需要选择行为时，用 `ItemsControl`；当你需要支持虚拟化、可选择的集合时，用 `ListBox`。

| 控件 | 选择 | 虚拟化 | 最适合 |
|---|---|---|---|
| `ListBox` | Built-in | Yes | 可选择的列表 |
| `ItemsControl` | None | 否（默认情况下） | 自定义布局 |

## `ItemsControl` 基本用法 {#itemscontrol-basic-usage}

`ItemsControl` 按数据模板把每一项渲染成同样的模样，不提供选中、悬停或聚焦时的样式。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:BasicItemsControl">
  <UserControl.DataContext>
    <vm:MainViewModel/>
  </UserControl.DataContext>
  <ItemsControl ItemsSource="{Binding Tags}">
    <ItemsControl.ItemTemplate>
      <DataTemplate>
        <Border Background="gray"
                CornerRadius="12"
                Padding="8,4"
                Margin="2"
                HorizontalAlignment="Left">
          <TextBlock Text="{Binding}" />
        </Border>
      </DataTemplate>
    </ItemsControl.ItemTemplate>
  </ItemsControl>
</UserControl>
```

```csharp
using System.Collections.ObjectModel;

namespace BasicItemsControl;

public class MainViewModel
{
    public ObservableCollection<string> Tags { get; set; } = new()
    {
        "avalonia",
        "xaml",
        "mvvm",
        "cross-platform"
    };
}
```

</XamlPreview>

### 自定义面板 {#custom-panel}

`ItemsControl` 把内容显示在 `ItemsPanel` 中——那是个布局控件，默认为 `StackPanel`。

要改变项目的排布方式，可以把 `StackPanel` 换成别的控件：用 `ItemsPanelTemplate` 覆盖默认值，再放入你中意的布局控件。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:CustomItemsPanel">

  <UserControl.DataContext>
    <vm:MainViewModel/>
  </UserControl.DataContext>

  <ItemsControl ItemsSource="{Binding Tags}">
    <ItemsControl.ItemsPanel>
        <!-- Change to a WrapPanel to wrap items horizontally -->
        <ItemsPanelTemplate>
            <WrapPanel Orientation="Horizontal" />
        </ItemsPanelTemplate>
    </ItemsControl.ItemsPanel>
    <ItemsControl.ItemTemplate>
        <DataTemplate>
            <Border Background="gray"
                    CornerRadius="16" 
                    Padding="12,6"
                    Margin="4">
                <TextBlock Text="{Binding}" />
            </Border>
        </DataTemplate>
    </ItemsControl.ItemTemplate>
  </ItemsControl>

</UserControl>
```

```csharp
using System.Collections.ObjectModel;

namespace CustomItemsPanel;

public class MainViewModel
{
    public ObservableCollection<string> Tags { get; set; } = new()
    {
        "avalonia",
        "xaml",
        "mvvm",
        "cross-platform"
    };
}
```

</XamlPreview>

### 横向排列 {#horizontal-layout}

`StackPanel` 默认把项目纵向堆叠。想横着排，就照上一个例子那样自定义 `ItemsPanelTemplate` 并设置 `Orientation="Horizontal"`。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:HorizontalLayout">
  <UserControl.DataContext>
    <vm:MainViewModel/>
  </UserControl.DataContext>

  <ItemsControl ItemsSource="{Binding Steps}">
    <ItemsControl.ItemsPanel>
      <ItemsPanelTemplate>
        <StackPanel Orientation="Horizontal" Spacing="16" />
      </ItemsPanelTemplate>
    </ItemsControl.ItemsPanel>
    <ItemsControl.ItemTemplate>
      <DataTemplate>
        <StackPanel Width="120">
          <Border Width="40" Height="40"
                  CornerRadius="20"
                  Background="#6366F1"
                  HorizontalAlignment="Center">
          <TextBlock Text="{Binding Number}"
                     Foreground="White"
                     HorizontalAlignment="Center"
                     VerticalAlignment="Center" />
          </Border>
          <TextBlock Text="{Binding Title}"
                     HorizontalAlignment="Center"
                     Margin="0,8,0,0" />
        </StackPanel>
      </DataTemplate>
    </ItemsControl.ItemTemplate>
  </ItemsControl>
</UserControl>
```

```csharp
using System.Collections.ObjectModel;

namespace HorizontalLayout;

public class Step
{
    public string Title { get; set; }
    public int Number { get; set; }

    public Step(string title, int number)
    {
        Title = title;
        Number = number;
    }
}

public class MainViewModel
{
    public ObservableCollection<Step> Steps { get; set; } = new()
    {
        new Step("Step 1", 1),
        new Step("Step 2", 2)
    };
}
```

</XamlPreview>

### 空状态 {#empty-state}

要在集合为空时显示一个空状态提示，可以把 `ItemsControl` 包进 `Panel`，再放第二个控件，让它在集合中没有项目时现身。

本例用一个 `TextBlock` 显示简单的文字提示。它的 `IsVisible` 属性绑定到 `ItemsControl.ItemCount` 属性，因此只有 `ItemCount` 为零时提示才会出现。

```xml
<!-- Set a resource that converts string to int, so that ItemCount can compare correctly. -->
<Window.Resources>
  <x:Int32 x:Key="Zero">0</x:Int32>
</Window.Resources>

<!-- Only one of ItemsControl or TextBlock is ever displayed, so wrap everything in a Panel. -->
<Panel>

  <!-- Give the ItemsControl a name, so the TextBlock can refer to it. -->
  <ItemsControl x:Name="TagsList"
                ItemsSource="{Binding Tags}">
    <ItemsControl.ItemTemplate>
      <DataTemplate>
        <Border Background="gray"
                CornerRadius="12"
                Padding="8,4"
                Margin="2"
                HorizontalAlignment="Left">
          <TextBlock Text="{Binding}" />
        </Border>
      </DataTemplate>
    </ItemsControl.ItemTemplate>
  </ItemsControl>

  <!-- Use IsVisible to display the TextBlock when the TagsList ItemsControl has no items, as counted by the ItemCount property. -->
  <TextBlock Text="No tags"
             Margin="2"
             Opacity="0.6"
             HorizontalAlignment="Left"
             VerticalAlignment="Top"
             IsVisible="{Binding #TagsList.ItemCount,
                         Converter={x:Static ObjectConverters.Equal},
                         ConverterParameter={StaticResource Zero}}" />
</Panel>
```

### 支持虚拟化的可滚动项目 {#virtualized-scrollable-items}

要把 `ItemsControl` 变成可滚动、支持虚拟化的显示，可以把它包进 [ScrollViewer](/controls/layout/containers/scrollviewer)，再[把 `ItemsPanel` 自定义](#custom-panel)成 [`VirtualizingStackPanel`](/api/avalonia/controls/virtualizingstackpanel)。

这样做出来的控件，显示效果与 [`ListBox`](/controls/data-display/collections/listbox) 相仿，只是没有选择行为。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:VirtualizingScrollingItems">
  <UserControl.DataContext>
    <vm:MainViewModel/>
  </UserControl.DataContext>

  <ScrollViewer>
    <ItemsControl ItemsSource="{Binding Tags}">
      <ItemsControl.ItemsPanel>
        <ItemsPanelTemplate>
          <VirtualizingStackPanel />
        </ItemsPanelTemplate>
      </ItemsControl.ItemsPanel>
      <ItemsControl.ItemTemplate>
        <DataTemplate>
          <Border Background="gray"
                  CornerRadius="12"
                  Padding="8,4"
                  Margin="2"
                  HorizontalAlignment="Left">
            <TextBlock Text="{Binding}" />
          </Border>
        </DataTemplate>
      </ItemsControl.ItemTemplate>
    </ItemsControl>
  </ScrollViewer>
</UserControl>
```

```csharp
using System.Collections.ObjectModel;

namespace VirtualizingScrollingItems;

public class MainViewModel
{
    public ObservableCollection<string> Tags { get; set; } = new()
    {
        "apples",
        "oranges",
        "bananas",
        "pears",
        "mangoes",
        "guavas",
        "grapes",
        "dragonfruits",
        "lemons",
        "limes",
        "kiwis",
        "watermelons",
        "strawberries",
        "blueberries",
        "cherries",
        "passionfruits",
        "peaches",
        "plums",
        "figs",
        "kumquats",
    };
}
```

</XamlPreview>

## 用 `PreparingContainer` 自定义容器 {#customizing-containers-with-preparingcontainer}

每当 `ItemsControl` 为某个数据项创建或回收容器时，都会触发 `PreparingContainer` 事件。你可以借它为单个项目做定制，比如依据项目数据施加条件样式：

```csharp
myItemsControl.PreparingContainer += (sender, e) =>
{
    if (e.Item is TodoItem todo && todo.IsOverdue)
    {
        e.Container.Classes.Add("overdue");
    }
};
```

与之配套的 `ContainerClearing` 事件，会在容器被清空（无论是为了复用还是移除）时触发。需要的话，可以在这个事件里清理你做过的定制。

## 性能建议 {#performance-tips}

- 大集合别拿 `WrapPanel` 当 `ItemsPanel` 用——它不作虚拟化。
- 项模板要尽量轻量，模板一复杂，滚动就会变卡。

更通用的性能优化建议，请参阅[性能](/docs/app-development/performance)。

## 另请参阅 {#see-also}

- [ItemsControl](/controls/data-display/collections/itemscontrol)
- [ItemsControl API 参考](/api/avalonia/controls/itemscontrol)
- [数据模板](/docs/data-templates/introduction-to-data-templates)：模板的运作原理。
- [ListBox 操作指南](/docs/how-to/listbox-how-to)：需要选择行为时该怎么办。
