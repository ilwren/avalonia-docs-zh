---
id: tableview
title: TableView
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

`TableView` 把一组条目按可配置的列展示出来。它是一个只读的表格控件：只负责呈现数据，不提供对单元格内容的就地编辑。

`TableView` 派生自 [`ListBox`](/controls/data-display/collections/listbox)，因此沿用同样的 `ItemsSource` 和 `SelectionModel`。每一行是一个 `TableViewRow`，每一列是一个 `TableViewColumn`。

:::info
`TableView` 属于核心的 **Avalonia.Controls** 包，无需额外的 NuGet 包，也不必引入额外样式。它自 Avalonia 12.1 起提供。
:::


## 基本用法 {#basic-usage}

把 `ItemsSource` 属性绑定到视图模型中的某个集合，然后在 `TableView.Columns` 内为每一列声明一个 `TableViewColumn`。用列的 `Binding` 属性指定每个单元格所显示的值：

<Tabs
  defaultValue="xaml"
  values={[
      { label: 'XAML View', value: 'xaml', },
      { label: 'C# View Model', value: 'viewmodel', },
      { label: 'C# Item Class', value: 'item', },
  ]}
>

<TabItem value="xaml">

```xml
<TableView ItemsSource="{Binding Countries}">
  <TableView.Columns>
    <TableViewColumn Header="Name" Binding="{Binding Name}" />
    <TableViewColumn Header="Region" Binding="{Binding Region}" />
    <TableViewColumn Header="Population"
                     Binding="{Binding Population, StringFormat=N0}"
                     HorizontalContentAlignment="Right" />
  </TableView.Columns>
</TableView>
```

</TabItem>

<TabItem value="viewmodel">

```csharp
using System.Collections.ObjectModel;

public class MainWindowViewModel
{
    public ObservableCollection<Country> Countries { get; } =
    [
        new("Afghanistan", "Asia", 31056997),
        new("Albania", "Eastern Europe", 3581655),
        new("Algeria", "Northern Africa", 32930091),
    ];
}
```

</TabItem>

<TabItem value="item">

```csharp
public record Country(string Name, string Region, int Population);
```

</TabItem>

</Tabs>

:::info
这些例子采用 MVVM 写法，绑定到一个 `ObservableCollection`。数据绑定背后的概念请参阅[数据绑定简介](/docs/data-binding/introduction-to-data-binding)。
:::


## 常用属性 {#useful-properties}

下面这几个 `TableView` 属性大概是你用得最多的：

