---
id: autocompletebox
title: AutoCompleteBox
---

import AutoCompleteBoxScreenshot from '/img/controls/autocompletebox/autocompletebox.gif';

`AutoCompleteBox` 提供一个供用户输入的文本框，以及一个下拉列表，里面是数据源集合中与所键入文本相匹配的候选项。用户一开始键入，下拉列表就出现，并且每敲一个字符都会刷新匹配结果，用户可以从中选取。

文本与数据源中候选项的匹配方式可以配置。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table><thead><tr><th width="233">Property</th><th>说明</th></tr></thead><tbody><tr><td><code>ItemsSource</code></td><td>用于匹配的候选项列表。 </td></tr><tr><td><code>FilterMode</code></td><td>匹配方式的选项，见下表。</td></tr><tr><td><code>AsyncPopulator</code></td><td>一个异步函数，针对给定的（字符串）条件给出匹配列表。</td></tr><tr><td><code>MaxLength</code></td><td>用户最多能键入的字符数。0 表示不限。</td></tr><tr><td><code>InnerLeftContent</code></td><td>显示在文本区左侧内部的内容（比如搜索图标）。</td></tr><tr><td><code>InnerRightContent</code></td><td>显示在文本区右侧内部的内容（比如清除按钮）。</td></tr></tbody></table>

筛选模式属性的可选值如下：

<table><thead><tr><th width="350">Filter Mode</th><th>说明</th></tr></thead><tbody><tr><td><code>StartsWith</code></td><td>区分区域设置、不区分大小写的筛选，返回以指定文本开头的条目。</td></tr><tr><td><code>StartsWithCaseSensitive</code></td><td>区分区域设置、区分大小写的筛选，返回以指定文本开头的条目。</td></tr><tr><td><code>StartsWithOrdinal</code></td><td>按序号比较、不区分大小写的筛选，返回以指定文本开头的条目。</td></tr><tr><td><code>StartsWithOrdinalCaseSensitive</code></td><td>按序号比较、区分大小写的筛选，返回以指定文本开头的条目。</td></tr><tr><td><code>Contains</code></td><td>区分区域设置、不区分大小写的筛选，返回包含指定文本的条目。</td></tr><tr><td><code>ContainsCaseSensitive</code></td><td>区分区域设置、区分大小写的筛选，返回包含指定文本的条目。</td></tr><tr><td><code>ContainsOrdinal</code></td><td>按序号比较、不区分大小写的筛选，返回包含指定文本的条目。</td></tr><tr><td><code>ContainsOrdinalCaseSensitive</code></td><td>按序号比较、区分大小写的筛选，返回包含指定文本的条目。</td></tr><tr><td><code>Equals</code></td><td>区分区域设置、不区分大小写的筛选，返回与指定文本相同的条目。</td></tr><tr><td><code>EqualsCaseSensitive</code></td><td>区分区域设置、区分大小写的筛选，返回与指定文本相同的条目。</td></tr><tr><td><code>EqualsOrdinal</code></td><td>按序号比较、不区分大小写的筛选，返回与指定文本相同的条目。</td></tr><tr><td><code>EqualsOrdinalCaseSensitive</code></td><td>按序号比较、区分大小写的筛选，返回与指定文本相同的条目。</td></tr></tbody></table>

:::info
在**按序号**比较字符串时，每个字符都按其原始字节值比对（与语言无关）。
:::

:::info
**区分区域设置**指的是在设计和技术实现中照顾不同文化背景用户的需要，包括按语言采用不同的字符串处理与排序方式。比如英语通常按 A-Z 字母顺序排，中文可能按拼音或笔画排，其他语言又有各自的排序规则。
:::


## 示例 {#examples}

这个例子用的是在 C# 代码隐藏中设定的固定数据源（数组）。

```xml
<StackPanel Margin="20">
  <TextBlock Margin="0 5">Choose an animal:</TextBlock>
  <AutoCompleteBox x:Name="animals" FilterMode="StartsWith" />
</StackPanel>
```

```csharp title='C#'
using Avalonia.Controls;
using System.Linq;

namespace AvaloniaControls.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            animals.ItemsSource = new string[] 
                {"cat", "camel", "cow", "chameleon", "mouse", "lion", "zebra" }
            .OrderBy(x=>x);
        }
    }
}
```

<Image light={AutoCompleteBoxScreenshot} maxWidth={400} cornerRadius="true" position="center" alt="A short animation demonstrating the type-to-search functionality of the auto-complete box using a list of animals." />
<br />

### 用 AutoCompleteBox 处理对象 {#using-autocompletebox-with-objects}
当数据不是简单字符串而是复杂对象时，需要指明显示哪个属性、以及控件该如何筛选底层数据。下面几节分别讲显示绑定、自定义筛选，以及所呈现文本的格式化。

