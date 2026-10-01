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

If you assign a control to a `ContentControl`, it renders that control directly:

```xml
<ContentControl>
  <Button>Click Me!</Button>
</ContentControl>
```

A `ContentControl` can hold only one direct child. If you need to display multiple elements, wrap them in a layout panel such as a `StackPanel` or `Grid`:

```xml
<ContentControl>
  <StackPanel>
    <TextBlock Text="Line one" />
    <TextBlock Text="Line two" />
  </StackPanel>
</ContentControl>
```

### Displaying content with templates

`ContentControl` becomes especially useful when you combine it with data binding and data templates. By setting the `ContentTemplate` property, you control how a bound data object is rendered visually. For example, given the following view models:

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

> Note: The following examples assume an instance of `MainWindowViewModel` is assigned to the window's `DataContext`. See [the section on `DataContext`](/docs/data-binding/data-context) for more information.

You can display the student's first and last name in a `ContentControl` using the `ContentTemplate` property:

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

For more information, see the [data templates](/docs/data-templates/introduction-to-data-templates) page.

### Switching content dynamically

Because `Content` is a bindable property, you can swap what a `ContentControl` displays at runtime. This pattern is commonly used for view-based navigation, where you bind a view model to `Content` and use data templates (or a `ViewLocator`) to resolve the appropriate view:

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

When your view model changes `CurrentPage` from a `HomeViewModel` to a `SettingsViewModel`, the `ContentControl` automatically renders the matching view.

If you want an animated transition when the content changes, consider using [`TransitioningContentControl`](/controls/data-display/transitioningcontentcontrol) instead.

## 另请参阅 {#see-also}

- [ContentControl API reference](/api/avalonia/controls/contentcontrol)
- [GitHub 上的 `ContentControl.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ContentControl.cs)
- [数据模板](/docs/data-templates/introduction-to-data-templates)
- [`TransitioningContentControl`](/controls/data-display/transitioningcontentcontrol)
- [Data binding](/docs/data-binding/data-context)
