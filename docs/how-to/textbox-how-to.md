---
id: textbox-how-to
title: "操作指南：使用 TextBox"
description: Avalonia 中 TextBox 的校验、格式化、输入掩码、选择与自定义。
doc-type: how-to
---

本指南介绍 TextBox 的常见场景：校验、格式化、输入掩码、选择与自定义。

## Basic Text Binding

以 `TwoWay` 模式绑定 `Text` 属性（这也是 TextBox.Text 的默认模式）：

```xml
<TextBox Text="{Binding Username}" PlaceholderText="Enter username" />
```

```csharp
[ObservableProperty]
private string _username = "";
```

## Placeholder Text

TextBox 为空时显示提示文字：

```xml
<TextBox PlaceholderText="Search..." />
<TextBox PlaceholderText="Enter email address" />
```

用户一开始输入，占位文字就消失；文本被清空后它又会回来。

要自定义占位文字的颜色，请设置 `PlaceholderForeground`：

```xml
<TextBox PlaceholderText="Search..." PlaceholderForeground="Gray" />
```

占位文字默认以 50% 的不透明度渲染。覆盖 `TextControlPlaceholderOpacity` 主题资源即可全局调整，比如为了无障碍而提高对比度：

```xml
<Application.Resources>
    <x:Double x:Key="TextControlPlaceholderOpacity">0.7</x:Double>
</Application.Resources>
```

## Password Input

用 `PasswordChar` 把输入的字符遮起来：

```xml
<TextBox PasswordChar="*" PlaceholderText="Password" />
<TextBox PasswordChar="●" PlaceholderText="Password" />
```

若要做一个「显示密码」的切换按钮，请绑定 `RevealPassword`：

```xml
<Grid ColumnDefinitions="*,Auto">
    <TextBox x:Name="PasswordBox" PasswordChar="●" Text="{Binding Password}" />
    <ToggleButton Grid.Column="1" Content="Show"
                  IsChecked="{Binding #PasswordBox.RevealPassword}" />
</Grid>
```

## 多行输入 {#multi-line-input}

启用多行文本输入：

```xml
<TextBox AcceptsReturn="True"
         TextWrapping="Wrap"
         Height="120"
         PlaceholderText="Enter your message..." />
```

| 属性 | 效果 |
|---|---|
| `AcceptsReturn="True"` | 允许按 Enter 换行 |
| `TextWrapping="Wrap"` | 长行自动换行，而不是横向滚动 |
| `AcceptsTab="True"` | 允许按 Tab 插入制表符 |

## 只读与禁用 {#read-only-and-disabled}

```xml
<!-- Read-only: can select and copy, but not edit -->
<TextBox Text="{Binding DisplayValue}" IsReadOnly="True" />

<!-- Disabled: cannot interact at all -->
<TextBox Text="{Binding DisabledValue}" IsEnabled="False" />
```

## Text Selection

### 获得焦点时全选 {#select-all-on-focus}

TextBox 获得焦点时选中全部文本：

```csharp
private void OnTextBoxGotFocus(object? sender, GotFocusEventArgs e)
{
    if (sender is TextBox textBox)
    {
        textBox.SelectAll();
    }
}
```

```xml
<TextBox GotFocus="OnTextBoxGotFocus" Text="{Binding Value}" />
```

### 用代码控制选区 {#programmatic-selection}

```csharp
// Select a range
myTextBox.SelectionStart = 5;
myTextBox.SelectionEnd = 10;

// Select all
myTextBox.SelectAll();

// Get selected text
string selected = myTextBox.SelectedText;
```

## Input Validation

### 配合数据注解 {#with-data-annotations}

用 `INotifyDataErrorInfo` 把校验错误直接显示在 TextBox 上：

```csharp
public partial class FormViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyDataErrorInfo]
    [Required(ErrorMessage = "Email is required")]
    [EmailAddress(ErrorMessage = "Invalid email format")]
    private string _email = "";
}
```

```xml
<TextBox Text="{Binding Email}" PlaceholderText="Email" />
```

