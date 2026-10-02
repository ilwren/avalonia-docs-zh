---
id: virtualkeyboardscope
title: VirtualKeyboardScope
description: 一个容器控件，能根据输入焦点自动显示和隐藏虚拟键盘。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

`VirtualKeyboardScope` 控件是一个容器，能根据输入焦点自动管理[虚拟键盘](/controls/input/text-input/virtualkeyboard)的显示隐藏。当作用域内的文本输入控件获得焦点时，键盘出现；当焦点转到非文本控件或完全失去焦点时，键盘隐去。


:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 概述 {#overview}

把虚拟键盘集成进应用，推荐用 `VirtualKeyboardScope`。它带来一种浑然天成的体验：键盘只在需要时出现。它还会打理输入焦点和位置，免得键盘挡住正在使用的输入控件。

## 属性 {#properties}

| 属性 | 类型 | 说明 |
|----------|------|-------------|
| `InputMethods` | `IEnumerable\<VirtualKeyboardInputMethod>` | 获取或设置可供用户使用的输入法集合。 |

## 用法示例 {#usage-examples}

### 最简实现 {#minimal-implementation}

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <VirtualKeyboardScope InputMethods="en-US:kbd:standard">
        <StackPanel>
            <TextBlock>Enter your name:</TextBlock>
            <TextBox />
            <TextBlock>Comments:</TextBlock>
            <TextBox AcceptsReturn="True" Height="100" />
        </StackPanel>
    </VirtualKeyboardScope>
</Window>
```

### 多种输入法 {#multiple-input-methods}

```xml
<VirtualKeyboardScope InputMethods="en-US:kbd:standard, de:kbd:standard, ja:ime:kana">
    <StackPanel>
        <TextBox PlaceholderText="Type here" />
        <TextBlock>The keyboard will support English, German, and Japanese input</TextBlock>
    </StackPanel>
</VirtualKeyboardScope>
```

### 动态绑定 `InputMethods` {#binding-inputmethods-dynamically}

```xml
<VirtualKeyboardScope InputMethods="{Binding SelectedInputMethods}">
    <StackPanel>
        <TextBox />
        <ListBox ItemsSource="{Binding AvailableInputMethods}"
                 SelectionMode="Multiple"
                 Selection="{Binding SelectedInputMethodsCollection}" />
    </StackPanel>
</VirtualKeyboardScope>
```

### 在代码隐藏中配置 {#code-behind-configuration}

```csharp
// Get input methods for specific languages using SelectMany + ToList
var inputMethods = new[] { "en-US", "ja", "de" }
    .SelectMany(VirtualKeyboardInputMethod.GetInputMethodsForLanguage)
    .ToList();

// Assign to the VirtualKeyboardScope
myKeyboardScope.InputMethods = inputMethods;
```

## 配合 `TextInputOptions` 使用 {#working-with-textinputoptions}

通过 `TextInputOptions` 附加属性，可以定制输入字段与虚拟键盘的互动方式：

```xml
<VirtualKeyboardScope InputMethods="en-US:kbd:standard">
    <StackPanel>
        <TextBox TextInputOptions.ContentType="Email" 
                 PlaceholderText="Enter email address" />
                 
        <TextBox TextInputOptions.ContentType="Digits"
                 TextInputOptions.ReturnKeyType="Done"
                 PlaceholderText="Enter PIN code" />
                 
        <TextBox TextInputOptions.ReturnKeyType="Search"
                 PlaceholderText="Search..." />
    </StackPanel>
</VirtualKeyboardScope>
```

## 多个键盘 {#multiple-keyboards}

应用中可以摆放多个 `VirtualKeyboardScope` 控件。但同一时刻只会显示一个键盘，即当前持有焦点的那个作用域所对应的键盘。

```xml
<Grid ColumnDefinitions="*, *">
    <!-- First scope with English and German -->
    <VirtualKeyboardScope Grid.Column="0" InputMethods="en-US:kbd:standard, de:kbd:standard">
        <StackPanel>
            <TextBlock>Form 1</TextBlock>
            <TextBox />
        </StackPanel>
    </VirtualKeyboardScope>
    
    <!-- Second scope with English and Japanese -->
    <VirtualKeyboardScope Grid.Column="1" InputMethods="en-US:kbd:standard, ja:ime:kana">
        <StackPanel>
            <TextBlock>Form 2</TextBlock>
            <TextBox />
        </StackPanel>
    </VirtualKeyboardScope>
</Grid>
```

## 实践建议 {#best-practices}

- **把作用域放在合适的层级。** 请把 `VirtualKeyboardScope` 放在 `Window` 或 `UserControl` 的根部，或者放在能把所有应触发键盘的文本输入控件都包住的那一层。
- **挑选合适的输入法。** 提供与目标用户相称的输入法。应用支持的每个地区，至少都该配上一种语言布局。
- **为变窄的屏幕留余地。** 键盘出现时，`VirtualKeyboardScope` 会自动滚动，让获得焦点的输入框保持可见。不过你可能仍需调整布局，好让键盘在屏幕上时内容依然可用。
- **善用只读和禁用状态。** 对只读或已禁用的文本输入控件，键盘不会出现。若某段文本应当可选但不可编辑，请使用 `IsReadOnly="True"`。

## 实用提示 {#practical-notes}

- `VirtualKeyboardScope` 多用于自助终端和嵌入式 Linux 这类没有实体键盘的场景。在配有硬件键盘的桌面平台上，用户是看不到屏幕键盘的。
- 若你想完全掌控键盘在布局中的位置，请改用独立的 [`VirtualKeyboard` 控件](/controls/input/text-input/virtualkeyboard/virtualkeyboard-control)。
- `InputMethods` 属性既接受以逗号分隔的字符串（比如 `"en-US:kbd:standard, de:kbd:standard"`），也接受绑定来的 `VirtualKeyboardInputMethod` 对象集合。快速原型用字符串形式，可用语言在运行时才确定的则用绑定形式。

## 另请参阅 {#see-also}

- [VirtualKeyboard](/controls/input/text-input/virtualkeyboard/virtualkeyboard-control) —— 手动摆放键盘
- [TextBox](/controls/input/text-input/textbox) —— 标准的文本输入控件。