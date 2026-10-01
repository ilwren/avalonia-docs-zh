---
id: text-input
title: 文本输入与输入法
---

Avalonia 支持来自键盘、屏幕键盘以及输入法编辑器（IME）的文本输入，后者服务于中文、日文、韩文这类需要组字的语言。

## 文本输入的运作方式 {#how-text-input-works}

Avalonia 中的文本输入要经过这么几个阶段：

1. **KeyDown/KeyUp 事件**在原始按键按下时触发。
2. 平台的输入法把按键组合处理成字符。
3. **TextInput 事件**带着最终组好的文本触发。

多数应用都不必自己处理文本输入，[`TextBox`](/api/avalonia/controls/textbox) 和 `AutoCompleteBox` 这类控件会自动把一切都安排好。本页讲的是你需要自定义文本输入行为的那些场景。

## TextInput 事件 {#textinput-event}

`TextInput` 事件送来的是经输入法处理后组好的文本。`KeyDown` 给出的是按下的物理按键，而 `TextInput` 给出的则是用户真正想输入的那个（或那些）字符：

```csharp
myControl.AddHandler(InputElement.TextInputEvent, OnTextInput);

private void OnTextInput(object? sender, TextInputEventArgs e)
{
    // e.Text contains the composed character(s)
    if (e.Text is not null)
    {
        ProcessInput(e.Text);
    }
}
```

### 何时用 TextInput、何时用 KeyDown {#when-to-use-textinput-vs-keydown}

| 场景 | 用法 |
|---|---|
| 处理输入的字符（文本编辑） | `TextInput` |
| 检测修饰键（Ctrl+S、Alt+F4） | `KeyDown` |
| 处理方向键、Enter、Esc | `KeyDown` |
| 顾及输入法的文本处理 | `TextInput` |

:::tip
若你靠处理 `KeyDown` 来获取输入的文本，就会漏掉输入法组出的字符，还可能把死键（重音组合）处理错。字符输入请一律用 `TextInput`。
:::

## 输入法编辑器（IME） {#input-method-editors-ime}

输入法让用户能通过多次按键组字，从而输入复杂的文字体系。比如在中文输入法里敲「ni hao」就能打出「你好」。

### TextBox 中的输入法组字 {#ime-composition-in-textbox}

`TextBox` 开箱即支持输入法组字。组字过程中：
- 正在输入中的文本会带下划线显示
- 用户可以从候选字中挑选
- 按 Enter 或选中候选项即可上屏

无需任何额外配置。

### 在自定义控件上启用输入法 {#enabling-ime-on-custom-controls}

若你要写一个自定义的文本输入控件，就得实现 `ITextInputMethodClient` 并把它注册到文本输入法系统中：

```csharp
public class MyTextControl : Control, ITextInputMethodClient
{
    protected override void OnGotFocus(GotFocusEventArgs e)
    {
        base.OnGotFocus(e);
        var method = TopLevel.GetTopLevel(this)?.TextInputMethod;
        method?.SetClient(this);
    }

    protected override void OnLostFocus(RoutedEventArgs e)
    {
        base.OnLostFocus(e);
        var method = TopLevel.GetTopLevel(this)?.TextInputMethod;
        method?.SetClient(null);
    }

    // ITextInputMethodClient implementation
    public bool SupportsPreedit => true;
    public bool SupportsSurroundingText => false;

    public void SetPreeditText(string? preeditText)
    {
        // Display the in-progress composition text
    }

    // Additional interface members...
}
```

### 从自定义控件呼出屏幕键盘 {#requesting-the-on-screen-keyboard-from-a-custom-control}

继承自 `TextInputMethodClient` 的自定义文本输入控件，可以通过引发 `InputPaneActivationRequested` 事件来请求屏幕键盘，平台会据此把输入面板显示出来：

```csharp
public class MyTextInputClient : TextInputMethodClient
{
    public void OnTapped()
    {
        // Request the platform to show the on-screen keyboard
        RaiseInputPaneActivationRequested();
    }
}
```

## 屏幕键盘 {#on-screen-keyboards}

在触摸设备和移动平台上，当文本输入控件获得焦点时，Avalonia 可以把平台自带的屏幕键盘显示出来。

### 控制键盘的显隐 {#controlling-keyboard-visibility}

用 `InputPane` 服务来监视或控制屏幕键盘：

```csharp
var inputPane = TopLevel.GetTopLevel(this)?.InputPane;
if (inputPane is not null)
{
    inputPane.StateChanged += (sender, e) =>
    {
        if (e.NewState == InputPaneState.Open)
        {
            // Adjust layout to accommodate keyboard
        }
    };
}
```

### 移动端的键盘类型 {#keyboard-types-on-mobile}

在 Android 和 iOS 上，`TextBox` 的 `InputScope` 属性可以提示系统该显示哪种键盘布局：

```xml
<!-- Numeric keyboard -->
<TextBox InputScope="Number" />

<!-- Email keyboard (with @ key) -->
<TextBox InputScope="EmailSmtpAddress" />

<!-- URL keyboard -->
<TextBox InputScope="Url" />

<!-- Phone dialer -->
<TextBox InputScope="TelephoneNumber" />
```

## 平台注意事项 {#platform-considerations}

| 特性 | Windows | macOS | Linux | Android/iOS | WebAssembly |
|---|---|---|---|---|---|
| 输入法支持 | Full | Full | 完整支持（通过 IBus/Fcitx） | 完整支持（平台原生输入法） | Partial |
| 屏幕键盘 | 触摸设备 | Touch Bar | 虚拟键盘 | Full | Browser-managed |
| 死键 | Supported | Supported | Supported | 不适用 | Browser-managed |

## 另请参阅 {#see-also}

- [键盘与快捷键](/docs/input-interaction/keyboard-and-hotkeys)：按键绑定与键盘快捷键。
- [输入面板](/docs/services/input-pane)：屏幕键盘服务。
- [TextBox 控件](/controls/input/text-input/textbox)：内置的文本输入控件。