校验未通过时，TextBox 会显示红色边框和错误信息。详见[数据绑定中的校验](/docs/data-binding/binding-validation)。

### 限制可输入的字符 {#restricting-input-characters}

处理 `TextChanging` 事件来过滤输入：

```csharp
private void OnTextChanging(object? sender, TextChangingEventArgs e)
{
    // Allow only digits
    if (sender is TextBox textBox)
    {
        var newText = textBox.Text;
        if (newText is not null && !newText.All(char.IsDigit))
        {
            e.Cancel = true;
        }
    }
}
```

## Max Length

限制字符数量：

```xml
<TextBox MaxLength="50" PlaceholderText="Max 50 characters" />
```

## Text Changed Event

响应文本变化，做输入即搜索或实时预览：

```xml
<TextBox Text="{Binding SearchText}" />
```

```csharp
[ObservableProperty]
private string _searchText = "";

partial void OnSearchTextChanged(string value)
{
    ApplyFilter(value);
}
```

关于带防抖的搜索（避免每敲一个键就筛一次），请参阅[性能](/docs/app-development/performance#debouncing-rapid-input)。

## Inner Content (Left/Right)

用 `InnerLeftContent` 和 `InnerRightContent` 在 TextBox 内部放上图标或按钮：

```xml
<TextBox PlaceholderText="Search..." InnerLeftContent="🔍">
    <TextBox.InnerRightContent>
        <Button Content="✕" Command="{Binding ClearSearchCommand}"
                Background="Transparent" BorderThickness="0"
                Padding="4" />
    </TextBox.InnerRightContent>
</TextBox>
```

## 撤销与重做 {#undo-and-redo}

TextBox 支持标准快捷键（Ctrl+Z / Ctrl+Shift+Z）的撤销和重做，无需额外代码即可生效。

要清空撤销历史：

```csharp
myTextBox.Clear(); // Clears text and undo history
```

## Styling

### 自定义外观 {#custom-appearance}

```xml
<Style Selector="TextBox.custom">
    <Setter Property="Background" Value="#F8F8F8" />
    <Setter Property="BorderBrush" Value="#E0E0E0" />
    <Setter Property="BorderThickness" Value="1" />
    <Setter Property="CornerRadius" Value="8" />
    <Setter Property="Padding" Value="12,8" />
</Style>

<Style Selector="TextBox.custom:focus">
    <Setter Property="BorderBrush" Value="#6366F1" />
    <Setter Property="BorderThickness" Value="2" />
</Style>

<Style Selector="TextBox.custom:error">
    <Setter Property="BorderBrush" Value="#EF4444" />
</Style>
```

### 去掉聚焦时的边框 {#removing-the-focus-border}

```xml
<Style Selector="TextBox.borderless">
    <Setter Property="BorderThickness" Value="0" />
    <Setter Property="Background" Value="Transparent" />
</Style>

<Style Selector="TextBox.borderless:focus">
    <Setter Property="BorderThickness" Value="0" />
</Style>
```

## Context Menu

TextBox 自带含剪切、复制、粘贴的上下文菜单。要自定义它：

```xml
<TextBox Text="{Binding Value}">
    <TextBox.ContextMenu>
        <ContextMenu>
            <MenuItem Header="Cut" Command="{Binding $parent[TextBox].Cut}" InputGesture="Ctrl+X" />
            <MenuItem Header="Copy" Command="{Binding $parent[TextBox].Copy}" InputGesture="Ctrl+C" />
            <MenuItem Header="Paste" Command="{Binding $parent[TextBox].Paste}" InputGesture="Ctrl+V" />
            <Separator />
            <MenuItem Header="Select All" InputGesture="Ctrl+A" />
        </ContextMenu>
    </TextBox.ContextMenu>
</TextBox>
```

## See Also

- [TextBox 控件参考](/controls/input/text-input/textbox)：属性一览。
- [数据绑定中的校验](/docs/data-binding/binding-validation)：数据注解与 INotifyDataErrorInfo 校验。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定模式与各项参数。
