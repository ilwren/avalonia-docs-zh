---
id: index
title: TreeDataGrid 控件
tags:
  - avalonia pro
  - avalonia enterprise
---

import FlatTreeDataGrid from '/img/avalonia-pro/treedatagrid/quickstart-flat-1.png';
import HierarchicalTreeDataGrid from '/img/avalonia-pro/treedatagrid/quickstart-hierarchical-1.png';

`TreeDataGrid` 把树视图和数据网格的能力合到了一个控件里，可以同时呈现层级数据和表格数据。它支持两种模式：

* _扁平模式_以二维表格呈现数据，与普通数据网格类似。
* _层级模式_以可展开的树呈现数据，并可带列。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

:::tip[要从 v11 升级？]
TreeDataGrid v12 带来了不小的 API 变动，包括列类型更名、全新的 XAML 优先工作流，以及一套流式的代码隐藏 API。完整的迁移指引请参阅[破坏性变更文档](/controls/data-display/structured-data/treedatagrid/breaking-changes-v12)。
:::

## 快速上手 {#getting-started}

1. 运行 `dotnet add package` 安装 `Avalonia.Controls.TreeDataGrid` NuGet 包。

```bash
dotnet add package Avalonia.Controls.TreeDataGrid
```

2. 在可执行项目文件（`.csproj`）中填入你的 Avalonia 许可证密钥。密钥可以在 [Avalonia 门户](https://portal.avaloniaui.net)中获取。

```xml
<ItemGroup>
  <AvaloniaUILicenseKey Include="YOUR_LICENSE_KEY" />
</ItemGroup>
```

:::tip
对于多项目解决方案，可以把许可证密钥放进[环境变量](https://learn.microsoft.com/en-us/visualstudio/msbuild/how-to-use-environment-variables-in-a-build)或[共享 props 文件](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory?view=vs-2022#directorybuildprops-example)，免得到处重复。
:::

3. 在 `App.axaml` 文件中通过 `StyleInclude` 引用 `TreeDataGrid` Fluent 主题。它会带来渲染该控件所需的资源。

```xml
<Application.Styles>
    <StyleInclude Source="avares://Avalonia.Controls.TreeDataGrid/Themes/Fluent.axaml"/>
    <!-- other styles -->
</Application.Styles>
```

关于安装 Avalonia Pro 控件的更多内容，请参阅[安装 Avalonia Pro](/tools/installing-avalonia-pro)。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性               | 说明                                                                                   |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| `ItemsSource`          | 为 XAML 中定义的列绑定数据集合。                                               |
| `Source`               | 驱动该控件行与列的数据源（代码隐藏写法）。            |
| `SelectionMode`        | 选择模式，比如 `Row`、`Cell`、`Row,Multiple`。默认为 `Row`（单选）。  |
| `CanUserResizeColumns` | 用户能否用指针调整列宽。默认为 `false`。               |
| `CanUserSortColumns`   | 用户能否点击标题排序。默认为 `true`。                  |

### 两种写法 {#two-approaches}

搭建 `TreeDataGrid` 有两条路子：

- **XAML 列**——设置 `ItemsSource`，并直接在 XAML 标记中定义各列。这是最省事的做法。
- **代码隐藏数据源**——用流式 API 在视图模型中创建 `FlatTreeDataGridSource` 或 `HierarchicalTreeDataGridSource`，再把它绑定到 `Source` 属性。筛选、以编程方式展开/折叠等功能必须走这条路。

下面的例子两种写法都会给出。

## 扁平数据 {#flat-data}

### 数据模型 {#data-model}

先写一个简单的 `Person` 类：

```csharp
public class Person
{
    public string? FirstName { get; set; }
    public string? LastName { get; set; }
    public int Age { get; set; }
}
```

然后创建一个 `MainWindowViewModel`，把示例数据放进 [`ObservableCollection<T>`](https://docs.microsoft.com/en-us/dotnet/api/system.collections.objectmodel.observablecollection-1?view=net-6.0) 中，这样网格就能自动反映数据的变化：

```csharp
using System.Collections.ObjectModel;

public class MainWindowViewModel
{
    public ObservableCollection<Person> People { get; } = new()
    {
        new Person { FirstName = "Eleanor", LastName = "Pope", Age = 32 },
        new Person { FirstName = "Jeremy", LastName = "Navarro", Age = 74 },
        new Person { FirstName = "Lailah ", LastName = "Velazquez", Age = 16 },
        new Person { FirstName = "Jazmine", LastName = "Schroeder", Age = 52 },
    };
}
```

### XAML 列 {#xaml-columns}

直接在 `TreeDataGrid` 标记中用 `ItemsSource` 定义各列：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="AvaloniaApplication.MainWindow">
  <TreeDataGrid ItemsSource="{Binding People}">
    <TreeDataGridTextColumn Header="First Name" Binding="{Binding FirstName}" />
    <TreeDataGridTextColumn Header="Last Name" Binding="{Binding LastName}" />
    <TreeDataGridTextColumn Header="Age" Binding="{Binding Age}" />
  </TreeDataGrid>
</Window>
```

### 代码隐藏数据源 {#code-behind-source}

另一种做法是用流式 API 在视图模型中创建 `FlatTreeDataGridSource<T>`，再把它绑定到 `Source` 属性：

```csharp
using System.Collections.ObjectModel;
using Avalonia.Controls;

public class MainWindowViewModel
{
    private ObservableCollection<Person> _people = new()
    {
        new Person { FirstName = "Eleanor", LastName = "Pope", Age = 32 },
        new Person { FirstName = "Jeremy", LastName = "Navarro", Age = 74 },
        new Person { FirstName = "Lailah", LastName = "Velazquez", Age = 16 },
        new Person { FirstName = "Jazmine", LastName = "Schroeder", Age = 52 },
    };

    public MainWindowViewModel()
    {
        Source = new FlatTreeDataGridSource<Person>(_people)
            .WithTextColumn("First Name", x => x.FirstName)
            .WithTextColumn("Last Name", x => x.LastName)
            .WithTextColumn(x => x.Age);
    }

    public FlatTreeDataGridSource<Person> Source { get; }
}
```

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="AvaloniaApplication.MainWindow">
  <TreeDataGrid Source="{Binding Source}"/>
</Window>
```

### 运行应用 {#run-the-application}

<Image light={FlatTreeDataGrid} maxWidth={400} alignment="center" />

## 层级数据 {#hierarchical-data}

### 数据模型 {#data-model-1}

层级模型就是那个 `Person` 类，只是多加了一个 `Children` 集合：

```csharp
public class Person
{
    public string? FirstName { get; set; }
    public string? LastName { get; set; }
    public int Age { get; set; }
    public ObservableCollection<Person> Children { get; } = new();
}
```

此时视图模型中装的是嵌套数据：

```csharp
using System.Collections.ObjectModel;

public class MainWindowViewModel
{
    public ObservableCollection<Person> People { get; } = new()
    {
        new Person
        {
            FirstName = "Eleanor",
            LastName = "Pope",
            Age = 32,
            Children =
            {
                new Person { FirstName = "Marcel", LastName = "Gutierrez", Age = 4 },
            }
        },
        new Person
        {
            FirstName = "Jeremy",
            LastName = "Navarro",
            Age = 74,
            Children =
            {
                new Person
                {
                    FirstName = "Jane",
                    LastName = "Navarro",
                    Age = 42 ,
                    Children =
                    {
                        new Person { FirstName = "Lailah ", LastName = "Velazquez", Age = 16 }
                    }
                },
            }
        },
        new Person { FirstName = "Jazmine", LastName = "Schroeder", Age = 52 },
    };
}
```

### XAML 列 {#xaml-columns-1}

用 `TreeDataGridHierarchicalExpanderColumn` 包住应当显示树展开器的那一列。`ChildrenBinding` 特性则指明到哪里去找子项：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="AvaloniaApplication.MainWindow">
  <TreeDataGrid ItemsSource="{Binding People}">
    <TreeDataGridHierarchicalExpanderColumn Header="First Name"
                                            ChildrenBinding="{Binding Children}">
      <TreeDataGridTextColumn Binding="{Binding FirstName}" />
    </TreeDataGridHierarchicalExpanderColumn>
    <TreeDataGridTextColumn Header="Last Name" Binding="{Binding LastName}" />
    <TreeDataGridTextColumn Header="Age" Binding="{Binding Age}" />
  </TreeDataGrid>
</Window>
```

### 代码隐藏数据源 {#code-behind-source-1}

若采用代码隐藏写法，请使用 `HierarchicalTreeDataGridSource<T>` 配合 `WithHierarchicalExpanderTextColumn` 流式方法：

```csharp
using System.Collections.ObjectModel;
using Avalonia.Controls;

public class MainWindowViewModel
{
    private ObservableCollection<Person> _people = /* defined earlier */

    public MainWindowViewModel()
    {
        Source = new HierarchicalTreeDataGridSource<Person>(_people)
            .WithHierarchicalExpanderTextColumn(
                "First Name",
                x => x.FirstName,
                x => x.Children)
            .WithTextColumn("Last Name", x => x.LastName)
            .WithTextColumn(x => x.Age);
    }

    public HierarchicalTreeDataGridSource<Person> Source { get; }
}
```

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        x:Class="AvaloniaApplication.MainWindow">
  <TreeDataGrid Source="{Binding Source}"/>
</Window>
```

### 运行应用 {#run-the-application-1}

<Image light={HierarchicalTreeDataGrid} maxWidth={400} alignment="center" />

## 进阶用法 {#advanced-usage}

- [列类型](/controls/data-display/structured-data/treedatagrid/column-types)
- [选择模式](/controls/data-display/structured-data/treedatagrid/selection-modes)
- [展开与折叠操作](/controls/data-display/structured-data/treedatagrid/expand-and-collapse)
- [Sorting](/controls/data-display/structured-data/treedatagrid/sorting)
- [Filtering](/controls/data-display/structured-data/treedatagrid/filtering)

## 另请参阅 {#see-also}

- [DataGrid](/controls/data-display/structured-data/datagrid/)
