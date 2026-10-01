---
id: groupbox
title: GroupBox
description: 一个容器控件：用一圈边框和一个标题文字，把相关内容在视觉上归为一组。
doc-type: reference
---

[`GroupBox`](/api/avalonia/controls/groupbox) 控件用一圈边框和一个标题文字，把相关内容在视觉上归为一组。标题文字压在边框上沿，呈现出桌面界面框架里经典的「分组框」观感。

`GroupBox` 继承自 `HeaderedContentControl`，因此支持一个 `Header`（显示在边框顶部）和一个 `Content` 子元素。

## 常见用法 {#common-use-cases}

以下情况适合用 `GroupBox`：

- 把表单字段按逻辑分成若干区块（比如「个人信息」和「账单地址」）。
- 在视觉上区隔成组的相关选项，比如一组复选框或单选按钮。
- 给界面的某个区块加上带标签的外框，让这组控件的用途一目了然。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table><thead><tr><th width="261">Property</th><th>说明</th></tr></thead><tbody><tr><td><code>Header</code></td><td>显示在边框顶部的文字或内容。</td></tr><tr><td><code>Content</code></td><td>分组框内承载的子控件或布局。</td></tr><tr><td><code>BorderBrush</code></td><td>外圈边框的颜色。</td></tr><tr><td><code>BorderThickness</code></td><td>外圈边框的粗细。</td></tr><tr><td><code>CornerRadius</code></td><td>边框圆角的半径。</td></tr><tr><td><code>Padding</code></td><td>边框与内容之间的间距。</td></tr></tbody></table>

## Example

下面的例子用两个分组框来组织一个表单：

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Spacing="16" Margin="16">
  <GroupBox Header="Personal Details">
    <StackPanel Spacing="8">
      <TextBox PlaceholderText="First name" />
      <TextBox PlaceholderText="Last name" />
      <TextBox PlaceholderText="Email" />
    </StackPanel>
  </GroupBox>
  <GroupBox Header="Preferences">
    <StackPanel Spacing="8">
      <CheckBox Content="Receive notifications" />
      <CheckBox Content="Dark mode" />
    </StackPanel>
  </GroupBox>
</StackPanel>
```

</XamlPreview>

## 自定义标题内容 {#custom-header-content}

`Header` 属性接受任意内容，不限于文字。你可以用它显示图标、带格式的文本，或任何其他控件：

```xml
<GroupBox>
  <GroupBox.Header>
    <StackPanel Orientation="Horizontal" Spacing="6">
      <PathIcon Data="{StaticResource SettingsIcon}" />
      <TextBlock Text="Advanced Settings" FontWeight="Bold" />
    </StackPanel>
  </GroupBox.Header>
  <StackPanel Spacing="8">
    <CheckBox Content="Enable logging" />
    <CheckBox Content="Verbose output" />
  </StackPanel>
</GroupBox>
```

## 绑定标题 {#data-binding-the-header}

`Header` 属性可以绑定到视图模型的属性；当区块标签需要在运行时变化时，这很有用：

```xml
<GroupBox Header="{Binding SectionTitle}">
  <TextBlock Text="{Binding SectionContent}" />
</GroupBox>
```

```csharp
public class MyViewModel : ViewModelBase
{
    private string _sectionTitle = "Details";

    public string SectionTitle
    {
        get => _sectionTitle;
        set => this.RaiseAndSetIfChanged(ref _sectionTitle, value);
    }
}
```

## 嵌套分组框 {#nesting-group-boxes}

`GroupBox` 控件可以相互嵌套以划分子区块。嵌套层级尽量浅（一到两层），免得布局显得杂乱：

```xml
<GroupBox Header="Account">
  <StackPanel Spacing="12">
    <GroupBox Header="Login credentials">
      <StackPanel Spacing="8">
        <TextBox PlaceholderText="Username" />
        <TextBox PlaceholderText="Password" PasswordChar="*" />
      </StackPanel>
    </GroupBox>
    <GroupBox Header="Profile">
      <StackPanel Spacing="8">
        <TextBox PlaceholderText="Display name" />
        <TextBox PlaceholderText="Bio" />
      </StackPanel>
    </GroupBox>
  </StackPanel>
</GroupBox>
```

## Styling

`GroupBox` 的外观可以通过主题资源来定制：

| 资源 | 默认值 | 说明 |
|---|---|---|
| `GroupBoxPadding` | `4` | 内容四周的内边距。 |
| `GroupBoxHeaderFontSize` | `16` | 标题文字的字号。 |
| `GroupBoxHeaderMargin` | `0,4,0,12` | 标题四周的外边距。 |
| `GroupBoxBorderThickness` | `1` | 外圈边框的粗细。 |
| `GroupBoxBackground` | Transparent | 内容区的背景填充。 |
| `GroupBoxBorderBrush` | `SystemControlForegroundBaseMediumBrush` | 边框的颜色。 |
| `GroupBoxHeaderForeground` | `SystemBaseHighColor` | 标题文字的颜色。 |

## 另请参阅 {#see-also}

- [Border](/controls/layout/containers/border)
- [Expander](/controls/layout/containers/expander)
- [GroupBox API 参考](/api/avalonia/controls/groupbox)
- [GitHub 上的 `GroupBox.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/GroupBox.cs)
