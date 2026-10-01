---
id: datagrid
title: DataGrid
---

import Pill from '/src/components/global/Pill';
import DataGridNuGetScreenshot from '/img/controls/datagrid/datagrid-nuget.png';
import DataGridSortColumnScreenshot from '/img/controls/datagrid/datagrid-sort-column.gif';
import DataGridReorderColumnScreenshot from '/img/controls/datagrid/datagrid-reorder-column.gif';
import DataGridColumnTypesScreenshot from '/img/controls/datagrid/datagrid-column-types.gif';
import DataGridTemplateColumn from '/img/controls/datagrid/grid4.gif';
import DataGridColumnPreviewScreenshot from '/img/controls/datagrid/datagridtextcolumn.png';

<Pill variant="warning">Deprecated</Pill>

`DataGrid` 以可定制的网格呈现重复数据。该控件支持设置样式、套用模板和数据绑定。

`DataGrid` 需要绑定到视图模型中的一个可观察集合，而该视图模型要能从相应的**数据上下文**中找到。

:::warning
`DataGrid` 已弃用！  
只读的表格数据，推荐使用 [TableView](/controls/data-display/structured-data/tableview)。  
需要较复杂的编辑能力时，推荐使用 [TreeDataGrid](/controls/data-display/structured-data/treedatagrid)。  
:::

:::info
若想回顾**数据上下文**背后的概念，请参阅[数据上下文](/docs/data-binding/data-context)。
:::

:::info
`DataGrid` 位于 _Avalonia_ 的一个独立包中。要在项目里用 `DataGrid`，你必须引用 **Avalonia.Controls.DataGrid** _NuGet_ 包，并引入它所依赖的样式，详见下文。
:::

### 引用 NuGet 包 {#nuget-package-reference}

你必须为 `DataGrid` 安装对应的 _NuGet_ 包，方式有几种。可以用 IDE 项目菜单中的**管理 NuGet 程序包**：

