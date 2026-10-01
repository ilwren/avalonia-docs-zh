---
id: introduction-to-data-templates
title: 数据模板入门
description: 用数据模板定义 Avalonia 如何显示数据对象，包括类型匹配与复用。
doc-type: overview
---

Avalonia 中的数据模板定义了数据的视觉表现：它规定数据对象在界面上如何呈现、如何排布。本文介绍数据模板，并演示如何在你的应用中使用它们。

## 什么是数据模板？ {#what-is-a-data-template}

说到底，数据模板就是一份可复用的定义，规定了某一类型的数据该如何呈现 —— 包括数据显示在用户界面上时的视觉结构和外观。在 Avalonia 中，数据模板常与列表类控件（如 [`ListBox`](/api/avalonia/controls/listbox) 或 `ItemsControl`）搭配使用，负责渲染该控件中的每一个数据项。

## 给 ListBox 套用数据模板 {#applying-a-data-template-to-a-listbox}

要给 `ListBox` 套用数据模板，通常用控件的 `ItemTemplate` 属性。 

举例来说，若有一个 `ListBox` 要用已定义的数据模板来显示一组 `Item` 对象，可以这样设置 `ItemTemplate` 属性：

```xml
<ListBox ItemsSource="{Binding Items}">
  <ListBox.ItemTemplate>
    <DataTemplate>
        <StackPanel Orientation="Horizontal">
            <TextBlock Text="{Binding Name}" />
            <Image Source="{Binding ImageSource}" />
        </StackPanel>
    </DataTemplate>
  </ListBox.ItemTemplate>
</ListBox>
```

本例中，数据模板用一个 `StackPanel` 容器定义视觉布局。`StackPanel` 内部有一个绑定到数据项 `Name` 属性的 `TextBlock`，以及一个绑定到 `ImageSource` 属性的 `Image` 控件。

## 针对特定类型的数据模板 {#type-specific-data-templates}

用 `DataType` 可以根据待显示对象的类型自动挑选模板：

```xml
<Window.DataTemplates>
    <DataTemplate DataType="{x:Type local:Customer}">
        <StackPanel Orientation="Horizontal" Spacing="8">
            <TextBlock Text="{Binding Name}" FontWeight="Bold" />
            <TextBlock Text="{Binding Email}" Foreground="Gray" />
        </StackPanel>
    </DataTemplate>

    <DataTemplate DataType="{x:Type local:Product}">
        <StackPanel Orientation="Horizontal" Spacing="8">
            <TextBlock Text="{Binding ProductName}" />
            <TextBlock Text="{Binding Price, StringFormat='${0:F2}'}" />
        </StackPanel>
    </DataTemplate>
</Window.DataTemplates>
```

当 Avalonia 在某个内容区域里遇到一个对象时，会按类型搜寻匹配的 `DataTemplate`。搜索从该控件开始，沿树向上直到找到匹配为止。

## 数据模板可以定义在哪里 {#where-data-templates-can-be-defined}

| 位置 | 作用范围 |
|---|---|
| `Control.DataTemplates` | 该控件及其子元素可用。 |
| `Window.DataTemplates` | 整个窗口可用。 |
| `Application.DataTemplates` | 整个应用可用。 |
| `ContentTemplate` property | 直接应用于某个特定的 `ContentControl`。 |
| `ItemTemplate` property | 应用于列表或集合类控件中的每一项。 |

## 定义在资源中的数据模板 {#data-templates-in-resources}

把可复用的模板定义成资源：

```xml
<Application.Resources>
    <DataTemplate x:Key="CustomerTemplate" DataType="{x:Type local:Customer}">
        <TextBlock Text="{Binding Name}" />
    </DataTemplate>
</Application.Resources>
```

然后这样引用它：

```xml
<ContentControl Content="{Binding SelectedCustomer}"
                ContentTemplate="{StaticResource CustomerTemplate}" />
```

## 另请参阅 {#see-also}

- [控件内容](/docs/data-templates/control-content)：控件如何显示非控件内容。
- [内容模板](/docs/data-templates/content-templates)：直接使用 `ContentTemplate`。
- [数据模板集合](/docs/data-templates/data-template-collection)：按类型定义多个模板。
- [复用数据模板](/docs/data-templates/reusing-data-templates)：在整个应用中共享模板。
