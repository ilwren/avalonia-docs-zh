---
id: combobox
title: ComboBox
description: 一个下拉选择器：让用户从列表中选出一项，还可选配可编辑的文本输入和占位提示。
doc-type: reference
---

import ComboBoxDataTemplateScreenshot from '/img/controls/combobox/combobox-data-template.gif';
import ComboBoxBindingToViewModel from '/img/controls/combobox/combobox-binding-to-viewmodel.png';
import ComboBoxEditable from '/img/controls/combobox/combobox-editable.gif';

`ComboBox` 在一个框里显示当前选中项，旁边的下拉按钮展开后列出所有选项。本页是该控件的通用参考；`ComboBox` 的实用指引请参阅[操作指南：使用 ComboBox](/docs/how-to/combobox-how-to)。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性                   | 类型       | 说明                                                                                                              |
| -------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| `ItemsSource`                    | `IEnumerable?` | 作为控件数据源的绑定集合。继承自 [`ItemsControl`](/controls/data-display/collections/itemscontrol)。                                                                                           |
| `SelectedIndex`            | `int`      | 选中项的索引（从 0 开始）。                                                                             |
| `SelectedItem`             | `object?`  | 选中项本身。                                                                                                |
| `SelectedValue`            | `object?`  | 选中项的值，由 `SelectedValueBinding` 决定。                                                    |
| `IsEditable`               | `bool`     | 启用文本编辑，允许直接在组合框里键入内容。                           |
| `Text`                     | `string?`  | 当 `IsEditable` 为 `true` 时，获取或设置文本值。                                                                 |
| `PlaceholderText`          | `string?`  | 未选中任何条目时显示的占位文字。                                                                                     |
| `AutoScrollToSelectedItem` | `bool`     | 指示是否自动滚动到新选中的条目。                                                       |
| `IsDropDownOpen`           | `bool`     | 指示下拉当前是否展开。                                                                        |
| `MaxDropDownHeight`        | `double`   | 下拉列表的最大高度。这指的是列表部分的实际高度，而不是显示多少个条目。  |
| `ItemsPanel`               | `ITemplate<Panel>` | 承载各项的容器面板，默认是 `StackPanel`。自定义 `ItemsPanel` 的方法见[自定义面板](/docs/how-to/itemscontrol-how-to#custom-panel)。 |

<br />

:::note
默认情况下，组合框的宽高会随选中项自适应。若需要固定尺寸，也可以显式设置 `Width` 和 `Height`。
:::

## 小贴士 {#tips}

- 若希望控件加载时就显示某个选中项，请务必给 `SelectedIndex` 或 `SelectedItem` 设一个初始值。两者都不设、又没指定 `PlaceholderText` 时，控件会是空白的。
- 用 `PlaceholderText` 在尚未选中任何条目时给用户一点提示（比如「请选择…」）。
- 把 `ItemsSource` 绑定到一组复杂对象时，请提供 `ItemTemplate`，好让控件知道每一项该怎么渲染。没有模板时，控件会对每个对象调用 `ToString()`。
- 若要在代码中清除选中项，请把 `SelectedIndex` 设为 `-1`，或把 `SelectedItem` 设为 `null`。
- 选中项每次变化都会触发 `SelectionChanged` 事件。要在视图模型之外跑一些副作用逻辑时，可以用它。
- 列表中的条目可以自由编排、绑定或套模板。关于数据模板，请参阅[数据模板简介](/docs/data-templates/introduction-to-data-templates)。

## 示例 {#examples}

### 基本示例 {#basic-example}

一个最基础的文本条目列表。它们写死在 XAML 里，因此运行时无法改变。`SelectedIndex` 按列表位置预先选中其中一项作为默认选中项。下拉菜单的高度是固定的，内容超出时便可滚动。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Margin="20">
  <ComboBox SelectedIndex="0" MaxDropDownHeight="100">
    <ComboBoxItem>Text Item 1</ComboBoxItem>
    <ComboBoxItem>Text Item 2</ComboBoxItem>
    <ComboBoxItem>Text Item 3</ComboBoxItem>
    <ComboBoxItem>Text Item 4</ComboBoxItem>
    <ComboBoxItem>Text Item 5</ComboBoxItem>
    <ComboBoxItem>Text Item 6</ComboBoxItem>
    <ComboBoxItem>Text Item 7</ComboBoxItem>
    <ComboBoxItem>Text Item 8</ComboBoxItem>
    <ComboBoxItem>Text Item 9</ComboBoxItem>
  </ComboBox>
</StackPanel>
```

</XamlPreview>

### 组合出来的视图 {#composed-view}

这个组合框的下拉列表把文字叠在彩色圆片上显示。

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Margin="20">
  <ComboBox SelectedIndex="0">
    <ComboBoxItem>
      <Panel>
        <Ellipse Width="50" Height="50" Fill="Red"/>
        <TextBlock VerticalAlignment="Center"
                   HorizontalAlignment="Center">Red</TextBlock>
      </Panel>
    </ComboBoxItem>
    <ComboBoxItem>
        <Panel>
          <Ellipse Width="50" Height="50" Fill="Orange"/>
          <TextBlock VerticalAlignment="Center"
                       HorizontalAlignment="Center">Amber</TextBlock>
        </Panel>
    </ComboBoxItem>
    <ComboBoxItem>
      <Panel>
        <Ellipse Width="50" Height="50" Fill="Green"/>
        <TextBlock VerticalAlignment="Center"
                   HorizontalAlignment="Center">Green</TextBlock>
        </Panel>
    </ComboBoxItem>
  </ComboBox>
</StackPanel>
```

</XamlPreview>

### 绑定数据模板 {#binding-to-a-data-template}

这个例子用数据模板绑定组合框中的条目。C# 代码隐藏加载系统已安装的字体族名称，并把它们绑定到 `ItemsSource` 属性。

<Tabs>

<TabItem value="xaml" label="MainWindow.axaml">

```xml
<StackPanel Margin="20">
    <ComboBox x:Name="fontComboBox"
              SelectedIndex="0"
              Width="200" MaxDropDownHeight="300"
              ItemsSource="{Binding FontFamilies}"
              SelectedValue="{Binding SelectedFont}">
        <ComboBox.ItemTemplate>
            <DataTemplate x:DataType="FontFamily">
                <TextBlock Text="{Binding Name}" FontFamily="{Binding}" />
            </DataTemplate>
        </ComboBox.ItemTemplate>
    </ComboBox>
</StackPanel>
```

</TabItem>

<TabItem value="csharp" label="MainWindow.axaml.cs">

```csharp
using Avalonia.Controls;
using Avalonia.Media;
using Avalonia.Media.Fonts;
using System.Collections.Generic;
using System.Linq;

namespace TmpAvaloniaApp;

public partial class MainWindow : Window
    
{
    public MainWindow()
    {
        InitializeComponent();
        IFontCollection fontCollection = FontManager.Current.SystemFonts;
        FontFamilies = new List<FontFamily>(fontCollection).OrderBy(x=>x.Name).ToList();
        DataContext = this;
    }
    
    public FontFamily? SelectedFont { get; set; }

    public List<FontFamily> FontFamilies { get; set; }
    
}
```

</TabItem>

<TabItem value="preview" label="Preview">

<Image light={ComboBoxDataTemplateScreenshot} alt="ComboBox with data template showing font families." position="center" maxWidth={400} cornerRadius="true"/>

</TabItem>

</Tabs>

### 绑定到视图模型 {#binding-to-a-view-model}

组合框的列表项也可以在视图模型中绑定。本例把条目放进主窗口视图模型的一个 `ObservableCollection` 中，`ItemsSource` 和 `SelectedItem` 都绑定到它。

<Tabs>

<TabItem value="xaml" label="MainWindow.axaml">

```xml
<ComboBox ItemsSource="{Binding Categories}"
          SelectedItem="{Binding SelectedCategory}"
          PlaceholderText="Select a category" />
```

</TabItem>

<TabItem value="csharp" label="MainWindowViewModel.cs">

```csharp
using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;

namespace ComboBoxTest.ViewModels;

public partial class MainWindowViewModel : ViewModelBase
{
    public ObservableCollection<string> Categories { get; } = new()
    {
        "Electronics", "Clothing", "Books", "Food"
    };

    [ObservableProperty]
    private string? _selectedCategory;
}
```

</TabItem>

<TabItem value="preview" label="Preview">

<Image light={ComboBoxBindingToViewModel} alt="Open ComboBox showing a list of four items defined in the view model." position="center" maxWidth={400} cornerRadius="true"/>

</TabItem>

</Tabs>

## 可编辑的组合框 {#editable-combo-box}

`ComboBox` 有一个 `IsEditable` 属性。设为 `true` 后，框内就能键入文本。
 
在框中键入的内容若与某个列表项匹配，便会设置 `SelectedItem`。借此可以让用户不必翻下拉列表就选中条目。

<Tabs>

<TabItem value="xaml" label="MainWindow.axaml">

```xml
<StackPanel>
    <!-- You must bind SelectedItem in XAML to persist the selection.
         Otherwise, the selection just shows in the box but does nothing. -->
    <ComboBox ItemsSource="{Binding Countries}"
              // highlight-next-line
              SelectedItem="{Binding SelectedCountry}"
              IsEditable="True"
              PlaceholderText="Input a country..." />
    
    <TextBlock Text="{Binding SelectedCountry, StringFormat='You have selected {0}'}" />
</StackPanel>
```

</TabItem>

<TabItem value="csharp" label="MainWindowViewModel.cs">

```csharp
using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;

namespace ComboBoxTest.ViewModels;

public partial class MainWindowViewModel : ViewModelBase
{
    public ObservableCollection<string> Countries { get; } = new()
    {
        "Australia", "Canada", "Japan", "Singapore", "UK", "USA"
    };
    
    [ObservableProperty]
    private string? _selectedCountry;
}
```

</TabItem>

<TabItem value="preview" label="Preview">

<Image light={ComboBoxEditable} alt="A short animation displaying items from the combo box being selected by text input or clicking the dropdown list." position="center" maxWidth={400} cornerRadius="true"/>

</TabItem>

</Tabs>

:::caution
`IsEditable="True"` 并不会让 `ComboBox` 变得可搜索，也不会在用户键入时过滤下拉列表。

若需要「键入即搜索」的功能，请改用 [`AutoCompleteBox`](/controls/input/text-input/autocompletebox)。你可以把上面例子中的 `ComboBox` 换成 `AutoCompleteBox` 对比一下效果。
:::

### 复杂数据对象 {#complex-data-objects}

当条目是含多个成分的复杂对象时（比如由姓名、职位、邮箱等组成的用户资料），请用 `TextSearch.TextBinding` 指明可编辑文本应该与哪个属性比对。

```xml
<ComboBox IsEditable="True"
          ItemsSource="{Binding People}"
          SelectedItem="{Binding SelectedPerson}"
          TextSearch.TextBinding="{Binding FullName}">
    <ComboBox.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding FullName}" />
        </DataTemplate>
    </ComboBox.ItemTemplate>
</ComboBox>
```

## 另请参阅 {#see-also}

- [操作指南：使用 ComboBox](/docs/how-to/combobox-how-to)
- [ListBox](/controls/data-display/collections/listbox)
- [AutoCompleteBox](/controls/input/text-input/autocompletebox)
- [RadioButton](/controls/input/buttons/radiobutton)
- [数据模板](/docs/data-templates/introduction-to-data-templates)
- [ComboBox API 参考](/api/avalonia/controls/combobox)
- [GitHub 上的 `ComboBox.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ComboBox.cs)
