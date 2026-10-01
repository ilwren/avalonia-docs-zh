---
id: reusing-data-templates
title: 复用数据模板
description: 把数据模板定义在 Application.DataTemplates 集合中，让它在所有窗口之间共享。
doc-type: explanation
---

import DataTemplatesScopeScreenshot from '/img/guides/data/data-templates/datatemplates-scope.png';

像上一页那样把数据模板定义在 `Window.DataTemplates` 集合里，它就能在整个窗口内复用。不过，你还可以把复用范围扩大到应用中的任意窗口。

这是因为 _Avalonia UI_ 挑选数据模板时，会沿逻辑树做层级搜索。搜索范围最大时，先从控件自身开始，再（递归地）扩展到各级父控件，接着查看窗口（即上一页的情形），最后还会到应用本身的数据模板集合里去找。

:::info
关于 _Avalonia UI_ 中逻辑树这一概念的更多说明，请见[界面组合](/docs/fundamentals/ui-composition)。
:::

因此，若希望某个模板在应用的任意窗口中都能复用，就把它定义在 app.axaml 文件的 `Application.DataTemplates` 集合里。

来看看实际效果。先添加另一个视图模型：

```csharp
namespace MySample
{
    public class Teacher
    {
        public string Name { get; set; } = String.Empty;
        public string Subject { get; set; } = String.Empty;
    }
}
```

再在 app.axaml 文件中，为 `Teacher` 类型添加一个数据模板：

```xml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:vm="using:MySample"
             x:Class="MySample.App"
             RequestedThemeVariant="Light">
    <Application.Styles>
        <FluentTheme />
    </Application.Styles>

  <Application.DataTemplates>
    <DataTemplate DataType="{x:Type vm:Teacher}">
      <Grid ColumnDefinitions="Auto,Auto" RowDefinitions="Auto,Auto">
        <TextBlock Grid.Row="0" Grid.Column="0">Name:</TextBlock>
        <TextBlock Grid.Row="0" Grid.Column="1" Text="{Binding Name}"/>
        <TextBlock Grid.Row="1" Grid.Column="0">Subject:</TextBlock>
        <TextBlock Grid.Row="1" Grid.Column="1" Text="{Binding Subject}"/>
      </Grid>
    </DataTemplate>
  </Application.DataTemplates>
</Application>
```

在窗口内容区里定义一个本地的 teacher 对象：

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
  
  <local:Teacher Name="Dr Jones" Subject="Maths"/>
</Window>
```

尽管窗口里并没有针对 teacher 的数据模板，Avalonia UI 依然会找到你定义在应用一级的那个模板，显示效果符合预期：

<Image light={DataTemplatesScopeScreenshot} alt="Window displaying a teacher name and subject using an application-level data template" position="center" maxWidth={400} cornerRadius="true"/>

:::caution
切记：无论数据模板定义在哪里，都要为它指定 `DataType` —— 因为一旦 _Avalonia UI_ 给你的数据找不到匹配的数据模板，界面上就什么都不会显示！
:::

## 另请参阅 {#see-also}

- [数据模板入门](/docs/data-templates/introduction-to-data-templates)：Avalonia 数据模板总览。
- [数据模板集合](/docs/data-templates/data-template-collection)：按类型定义多个模板。
- [在代码中创建数据模板](/docs/data-templates/creating-data-templates-in-code)：实现 `IDataTemplate` 与使用 `FuncDataTemplate<T>`。
