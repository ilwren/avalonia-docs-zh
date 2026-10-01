---
id: data-template-collection
title: 数据模板集合
description: 在控件的 DataTemplates 集合中定义多个数据模板，按类型自动匹配。
doc-type: explanation
---

import DataTemplatesCollectionStudentScreenshot from '/img/concepts/data-concepts/data-templates/data-template-collection/datatemplates-collection-student.png';

_Avalonia UI_ 中每个控件都有一个 [`DataTemplates`](/api/avalonia/controls/templates/datatemplates) 集合，你可以往里放任意多个数据模板定义，之后便能按类类型挑选显示所用的模板。 

如果控件没有像上一页那样直接设置 `ContentTemplate` 属性，它就会从自己的 `DataTemplates` 集合里挑一个与待显示对象的类相匹配的模板。窗口也适用这条规则。

数据模板按类型匹配：待显示对象的类，与某个模板 `DataType` 属性中指定的完全限定类名一致时，即为匹配成功。

于是可以把前面的示例改成使用 `DataTemplates` 集合，如下：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:local="using:MySample"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d" d:DesignWidth="800" d:DesignHeight="450"
        x:Class="MySample.MainWindow"
        Title="MySample">
  <Window.DataTemplates>
    <DataTemplate DataType="{x:Type local:Student}">
      <Grid ColumnDefinitions="Auto,Auto" RowDefinitions="Auto,Auto">
        <TextBlock Grid.Row="0" Grid.Column="0">First Name:</TextBlock>
        <TextBlock Grid.Row="0" Grid.Column="1" Text="{Binding FirstName}"/>
        <TextBlock Grid.Row="1" Grid.Column="0">Last Name:</TextBlock>
        <TextBlock Grid.Row="1" Grid.Column="1" Text="{Binding LastName}"/>
      </Grid>
    </DataTemplate>
  </Window.DataTemplates>
  
  <local:Student FirstName="Jane" LastName="Deer"/>
</Window>
```

显示效果与上一页完全相同：

<Image light={DataTemplatesCollectionStudentScreenshot} alt="Window displaying student first and last name using a data template from the DataTemplates collection" position="center" maxWidth={400} cornerRadius="true"/>

## 按类型配置多个数据模板 {#multiple-data-templates-by-type}

`DataTemplates` 集合可以为不同类型选用不同的模板。Avalonia 遇到一个对象时，会在 `DataTemplates` 集合中搜寻 `DataType` 与该对象类型相符的模板：

```xml
<Window.DataTemplates>
    <DataTemplate DataType="{x:Type local:Student}">
        <StackPanel Orientation="Horizontal" Spacing="8">
            <TextBlock Text="🎓" />
            <TextBlock Text="{Binding FirstName}" />
            <TextBlock Text="{Binding LastName}" />
        </StackPanel>
    </DataTemplate>

    <DataTemplate DataType="{x:Type local:Teacher}">
        <StackPanel Orientation="Horizontal" Spacing="8">
            <TextBlock Text="📚" />
            <TextBlock Text="{Binding Name}" FontWeight="Bold" />
            <TextBlock Text="{Binding Subject}" Foreground="Gray" />
        </StackPanel>
    </DataTemplate>
</Window.DataTemplates>
```

定义好这些模板之后，显示 `Student` 对象的 `ListBox` 或 `ContentControl` 会用上第一个模板，而 `Teacher` 对象则用第二个：

```xml
<ListBox ItemsSource="{Binding People}" />
```

## 模板的搜索顺序 {#template-search-order}

当 Avalonia 需要为某个对象找数据模板时，会按以下顺序搜索：

1. 控件自身的 `DataTemplates` 集合。
2. 沿树向上，各级父控件的 `DataTemplates` 集合。
3. `Window.DataTemplates` 集合。
4. `Application.DataTemplates` 集合。

第一个匹配上的模板即被采用。因此你可以在树的任意一层覆盖应用级的模板。

## 另请参阅 {#see-also}

- [数据模板入门](/docs/data-templates/introduction-to-data-templates)：Avalonia 数据模板总览。
- [内容模板](/docs/data-templates/content-templates)：直接使用 `ContentTemplate`。
- [复用数据模板](/docs/data-templates/reusing-data-templates)：在整个应用中共享模板。