| 属性                | 说明                                                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `ItemsSource`           | 用作各行数据源的绑定集合。                                                                            |
| `Columns`               | `TableViewColumn` 对象的集合，定义每一列如何显示。参见[列](#columns)。 |
| `CanUserResizeColumns`  | 用户能否拖动列标题之间的分隔线来调整列宽。默认为 `true`。                          |

由于 `TableView` 派生自 `ListBox`，标准的选择相关成员同样适用，比如 `SelectionMode`、`SelectedItem`、`SelectedItems` 和 `SelectedIndex`。详情参见 [ListBox](/controls/data-display/collections/listbox)。


## Columns

一个 `TableView` 由 `Columns` 集合组成。每个 `TableViewColumn` 同时描述该列的标题单元格和数据单元格。


### 显示单元格的值 {#displaying-cell-values}

决定单元格显示什么，有两种方式：

| 属性       | 说明                                                                                                                                           |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Binding`      | 通过绑定从该行的数据项中取出单元格的值。适合简单的属性展示，比如 `Binding="{Binding Name}"`。             |
| `CellTemplate` | 用数据模板构建单元格内容。整个行数据项会作为模板的数据上下文传入，因此你可以绑定其中任意属性。   |

`CellTemplate` 的优先级高于 `Binding`。纯文本取值用 `Binding`；需要图片、按钮或多个属性组合等更丰富的内容时，则用 `CellTemplate`：

```xml
<TableView ItemsSource="{Binding Countries}">
  <TableView.Columns>
    <TableViewColumn Header="Name" Binding="{Binding Name}" />
    <TableViewColumn Header="Population">
      <TableViewColumn.CellTemplate>
        <DataTemplate>
          <ProgressBar Minimum="0" Maximum="1500000000"
                       Value="{Binding Population}"
                       VerticalAlignment="Center" />
        </DataTemplate>
      </TableViewColumn.CellTemplate>
    </TableViewColumn>
  </TableView.Columns>
</TableView>
```

### 列的属性 {#column-properties}

| 属性                     | 说明                                                                                                                                                   |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Header`                     | 列标题中显示的内容。                                                                                                                  |
| `HeaderTemplate`             | 用于显示标题内容的数据模板。                                                                                                          |
| `HeaderTheme`                | 作用于标题的 `ControlTheme`，其 TargetType 必须是 `TableViewColumnHeader`。                                                                              |
| `Binding`                    | 从行数据项中读取单元格值的绑定（[见上文](#displaying-cell-values)）。                                                                                      |
| `CellTemplate`               | 单元格内容所用的数据模板，其数据上下文为该行的数据项（[见上文](#displaying-cell-values)）。                                                          |
| `CellTheme`                  | 作用于各单元格的 `ControlTheme`，其 TargetType 必须是 `TableViewCell`。                                                                                       |
| `Width`                      | 列宽，以 `GridLength` 表示（[见下文](#column-width)）。默认为 `1*`。                                                                              |
| `CanUserResize`              | 这一列本身能否调整宽度。保持默认值（`null`）时，取值回落到 `TableView` 的 `CanUserResizeColumns` 属性（[见上文](#useful-properties)）。                  |
| `HorizontalContentAlignment` | 该列标题和各单元格中内容的水平对齐方式。默认为 `Left`。                                          |

### 列宽 {#column-width}

`Width` 属性是 `GridLength`，因此列宽可以用绝对单位或相对单位指定，就跟 [Grid](/controls/layout/panels/grid) 的列一样：

- **星号**（`*`）：该列按比例分得剩余空间。这是默认值（`1*`）。
- **像素**：以设备无关像素表示的绝对宽度。

```xml
<TableView.Columns>
  <TableViewColumn Header="Name" Width="3*" Binding="{Binding Name}" />
  <TableViewColumn Header="Region" Width="2*" Binding="{Binding Region}" />
  <TableViewColumn Header="Code" Width="80" Binding="{Binding Code}" />
</TableView.Columns>
```

### 调整列宽 {#resizing-columns}

默认情况下，用户可以拖动两个列标题之间的分隔线来调整列宽。要为整个 `TableView` 关掉这一行为，把 `CanUserResizeColumns` 设为 `False`。

```xml
<TableView ItemsSource="{Binding Countries}"
           CanUserResizeColumns="False">
  <!-- ... -->
</TableView>
```

你也可以用 `CanUserResize` 为单独某一列改写该行为。保持默认值 `null` 时，该列跟随整个 `TableView` 的 `CanUserResizeColumns` 设置；改成 `True` 或 `False` 则只覆盖这一列：

```xml
<TableView.Columns>
  <!-- Fixed width, never resizable, regardless of the table setting -->
  <TableViewColumn Header="#" Width="40"
                   Binding="{Binding Index}"
                   CanUserResize="False" />
  <TableViewColumn Header="Name" Binding="{Binding Name}" />
</TableView.Columns>
```

:::info
拖动调整手柄会把该列切换为像素宽度。
:::


## Virtualization

与 `ListBox` 类似，行默认会被虚拟化和回收复用。单元格也会随其所属的行一同回收复用。

:::warning
`TableView` 会虚拟化行，但**不会**虚拟化列。所有列始终都是实体化的，因此列数要控制在合理范围内。
:::


## 另请参阅 {#see-also}

- [ListBox](/controls/data-display/collections/listbox)
- [TableView API 参考](https://api-docs.avaloniaui.net/docs/T_Avalonia_Controls_TableView)