<Image light={DataGridNuGetScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

也可以在命令行里执行：

```bash
dotnet add package Avalonia.Controls.DataGrid
```

或者直接把包引用写进项目文件（`.csproj`）：

```xml
<PackageReference Include="Avalonia.Controls.DataGrid" Version="11.0.0" />
```

:::caution
注意：安装的 DataGrid 版本必须与你所用的 _Avalonia_ 版本一致。
:::

### 引入 DataGrid 样式 {#include-datagrid-styles}

你必须引用 `DataGrid` 主题，才能把 `DataGrid` 所需的额外样式带进来。做法是在应用（`App.axaml` 文件）中添加一个 `<StyleInclude>` 元素。

例如（当你使用 `FluentTheme` 时）：

```xml
<Application.Styles>
    <FluentTheme />
    <StyleInclude Source="avares://Avalonia.Controls.DataGrid/Themes/Fluent.xaml"/>
</Application.Styles>
```

:::caution
DataGrid 的样式必须与你整体所用的主题相匹配，否则会出现冲突和资源找不到的问题。第三方主题请查阅其自身的文档和示例。
:::


### 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性                | 说明                                                                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `AutoGenerateColumns`   | 是否根据所绑定条目数据源的属性名自动生成列。（默认为 false。）            |
| `ItemsSource`           | 用作该控件数据源的绑定集合。                                                           |
| `IsReadOnly`            | 为 true 时把绑定方向设为单向。默认为 false——此时网格会接受对所绑定数据的改动。         |
| `CanUserReorderColumns` | 用户能否用指针拖动列标题来调整列的显示顺序。（默认为 false。） |
| `CanUserResizeColumns`  | 用户能否用指针调整列宽。（默认为 false。）                                      |
| `CanUserSortColumns`    | 用户能否通过点击列标题来排序。（默认为 true。）                                   |

### 示例 {#examples}

下面这个例子会生成一个基本的 `DataGrid`，列标题名称由条目类自动生成，条目数据源则绑定到主窗口的视图模型。

```xml
<DataGrid Margin="20" ItemsSource="{Binding People}" 
          AutoGenerateColumns="True" IsReadOnly="True" 
          GridLinesVisibility="All"
          BorderThickness="1" BorderBrush="Gray">
</DataGrid>
```

```csharp title='C# View Model'
using AvaloniaControls.Models;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace AvaloniaControls.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        public ObservableCollection<Person> People { get; }

        public MainWindowViewModel()
        {
            var people = new List<Person> 
            {
                new Person("Neil", "Armstrong"),
                new Person("Buzz", "Lightyear"),
                new Person("James", "Kirk")
            };
            People = new ObservableCollection<Person>(people);
        }
    }
}
```

```csharp title='C# Item Class'
public class Person
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    
    public Person(string firstName , string lastName)
    {
        FirstName = firstName;
        LastName = lastName;
    }
}
```

<Image light={DataGridSortColumnScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

:::info
这些例子采用 MVVM 写法，绑定到一个 `ObservableCollection`。数据绑定背后的概念请参阅[数据绑定简介](/docs/data-binding/introduction-to-data-binding)。
:::

条目类的属性名通常并不适合直接当列名。下面这个例子为网格加上了自定义的列标题名称，同时允许调整列序和列宽，并关掉了默认的列排序：

```xml
<DataGrid Margin="20" ItemsSource="{Binding People}"
          IsReadOnly="True"
          CanUserReorderColumns="True"
          CanUserResizeColumns="True"
          CanUserSortColumns="False"
          GridLinesVisibility="All"
          BorderThickness="1" BorderBrush="Gray">
  <DataGrid.Columns>
     <DataGridTextColumn Header="First Name"  Binding="{Binding FirstName}"/>
     <DataGridTextColumn Header="Last Name" Binding="{Binding LastName}" />
  </DataGrid.Columns>
</DataGrid>
```

<Image light={DataGridReorderColumnScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

下面这个例子展示 `DataGrid` 如何接受改动并更新底层集合，以及如何用不同的列类型来编辑数据：

```xml
<DataGrid Margin="20" ItemsSource="{Binding People}"        
          GridLinesVisibility="All"
          BorderThickness="1" BorderBrush="Gray">
  <DataGrid.Columns>
     <DataGridTextColumn Header="First Name"  Binding="{Binding FirstName}"/>
     <DataGridTextColumn Header="Last Name" Binding="{Binding LastName}" />
     <DataGridCheckBoxColumn Header="Fictitious?" Binding="{Binding IsFictitious}" />
  </DataGrid.Columns>
</DataGrid>
```

```csharp title='C# View Model'
using AvaloniaControls.Models;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace AvaloniaControls.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        public ObservableCollection<Person> People { get; }

        public MainWindowViewModel()
        {
            var people = new List<Person> 
            {
                new Person("Neil", "Armstrong", false),
                new Person("Buzz", "Lightyear", true),
                new Person("James", "Kirk", true)
            };
            People = new ObservableCollection<Person>(people);
        }
    }
}
```

```csharp title='C# Item Class'
public class Person
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public bool IsFictitious { get; set; }

    public Person(string firstName , string lastName, bool isFictitious)
    {
        FirstName = firstName;
        LastName = lastName;
        IsFictitious = isFictitious;
    }
}
```

<Image light={DataGridColumnTypesScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## DataGridTemplateColumn

你可以用这种列类型来定制某一列的显示方式和编辑方式。

有两个数据模板需要以附加属性的形式定义：

<table><thead><tr><th width="269">Data Template</th><th>说明</th></tr></thead><tbody><tr><td><code>CellTemplate</code> </td><td>该列取值在非编辑状态下的呈现方式。 </td></tr><tr><td><code>CellEditingTemplate</code> </td><td>该列取值的编辑模板。</td></tr></tbody></table>

:::info
如果不设置编辑模板，该列将保持只读。
:::

### Example

下面这个例子在编辑某人的年龄属性时，呈现一个数值微调控件：



```xml
<Window ...
  xmlns:model="using:AvaloniaControls.Models">
  
  <DataGrid Margin="20" ItemsSource="{Binding People}"
          GridLinesVisibility="All"
          BorderThickness="1" BorderBrush="Gray">
    <DataGrid.Columns>
      <DataGridTextColumn Header="First Name" Width="2*"
         Binding="{Binding FirstName}" />
      <DataGridTextColumn Header="Last Name" Width="2*"
         Binding="{Binding LastName}" />
      
      <DataGridTemplateColumn Header="Age" SortMemberPath="AgeInYears">
        <DataGridTemplateColumn.CellTemplate>
          <DataTemplate DataType="model:Person">
            <TextBlock Text="{Binding AgeInYears, StringFormat='{}{0} years'}" 
              VerticalAlignment="Center" HorizontalAlignment="Center" />
          </DataTemplate>
        </DataGridTemplateColumn.CellTemplate>
        <DataGridTemplateColumn.CellEditingTemplate>
          <DataTemplate DataType="model:Person">
            <NumericUpDown Value="{Binding AgeInYears}"  
               FormatString="N0" Minimum="0" Maximum="120"  
               HorizontalAlignment="Stretch"/>
          </DataTemplate>
        </DataGridTemplateColumn.CellEditingTemplate>
      </DataGridTemplateColumn>
    
    </DataGrid.Columns>
  </DataGrid>
</Window>
```


```csharp title='C# View Model'
using AvaloniaControls.Models;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace AvaloniaControls.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        public ObservableCollection<Person> People { get; }

        public MainWindowViewModel()
        {
            var people = new List<Person> 
            {
                new Person("Neil", "Armstrong",  55),
                new Person("Buzz", "Lightyear", 38),
                new Person("James", "Kirk", 44)
            };
            People = new ObservableCollection<Person>(people);
        }
    }
}
```


```csharp title='C# Item Class'
public class Person
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public int AgeInYears { get; set; } 

    public Person(string firstName, string lastName, int ageInYears)
    {
        FirstName = firstName;
        LastName = lastName;
        AgeInYears = ageInYears;
    }
}
```

<Image light={DataGridTemplateColumn} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## DataGridColumn

一个 `DataGrid` 可以包含多个数据网格列。_Avalonia_ 内置了两种列类型用于展示不同的数据类型，另有一种模板列类型可用来定制列的外观。

| Column Type              | 说明                                                                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DataGridTextColumn`     | 用文本框来显示和编辑该列数据。这种列类型可以控制字体族、字号等排版属性。                                 |
| `DataGridCheckBoxColumn` | 当数据为布尔值时，用复选框来显示和编辑该列数据。取值可空时，这种列类型还支持三态复选框。 |
| `DataGridTemplateColumn` | 可用于定制列数据在显示和编辑两种状态下的呈现方式。                                                                                   |

### 显示行号 {#displaying-row-numbers}

绑定到 `DataGridRow.Index` 即可在某一列中显示行号：

```xml
<DataGridTextColumn Header="#"
    Binding="{Binding $parent[DataGridRow].Index}"
    Width="60" IsReadOnly="True" />
```

### 常用属性 {#useful-properties-1}

下列属性大多为三种列类型所共有：

| 属性         | 说明                                                                                                                                     |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `Header`         | 列标题的内容。                                                                                                               |
| `HeaderTemplate` | 为该列套用数据模板。                                                                                                            |
| `IsReadOnly`     | 该列是否只读。如果数据网格本身是只读的，那么无论该属性取什么值，列都是只读的。 |
| `IsThreeState`   | 仅复选框列可用。当可空布尔值为 null 时，启用第三种（填充）状态。                                                  |
| `Width`          | 列宽可以用绝对尺寸或相对尺寸给出（详见下文）。                                                                         |

### 列宽 {#column-width}

如果不为某一列设置宽度，它会按内容自动调整大小；必要时网格还会加上一条水平滚动条。

你可以为列设置绝对宽度，例如：

```xml
<DataGridTextColumn Width="200" />
```

这样一来，放不下的列内容就会被隐藏。

另一种做法是指定相对的自动尺寸。用 \* 表示均分可用宽度，也可以写成 2\* 这样的倍数。未指定宽度的列则按内容自动调整。

比如把一个数据网格均分成 3 列：

```xml
<DataGridTextColumn Width="*" />
<DataGridTextColumn Width="*" />
<DataGridTextColumn Width="*" />
```

Example

下面这个例子让两列均分整个宽度，把数据网格的呈现效果改善了一番：

```xml
<Window ... >
   <Design.DataContext>
       <vm:MainWindowViewModel/>
  </Design.DataContext>
  <DataGrid Margin="20" ItemsSource="{Binding People}"
          IsReadOnly="True"
          GridLinesVisibility="All"
          BorderThickness="1" BorderBrush="Gray">
    <DataGrid.Columns>
      <DataGridTextColumn Header="First Name" Width="*" 
              Binding="{Binding FirstName}"/>
      <DataGridTextColumn Header="Last Name" Width="*" 
              Binding="{Binding LastName}" />
    </DataGrid.Columns>
  </DataGrid>
</Window>
```

```csharp title='C# View Model'
using AvaloniaControls.Models;
using System.Collections.Generic;
using System.Collections.ObjectModel;

namespace AvaloniaControls.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        public ObservableCollection<Person> People { get; }

        public MainWindowViewModel()
        {
            var people = new List<Person> 
            {
                new Person("Neil", "Armstrong"),
                new Person("Buzz", "Lightyear"),
                new Person("James", "Kirk")
            };
            People = new ObservableCollection<Person>(people);
        }
    }
}
```

```csharp title='C# Item Class'
public class Person
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    
    public Person(string firstName , string lastName)
    {
        FirstName = firstName;
        LastName = lastName;
    }
}
```

它之所以能在预览窗格中生效，是因为 `<Design.DataContext>` 元素会创建一个供绑定的视图模型：

<Image light={DataGridColumnPreviewScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [DataGrid API 参考](https://api-docs.avaloniaui.net/docs/T_Avalonia_Controls_DataGrid)