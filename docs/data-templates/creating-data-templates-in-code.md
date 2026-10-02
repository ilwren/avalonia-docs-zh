---
id: creating-data-templates-in-code
title: 在代码中创建数据模板
description: 用 FuncDataTemplate 或自行实现 IDataTemplate，在 C# 中创建数据模板。
doc-type: how-to
---

## `FuncDataTemplate`

_Avalonia UI_ 支持在代码中创建数据模板。用实现了 [`IDataTemplate`](/api/avalonia/controls/templates/idatatemplate) 接口的 `FuncDataTemplate<T>` 类即可。

最简单的做法，是给 `FuncDataTemplate<T>` 构造函数传一个创建控件的 lambda 函数，就像这样：

```csharp
var template = new FuncDataTemplate<Student>((value, namescope) =>
    new TextBlock
    {
        [!TextBlock.TextProperty] = new ReflectionBinding("FirstName"),
    });
```

它等价于下面这段 XAML：

```xml
<DataTemplate DataType="{x:Type local:Student}">
    <TextBlock Text="{Binding FirstName}"/>
</DataTemplate>
```

## 在代码中做更精细的控制 {#taking-more-control-in-code}

如果你需要对代码中的数据模板做更精细的控制，可以自己写一个类来实现 `IDataTemplate` 接口。这样你想怎么呈现绑定数据类型的属性都行。

要使用 `IDataTemplate` 接口，你的数据模板类必须实现以下两个成员：

* `public bool Match(object data) { ... }` —— 实现该成员，判断传入的绑定数据是否与你的 `IDataTemplate` 相符。类型匹配就返回 true，否则返回 false。
* `public Control Build(object param) { ... }` —— 实现该成员，构建并返回用于呈现数据的控件。

## Example

下面是 `IDataTemplate` 接口的一个简单实现，它把字符串数据显示在文本块里：

```csharp
using Avalonia.Controls.Templates;
...
public class MyDataTemplate : IDataTemplate
{
    public Control Build(object param)
    {
        return new TextBlock() { Text = (string)param };
    }

    public bool Match(object data)
    {
        return data is string;
    }
}
```

现在就可以在视图中使用 `MyDataTemplate` 类了，像这样：

```xml
<!-- xmlns:dataTemplates="using:MyApp.DataTemplates" -->

<ContentControl Content="{Binding MyContent}">
	<ContentControl.ContentTemplate>
		<dataTemplates:MyDataTemplate />
	</ContentControl.ContentTemplate>
</ContentControl>
```

## 更多示例 {#more-examples}

[`FuncDataTemplate<T>` 类的进阶用法](https://github.com/AvaloniaUI/Avalonia.Samples/blob/main/src/Avalonia.Samples/DataTemplates/FuncDataTemplateSample)。

[`IDataTemplate` 接口的进阶实现](https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/DataTemplates/IDataTemplateSample)。

## 另请参阅 {#see-also}

- [数据模板入门](/docs/data-templates/introduction-to-data-templates)：Avalonia 数据模板总览。
- [数据模板集合](/docs/data-templates/data-template-collection)：按类型定义多个模板。
- [视图定位器](/docs/data-templates/view-locator)：为视图模型自动解析对应视图。
