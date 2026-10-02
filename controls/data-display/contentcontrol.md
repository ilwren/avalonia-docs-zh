---
id: contentcontrol
title: ContentControl
description: 一个基础控件，用于显示单块内容：可以是字符串、控件，也可以是经数据模板渲染的绑定对象。
doc-type: reference
---

import ControlContentStudentScreenshot from '/img/controls/contentcontrol/contentcontrol-student.png';

[`ContentControl`](/api/avalonia/controls/contentcontrol) 是一个显示单块内容的控件。内容可以是字符串、控件，也可以是经 `DataTemplate` 渲染的绑定对象。Avalonia 中许多常用控件都继承自 `ContentControl`，包括 `Button`、`Window` 和 `UserControl`，所以弄懂它的运作方式是构建 Avalonia 应用的基本功。

## 常用属性 {#common-properties}

下面这些属性你多半会经常用到：

| 属性 | 说明 |
|---|---|
| `Content` | 要在控件中显示的内容。 |
| `ContentTemplate` | 用于渲染 `Content` 对象的 `DataTemplate`。 |
| `HorizontalContentAlignment` | 控制内容在控件内的水平对齐方式。 |
| `VerticalContentAlignment` | 控制内容在控件内的垂直对齐方式。 |

## 显示内容 {#displaying-content}

最简单的情形下，`ContentControl` 直接显示你赋给它 [`Content`](/api/avalonia/controls/contentcontrol#content-property) 属性的数据。

例如：

```xml
<ContentControl Content="Hello World!"/>
```

这会显示字符串「Hello World!」。由于 `Content` 是该控件的默认（内容）属性，你也可以写成：

```xml
<ContentControl>Hello World!</ContentControl>
```

### 承载子控件 {#hosting-a-child-control}

如果你把一个控件赋给 `ContentControl`，它就会直接渲染那个控件：

```xml
<ContentControl>
  <Button>Click Me!</Button>
</ContentControl>
```

`ContentControl` 只能容纳一个直接子元素。要显示多个元素，请把它们装进 `StackPanel`、`Grid` 之类的布局面板：

```xml
<ContentControl>
  <StackPanel>
    <TextBlock Text="Line one" />
    <TextBlock Text="Line two" />
  </StackPanel>
</ContentControl>
```

### 用模板呈现内容 {#displaying-content-with-templates}

`ContentControl` 与数据绑定、数据模板搭配时尤其好用。设置 `ContentTemplate` 属性，就能掌控一个绑定的数据对象如何呈现。比如有下面这些视图模型：

```csharp
namespace Example
{
    public class MainWindowViewModel : ViewModelBase
    {
        object content = new Student("Jane", "Deer");

        public object Content
        {
            get => content;
            set => this.RaiseAndSetIfChanged(ref content, value);
        }
    }

    public class Student
    {
        public Student(string firstName, string lastName)
        {
            FirstName = firstName;
            LastName = lastName;
        }

        public string FirstName { get; }
        public string LastName { get; }
    }
}
```

> 注意：下面的示例都假定窗口的 `DataContext` 已被赋为一个 `MainWindowViewModel` 实例。详情请参阅 [`DataContext` 一节](/docs/data-binding/data-context)。

借助 `ContentTemplate` 属性，你可以在 `ContentControl` 中显示这名学生的姓和名：

```xml
<Window xmlns="https://github.com/avaloniaui">
  <ContentControl Content="{Binding Content}">
    <ContentControl.ContentTemplate>
      <DataTemplate>
        <Grid ColumnDefinitions="Auto,Auto" RowDefinitions="Auto,Auto">
          <TextBlock Grid.Row="0" Grid.Column="0">First Name:</TextBlock>
          <TextBlock Grid.Row="0" Grid.Column="1" Text="{Binding FirstName}"/>
          <TextBlock Grid.Row="1" Grid.Column="0">Last Name:</TextBlock>
          <TextBlock Grid.Row="1" Grid.Column="1" Text="{Binding LastName}"/>
        </Grid>
      </DataTemplate>
    </ContentControl.ContentTemplate>
  </ContentControl>
</Window>
```

<Image light={ControlContentStudentScreenshot} alt="Student first and last name" position="center" maxWidth={400} cornerRadius="true" />

更多内容请参阅[数据模板](/docs/data-templates/introduction-to-data-templates)页面。

### 动态切换内容 {#switching-content-dynamically}

由于 `Content` 是可绑定属性，你可以在运行时随时更换 `ContentControl` 所显示的东西。基于视图的导航常用这一招：把视图模型绑定到 `Content`，再用数据模板（或 `ViewLocator`）解析出对应的视图：

```xml
<ContentControl Content="{Binding CurrentPage}">
  <ContentControl.DataTemplates>
    <DataTemplate DataType="vm:HomeViewModel">
      <views:HomeView />
    </DataTemplate>
    <DataTemplate DataType="vm:SettingsViewModel">
      <views:SettingsView />
    </DataTemplate>
  </ContentControl.DataTemplates>
</ContentControl>
```

当视图模型把 `CurrentPage` 从 `HomeViewModel` 换成 `SettingsViewModel` 时，`ContentControl` 会自动渲染出匹配的视图。

若希望内容切换时带过渡动画，可以考虑改用 [`TransitioningContentControl`](/controls/data-display/transitioningcontentcontrol)。

## 另请参阅 {#see-also}

- [ContentControl API 参考](/api/avalonia/controls/contentcontrol)
- [GitHub 上的 `ContentControl.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ContentControl.cs)
- [数据模板](/docs/data-templates/introduction-to-data-templates)
- [`TransitioningContentControl`](/controls/data-display/transitioningcontentcontrol)
- [数据绑定](/docs/data-binding/data-context)
