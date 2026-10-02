---
id: content-templates
title: 内容模板
description: 用 ContentTemplate 属性定义控件如何展示数据对象。
doc-type: explanation
---

import ContentTemplateStudentScreenshot from '/img/concepts/data-concepts/data-templates/content-templates/contenttemplate-student.png';

数据模板的用处在于：它告诉 _Avalonia UI_，对于你自己定义的类所创建的对象（既不是控件，也不是简单的字符串），应当怎样把它显示出来。

使用数据模板分两步走：

1. 定义数据模板
2. 为内容挑选数据模板

用法之一，是直接设置控件的 `ContentTemplate` 属性。窗口也适用（因为它和其他控件一样，都继承自 `ContentControl`）。

你可以用 `DataTemplate` 标签，搭配若干内置控件和绑定，定义一个（不针对特定类的）数据模板。例如：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:local="using:MySample"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d" d:DesignWidth="800" d:DesignHeight="450"
        x:Class="MySample.MainWindow"
        Title="MySample">
  <Window.ContentTemplate>
    <DataTemplate DataType="{x:Type local:Student}">
      <StackPanel>
        <Grid ColumnDefinitions="Auto,Auto" RowDefinitions="Auto,Auto">
          <TextBlock Grid.Row="0" Grid.Column="0">First Name:</TextBlock>
          <TextBlock Grid.Row="0" Grid.Column="1" Text="{Binding FirstName}"/>
          <TextBlock Grid.Row="1" Grid.Column="0">Last Name:</TextBlock>
          <TextBlock Grid.Row="1" Grid.Column="1" Text="{Binding LastName}"/>
        </Grid>
      </StackPanel>
    </DataTemplate>
  </Window.ContentTemplate>
  
  <local:Student FirstName="Jane" LastName="Deer"/>
</Window>
```

上面这些绑定，引用的是窗口内容区里那个对象的属性 —— 不管它是哪个类。这里窗口内容仍是你之前用过的那个学生对象；但运行这段代码时，_Avalonia UI_ 显示的是：

<Image light={ContentTemplateStudentScreenshot} alt="Window displaying student first and last name using a content template" position="center" maxWidth={400} cornerRadius="true"/>

这样使用数据模板，等于在同一处地方既定义了模板、又为内容选定了模板 —— 都是通过直接设置窗口的 `ContentTemplate` 属性完成的。

这段代码能跑通，是因为窗口内容区里的对象恰好具备绑定中指定的那些属性。不妨做个练习：加一个绑定，指向学生类上并不存在的属性。（应用照样能跑，只是会忽略找不到的那个属性。）

下一页你会看到如何定义多个数据模板，并根据窗口内容区中对象的类自动挑选正确的那个。

## 另请参阅 {#see-also}

- [控件内容](/docs/data-templates/control-content)：控件如何显示非控件内容。
- [数据模板集合](/docs/data-templates/data-template-collection)：按类型定义多个模板。
- [在代码中创建数据模板](/docs/data-templates/creating-data-templates-in-code)：实现 `IDataTemplate` 与使用 `FuncDataTemplate<T>`。
