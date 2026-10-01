---
id: binding-classes
title: 如何绑定样式类
description: 把样式类绑定到布尔属性，按条件为 Avalonia 控件应用样式。
doc-type: how-to
---

import BindStyleClassSampleScreenshot from '/img/guides/data/bind-style-class.png';

本文介绍如何根据数据绑定的布尔值，按条件给控件套上样式类。

为此，你需要在 `<Styles>` 集合中定义若干样式类，并让它们指向你所使用的控件类型。

随后就能借助特殊的 `Classes.` 语法配合数据绑定，按条件把这些类应用到控件上。写法如下：

```xml
<SomeControl Classes.myClass="{Binding IsMyClassActive}">
```

### 绑定多个样式类 {#multiple-class-bindings}

同一个控件上可以绑定多个样式类。各个类绑定互不干扰，可以随意组合：

```xml
<TextBlock Classes.error="{Binding HasError}"
           Classes.highlight="{Binding IsHighlighted}"
           Classes.large="{Binding IsLarge}" />
```

### 取反运算符 {#negation-operator}

在绑定表达式中使用取反运算符（`!`），可以在布尔属性为 `false` 时应用某个类。想在两个互斥的类之间切换、又不愿为此多加一个视图模型属性时，这招很好用：

```xml
<TextBlock Classes.classA="{Binding IsOptionA}"
           Classes.classB="{Binding !IsOptionA}" />
```

本例中，`IsOptionA` 为 `true` 时应用 `classA`，`IsOptionA` 为 `false` 时则应用 `classB`。

## Example

本例定义了两条带类选择器的样式，分别把 `TextBlock` 的背景设为红色和绿色。当某一项的 `IsClass1` 属性为 `true` 时，`Classes.class1` 绑定会赋上 `class1`；借助取反运算符，`IsClass1` 为 `false` 时则赋上 `class2`。

```xml
<StackPanel Margin="20">
  <ListBox ItemsSource="{Binding ItemList}">
    <ListBox.Styles>
      <Style Selector="TextBlock.class1">
        <Setter Property="Background" Value="OrangeRed" />
      </Style>
      <Style Selector="TextBlock.class2">
        <Setter Property="Background" Value="PaleGreen" />
      </Style>
    </ListBox.Styles>
    <ListBox.ItemTemplate>
      <DataTemplate>
        <StackPanel>
          <TextBlock
              Classes.class1="{Binding IsClass1}"
              Classes.class2="{Binding !IsClass1}"
              Text="{Binding Title}"/>
        </StackPanel>
      </DataTemplate>
    </ListBox.ItemTemplate>
  </ListBox>
</StackPanel>
```

```csharp title='MainWindowViewModel.cs'
public class MainWindowViewModel : ViewModelBase
{
    public ObservableCollection<ItemClass> ItemList { get; set; }

    public MainWindowViewModel()
    {
        ItemList = new ObservableCollection<ItemClass>(new List<ItemClass>
        {
            new ItemClass("Item 1", false),
            new ItemClass("Item Two", false),
            new ItemClass("Third Item", true),
            new ItemClass("Item #4", false),
        });
    }
}
```

```csharp title='ItemClass.cs'
public class ItemClass
{
    public string Title { get; set; }
    public bool IsClass1 { get; set; }

    public ItemClass(string title, bool isClass1)
    {
        Title = title;
        IsClass1 = isClass1;
    }
}
```

<Image light={BindStyleClassSampleScreenshot} alt="Sample app showing style classes toggled by data binding" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [Styles](/docs/styling/styles)
- [数据绑定语法](/docs/data-binding/data-binding-syntax)
