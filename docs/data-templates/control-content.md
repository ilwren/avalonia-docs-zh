---
id: control-content
title: 控件内容
description: 理解控件如何显示非控件内容，以及为什么需要数据模板。
doc-type: explanation
---

import ControlContentButtonScreenshot from '/img/concepts/data-concepts/data-templates/control-content/content-button.png';
import ControlContentStringScreenshot from '/img/concepts/data-concepts/data-templates/control-content/content-string.png';
import ControlContentTypeScreenshot from '/img/concepts/data-concepts/data-templates/control-content/content-type.png';

把一个按钮控件放进 _Avalonia UI_ 窗口的内容区，会是什么效果，你多半已经见过了。

:::info
关于 _Avalonia UI_ 控件各个区域的更多说明，请见[布局](/docs/layout/)。
:::

例如：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d" d:DesignWidth="800" d:DesignHeight="450"
        x:Class="MySample.MainWindow"
        Title="MySample">
  <Button HorizontalAlignment="Center" >Hello World!</Button>
</Window>
```

窗口把按钮显示了出来 —— 这里水平方向居中（显式指定的），垂直方向也居中（默认行为）。看起来是这样：

<Image light={ControlContentButtonScreenshot} alt="Window displaying a centered Hello World button" position="center" maxWidth={400} cornerRadius="true"/>

如果往窗口内容区里放一个字符串，比如：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
        xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
        mc:Ignorable="d" d:DesignWidth="800" d:DesignHeight="450"
        x:Class="MySample.MainWindow"
        Title="MySample">
  Hello World!
</Window>
```

窗口就会把这个字符串显示出来：

<Image light={ControlContentStringScreenshot} alt="Window displaying a Hello World string" position="center" maxWidth={400} cornerRadius="true"/>

可要是你想在窗口里显示一个自定义类的对象，又会怎样？

比如说，有这样一个类定义 `Student`

```csharp
namespace MySample
{
    public class Student
    {
        public string FirstName { get; set;} = String.Empty;
        public string LastName { get; set;} = String.Empty;
    }
}
```

再把 XML 命名空间 `local` 定义为（前面那个）`MySample` 命名空间，就可以在窗口内容区里定义一个学生对象，像这样：

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:local="using:MySample"
        x:Class="MySample.Views.MainWindow">
  <local:Student FirstName="Jane" LastName="Deer"/>
</Window>
```

但你看到的只有学生对象的完全限定类名：

<Image light={ControlContentTypeScreenshot} alt="Window displaying the fully-qualified class name of a Student object" position="center" maxWidth={400} cornerRadius="true"/>

这可帮不上什么忙！之所以如此，是因为 _Avalonia UI_ 并不知道 `Student` 类的对象该怎么显示 —— 它又不是控件 —— 于是只好退回到 `.ToString()` 方法，你看到的也就只有完全限定类名了。

## 另请参阅 {#see-also}

- [内容模板](/docs/data-templates/content-templates)：用 `ContentTemplate` 定义数据的显示方式。
- [数据模板集合](/docs/data-templates/data-template-collection)：按类型定义多个模板。
- [数据模板入门](/docs/data-templates/introduction-to-data-templates)：Avalonia 数据模板总览。