#### Filtering Objects Using ValueMemberBinding
ValueMemberBinding 告诉控件：对象的哪个属性要显示在文本框中，并用于内置筛选。

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:vm="using:YourNamespace.ViewModels"
        x:Class="YourNamespace.MainWindow"
        x:DataType="vm:MainViewModel">

    <StackPanel Margin="20">
        <TextBlock Margin="0 5">Select a product:</TextBlock>

        <AutoCompleteBox ItemsSource="{Binding Products}"
                         SelectedItem="{Binding SelectedProduct}"
                         ValueMemberBinding="{Binding Name}"
                         FilterMode="Contains"
                         MinimumPrefixLength="0" />

        <TextBlock Margin="0 10"
                   Text="{Binding SelectedProduct.Price,
                                  StringFormat='Price: ${0:F2}'}" />
    </StackPanel>
</Window>
```

```csharp title='C#'

using System.Collections.ObjectModel;
using System.ComponentModel;

public class Product : INotifyPropertyChanged
{
    private int id;
    private string name = string.Empty;
    private decimal price;

    public int Id
    {
        get => id;
        set
        {
            if (id != value)
            {
                id = value;
                OnPropertyChanged(nameof(Id));
            }
        }
    }

    public string Name
    {
        get => name;
        set
        {
            if (name != value)
            {
                name = value;
                OnPropertyChanged(nameof(Name));
            }
        }
    }

    public decimal Price
    {
        get => price;
        set
        {
            if (price != value)
            {
                price = value;
                OnPropertyChanged(nameof(Price));
            }
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;
    private void OnPropertyChanged(string propertyName) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
}

public class MainViewModel : INotifyPropertyChanged
{
    private Product? selectedProduct;

    public ObservableCollection<Product> Products { get; } = new()
    {
        new Product { Id = 1, Name = "Laptop", Price = 999.99m },
        new Product { Id = 2, Name = "Mouse", Price = 29.99m },
        new Product { Id = 3, Name = "Keyboard", Price = 79.99m },
        new Product { Id = 4, Name = "Monitor", Price = 299.99m },
        new Product { Id = 5, Name = "Headphones", Price = 149.99m }
    };

    public Product? SelectedProduct
    {
        get => selectedProduct;
        set
        {
            if (selectedProduct != value)
            {
                selectedProduct = value;
                OnPropertyChanged(nameof(SelectedProduct));
            }
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;
    private void OnPropertyChanged(string propertyName) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
}

```

#### 用 ItemFilter 实现自定义筛选 {#implementing-custom-filtering-using-itemfilter}
若需要同时在多个属性（比如 Name 和 Id）中搜索，请提供一个自定义筛选函数。

```xml
<AutoCompleteBox x:Name="ProductAutoComplete"
                 ItemsSource="{Binding Products}"
                 SelectedItem="{Binding SelectedProduct}"
                 ValueMemberBinding="{Binding Name}"
                 MinimumPrefixLength="1" />
```
```csharp title='C#'

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        // Custom filter searching both Name and Id
        ProductAutoComplete.ItemFilter = (search, item) =>
        {
            if (item is Product product && !string.IsNullOrWhiteSpace(search))
            {
                return product.Name.Contains(search, StringComparison.OrdinalIgnoreCase)
                    || product.Id.ToString().Contains(search);
            }
            return true;
        };
    }
}

```

#### 用值转换器定制文本 {#customizing-text-using-a-value-converter}
用值转换器可以控制下拉列表中显示的文本。当你想把几个字段拼在一起显示时（比如商品名加价格），这很有用。但要留意它同时也会影响筛选行为：如果名称和价格都显示出来，用户用任一个值都能筛选。

如果你只想改变条目的视觉呈现、不影响筛选，请改用标准的 ItemTemplate 属性。

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:converters="using:YourNamespace.Converters"
        xmlns:vm="clr-namespace:YourNamespace.ViewModels;assembly=YourNamespace"
        x:DataType="vm:MainViewModel">

    <Window.Resources>
        <converters:ProductDisplayConverter x:Key="ProductDisplayConverter" />
    </Window.Resources>

    <StackPanel Margin="20">
        <TextBlock Margin="0 5">Select a product:</TextBlock>

        <AutoCompleteBox ItemsSource="{Binding Products}"
                         SelectedItem="{Binding SelectedProduct}"
                         ValueMemberBinding="{Binding ., Converter={StaticResource ProductDisplayConverter}}"
                         FilterMode="Contains" />
    </StackPanel>
</Window>

```
```csharp title='C#'

using Avalonia.Data.Converters;
using System;
using System.Globalization;

namespace YourNamespace.Converters
{
    public class ProductDisplayConverter : IValueConverter
    {
        public object? Convert(object? value, Type targetType,
                               object? parameter, CultureInfo culture)
        {
            if (value is Product product)
                return $"{product.Name} (${product.Price:F2})";

            return value?.ToString();
        }

        public object? ConvertBack(object? value, Type targetType,
                                   object? parameter, CultureInfo culture)
            => throw new NotSupportedException();
    }
}


```
## 另请参阅 {#see-also}

- [AutoCompleteBox API 参考](/api/avalonia/controls/autocompletebox)
- [GitHub 上的 `AutoCompleteBox.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/AutoCompleteBox/AutoCompleteBox.cs)
