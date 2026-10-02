---
id: data-templates
title: 数据模板
description: WPF 与 Avalonia 在数据模板、类型匹配和模板存放位置上的差异。
doc-type: migration
---

Avalonia 的数据模板与 WPF 相仿，都用来定义数据对象的视觉呈现。核心概念一致，但在模板存放在哪、类型如何匹配，以及额外提供了哪些能力上，有几处关键差异。

## 模板的存放位置 {#template-storage}

在 WPF 中，数据模板通常放在 `ResourceDictionary` 里——可以挂在控件上、窗口上，或者放进 `App.xaml`：

```xml
<!-- WPF -->
<Window.Resources>
    <DataTemplate DataType="{x:Type viewmodels:FooViewModel}">
        <TextBlock Text="{Binding Name}" />
    </DataTemplate>
</Window.Resources>
```

在 Avalonia 中，数据模板不放在资源里，而是放进 [`DataTemplates`](/api/avalonia/controls/templates/datatemplates) 集合——每个 `Control` 和 `Application` 上都有这么一个集合：

```xml
<!-- Avalonia -->
<Window xmlns:viewmodels="using:MyApp.ViewModels">
    <Window.DataTemplates>
        <DataTemplate DataType="viewmodels:FooViewModel">
            <TextBlock Text="{Binding Name}" />
        </DataTemplate>
    </Window.DataTemplates>
</Window>
```

模板解析会沿视觉树向上走，逐个查看各控件的 `DataTemplates` 集合，最后回退到 `Application.DataTemplates`。这与 WPF 的资源查找类似，只是用了一个专门的集合，而非通用的资源字典。

## DataType 匹配 {#datatype-matching}

两个框架都支持按 `DataType` 匹配模板，不过 Avalonia 还多出几分 WPF 没有的本事：

- **接口匹配：**Avalonia 可以让 `DataType` 匹配某个接口，而 WPF 只支持具体类型。
- **派生类匹配：**Avalonia 会把模板匹配给指定 `DataType` 的派生类，而 WPF 要求类型完全一致。

正因为匹配规则更宽，集合中模板的先后顺序就变得要紧了。模板按声明顺序依次判定，所以越具体的模板越要往前放：

```xml
<Window.DataTemplates>
    <!-- Most specific first -->
    <DataTemplate DataType="viewmodels:SpecialItemViewModel">
        <Border Background="Gold">
            <TextBlock Text="{Binding Name}" />
        </Border>
    </DataTemplate>
    <!-- Base type or interface last -->
    <DataTemplate DataType="viewmodels:ItemViewModel">
        <TextBlock Text="{Binding Name}" />
    </DataTemplate>
</Window.DataTemplates>
```

注意在 WPF 中 `DataType` 用的是 `{x:Type}` 标记扩展，而在 Avalonia 中你直接把类型写成字符串即可。

## DataTemplateSelector 的替代方案 {#datatemplateselector-replacement}

在 WPF 中，你可以写一个 `DataTemplateSelector` 的子类，按自定义逻辑挑选模板：

```csharp
// WPF
public class MyTemplateSelector : DataTemplateSelector
{
    public DataTemplate TemplateA { get; set; }
    public DataTemplate TemplateB { get; set; }

    public override DataTemplate SelectTemplate(object item, DependencyObject container)
    {
        return item is SpecialItem ? TemplateA : TemplateB;
    }
}
```

Avalonia 没有 `DataTemplateSelector`，取而代之的是实现 `IDataTemplate` 接口，用途完全一样：

```csharp
// Avalonia
public class MyDataTemplate : IDataTemplate
{
    public Control? Build(object? data)
    {
        if (data is SpecialItem)
            return new Border { Background = Brushes.Gold, Child = new TextBlock { Text = "Special" } };

        return new TextBlock { [!TextBlock.TextProperty] = new ReflectionBinding("Name") };
    }

    public bool Match(object? data)
    {
        return data is ItemViewModel;
    }
}
```

之后你就能在 XAML 中直接用上这个自定义模板：

```xml
<Window.DataTemplates>
    <local:MyDataTemplate />
</Window.DataTemplates>
```

完整的可运行示例请见 [IDataTemplate 示例](https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/DataTemplates/IDataTemplateSample)。

## TreeDataTemplate

WPF 的 `HierarchicalDataTemplate` 在 Avalonia 中叫 `TreeDataTemplate`。二者功能等价，只是名字不同。

**WPF:**

```xml
<!-- WPF -->
<TreeView ItemsSource="{Binding RootNodes}">
    <TreeView.Resources>
        <HierarchicalDataTemplate DataType="{x:Type viewmodels:NodeViewModel}"
                                  ItemsSource="{Binding Children}">
            <TextBlock Text="{Binding Title}" />
        </HierarchicalDataTemplate>
    </TreeView.Resources>
</TreeView>
```

**Avalonia:**

```xml
<!-- Avalonia -->
<TreeView ItemsSource="{Binding RootNodes}">
    <TreeView.DataTemplates>
        <TreeDataTemplate DataType="viewmodels:NodeViewModel"
                          ItemsSource="{Binding Children}">
            <TextBlock Text="{Binding Title}" />
        </TreeDataTemplate>
    </TreeView.DataTemplates>
</TreeView>
```

注意 Avalonia 把模板放在 `DataTemplates` 里，而不是 `Resources` 中。

## ItemTemplate 与 ContentTemplate {#itemtemplate-and-contenttemplate}

`ItemsControl`、`ListBox` 等控件上的 `ItemTemplate` 属性，在两个框架中用法一致：赋一个 `DataTemplate` 即可控制每一项的渲染方式：

```xml
<ListBox ItemsSource="{Binding Items}">
    <ListBox.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal" Spacing="8">
                <Image Source="{Binding Icon}" Width="16" Height="16" />
                <TextBlock Text="{Binding DisplayName}" />
            </StackPanel>
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

同理，`ContentControl` 和 `ContentPresenter` 上的 `ContentTemplate` 也一如预期。若你没有显式设置 `ItemTemplate` 或 `ContentTemplate`，Avalonia 会沿树向上在各个 `DataTemplates` 集合中寻找匹配的模板，正如 WPF 会去资源里找一样。

## 用 x:DataType 启用编译绑定 {#xdatatype-for-compiled-bindings}

Avalonia 支持编译绑定：既能在编译期校验绑定路径，运行时性能也更好。WPF 没有与之对应的特性。

要在数据模板内启用编译绑定，请把 `x:DataType` 特性设为该模板将要接收的类型：

```xml
<DataTemplate DataType="viewmodels:FooViewModel"
              x:DataType="viewmodels:FooViewModel">
    <StackPanel>
        <!-- These bindings are validated at compile time -->
        <TextBlock Text="{Binding Name}" />
        <TextBlock Text="{Binding Description}" />
    </StackPanel>
</DataTemplate>
```

设了 `x:DataType` 之后，编译器会检查 `Name` 和 `Description` 是否真的存在于 `FooViewModel` 上。拼错或写错属性名会直接报构建错误，而不是到运行时才悄无声息地失效。

在 `.csproj` 文件里加上 `<AvaloniaUseCompiledBindingsByDefault>true</AvaloniaUseCompiledBindingsByDefault>`，即可为整个项目启用编译绑定，这样所有绑定都默认按 `x:DataType` 来要求。

## 另请参阅 {#see-also}

- [数据模板入门](/docs/data-templates/introduction-to-data-templates)
- [Data Template Collection](/docs/data-templates/data-template-collection)
- [Compiled Bindings](/docs/data-binding/compiled-bindings)
