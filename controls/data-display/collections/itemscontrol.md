---
id: itemscontrol
title: ItemsControl
description: Avalonia 中 ItemsControl 的参考文档：它是呈现重复数据的基础控件，布局和条目外观完全由你掌控。
doc-type: reference
---

`ItemsControl` 是各类呈现重复数据的控件的基类，比如 [`ListBox`](/controls/data-display/collections/listbox) 和 [`ComboBox`](/controls/input/selectors/combobox)。它本身不带任何格式化、选择或滚动行为。

配合数据绑定、样式和数据模板，你可以用它做出完全自定义的重复数据控件。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 说明 |
|---|---|
| `ItemsSource` | 用作该控件数据源的绑定集合。 |
| `ItemTemplate` | 控制每个条目外观的 `DataTemplate`。 |
| `ItemsPanel` | 承载所生成条目的面板，默认为 `StackPanel`。换成别的面板的做法请参阅[自定义面板](/docs/how-to/itemscontrol-how-to#custom-panel)。 |
| `Styles` | 作用于 `ItemsControl` 子元素的样式。 |
| `DisplayMemberBinding` | 未提供 `ItemTemplate` 时，用于指定显示哪个属性的绑定。 |

## 实用提示 {#practical-notes}

- 如果你希望运行时增删条目后界面能自动更新，`ItemsSource` 请**使用 `ObservableCollection<T>`**。普通的 `List<T>` 改动后不会通知控件刷新。
- `ItemsControl` 默认**不做虚拟化**。条目数量很大时，请改用默认就会虚拟化的 [`ListBox`](/controls/data-display/collections/listbox)，或者[把 `ItemsPanel` 改造成虚拟化控件](/docs/how-to/itemscontrol-how-to#virtualized-scrollable-items)。
- `ItemsControl` **没有滚动条**。超出可用高度的内容会被裁掉。需要滚动时，请把 `ItemsControl` 放进 [`ScrollViewer`](/controls/layout/containers/scrollviewer) 里。
- 若要**横向排布条目**而非纵向，请[替换默认的 `ItemsPanel`](/docs/how-to/itemscontrol-how-to#horizontal-layout)。
- 自 Avalonia v12 起，**`ItemsRepeater` 不再受支持**。如果你的应用还在用它，建议升级到 `ItemsControl` 或它的派生控件。

## Example

下面这个例子把一个可观察的餐具集合绑定到 `ItemsControl`，每个条目的布局和样式由嵌在 `ItemsControl.ItemTemplate` 下的 `DataTemplate` 指定。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:vm="using:MyApp">
  <UserControl.DataContext>
    <vm:MainViewModel/>
  </UserControl.DataContext>
  <StackPanel Margin="20">
    <TextBlock Margin="0 5">List of crockery:</TextBlock>
    <ItemsControl ItemsSource="{Binding CrockeryList}">
      <ItemsControl.ItemTemplate>
        <DataTemplate>
          <Border Margin="0,10,0,0"
                  CornerRadius="5"
                  BorderBrush="Gray" BorderThickness="1"
                  Padding="5">
            <StackPanel Orientation="Horizontal">
              <TextBlock Text="{Binding Title}" />
              <TextBlock Margin="5 0" FontWeight="Bold"
                         Text="{Binding Number}" />
            </StackPanel>
          </Border>
        </DataTemplate>
      </ItemsControl.ItemTemplate>
    </ItemsControl>
  </StackPanel>
</UserControl>
```

```csharp
using System.Collections.ObjectModel;

namespace MyApp;

public class Crockery
{
    public string Title { get; set; }
    public int Number { get; set; }

    public Crockery(string title, int number)
    {
        Title = title;
        Number = number;
    }
}

public class MainViewModel
{
    public ObservableCollection<Crockery> CrockeryList { get; set; } = new()
    {
        new Crockery("dinner plate", 12),
        new Crockery("side plate", 12),
        new Crockery("breakfast bowl", 6),
        new Crockery("cup", 10),
        new Crockery("saucer", 10),
        new Crockery("mug", 6),
        new Crockery("milk jug", 1)
    };
}
```

</XamlPreview>

## 另请参阅 {#see-also}

- [如何使用 ItemsControl](/docs/how-to/itemscontrol-how-to)
- [ListBox](/controls/data-display/collections/listbox)
- [Carousel](/controls/data-display/collections/carousel)
- [DataGrid](/controls/data-display/structured-data/datagrid)
- [数据模板](/docs/data-templates/introduction-to-data-templates)
- [ItemsControl API 参考](/api/avalonia/controls/itemscontrol)
- [GitHub 上的 `ItemsControl.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ItemsControl.cs)

