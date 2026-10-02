---
id: virtualkeyboard-control
title: VirtualKeyboard 控件参考
tags:
  - avalonia pro
  - avalonia enterprise
---

import VirtualKeyboardStyles from '/img/avalonia-pro/virtual-keyboard/styles.png';

`VirtualKeyboard` 是一个独立的屏幕键盘控件，可以手动摆进应用布局中。`VirtualKeyboardScope` 会根据焦点自动管理键盘的显示隐藏，`VirtualKeyboard` 则不同——它明确指向某个特定的目标输入元素。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 概述 {#overview}

`VirtualKeyboard` 让你直接掌控键盘的位置和行为。不管焦点落在哪个控件上，它都把输入直接送给自己指定的目标。因此，当「随焦点自动弹出键盘」并不合适时，它就派上用场了。

## 属性 {#properties}

| 属性 | 类型 | 说明 |
|----------|------|-------------|
| `Target` | `IInputElement` | 获取或设置接收键盘按键的输入元素。 |
| `InputMethods` | `IEnumerable<VirtualKeyboardInputMethod>` | 获取或设置可供用户使用的输入法集合。 |

## 用法示例 {#usage-examples}

### 最简实现 {#minimal-implementation}

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <StackPanel>
        <TextBox x:Name="InputField" />
        <VirtualKeyboard Target="{Binding ElementName=InputField}"
                         InputMethods="en-US:kbd:standard" />
    </StackPanel>
</Window>
```

### 多种输入法 {#multiple-input-methods}

```xml
<StackPanel>
    <TextBox x:Name="EmailField" PlaceholderText="Email address" />
    <VirtualKeyboard Target="{Binding ElementName=EmailField}"
                     InputMethods="en-US:kbd:standard, de:kbd:standard, ja:ime:kana" />
</StackPanel>
```

### 在代码隐藏中配置 {#code-behind-configuration}

```csharp
// Get input methods for specific languages using SelectMany + ToList
var inputMethods = new[] { "en-US", "ja", "de" }
    .SelectMany(VirtualKeyboardInputMethod.GetInputMethodsForLanguage)
    .ToList();

// Create and configure a VirtualKeyboard
var keyboard = new VirtualKeyboard
{
    Target = myTextBox,
    InputMethods = inputMethods
};

// Add it to the visual tree
myContainer.Children.Add(keyboard);
```

## 配合 `TextInputOptions` 使用 {#working-with-textinputoptions}

`TextInputOptions` 附加属性可以加在目标元素上，用来定制键盘行为：

```xml
<StackPanel>
    <TextBox x:Name="EmailField" 
             TextInputOptions.ContentType="Email" 
             TextInputOptions.ReturnKeyType="Next" />
             
    <VirtualKeyboard Target="{Binding ElementName=EmailField}"
                     InputMethods="en-US:kbd:standard" />
</StackPanel>
```

## `VirtualKeyboard` 与 `VirtualKeyboardScope` 怎么选 {#when-to-use-virtualkeyboard-vs-virtualkeyboardscope}

### 这些情况下选 VirtualKeyboard： {#choose-virtualkeyboard-when}

- **目标固定**：无论焦点在哪，你都要让键盘始终指向某个特定的输入控件。
- **特殊输入场景**：你在打造自定义的输入体验，键盘目标并不由焦点决定。

### 这些情况下选 VirtualKeyboardScope： {#choose-virtualkeyboardscope-when}

- **常规输入**：你希望键盘自动跟随焦点。
- **集成更省事**：你更喜欢基于容器、配置项更少的方案。
- **自动显隐**：你希望键盘随焦点变化自动显示和隐藏。

## 实践建议 {#best-practices}

1. **设好有效的目标。**
   - 务必把 `Target` 属性设为一个能接收按键的有效输入元素。
   - 目标无效时，键盘的输入就无处可去了。

2. **摆放键盘要讲究。**
   - 把键盘放在不会遮挡重要内容的位置，通常是屏幕底部。
   - 与 `VirtualKeyboardScope` 不同，`VirtualKeyboard` 不会自动打理内容滚动，因此滚动或布局调整可能需要你自己处理。

3. **挑选合适的输入法。**
   - 选择与目标用户相称的输入法。
   - 面向国际化的应用，请把所有支持地区的布局都带上。

4. **控制内存占用。**
   - 若是动态创建键盘，用完后记得把它从视觉树中移除。

5. **做好自适应布局。**
   - 规划布局时要给键盘预留出位置。
   - 可以考虑用带行定义的 [`Grid`](/controls/layout/panels/grid) 为键盘划出空间。

## Styling

`VirtualKeyboard` 的样式通过具名资源来设定。你可以在应用中覆盖这些资源，以定制键盘各部分的外观。

### 可定制的资源 {#customizable-resources}

<Image light={VirtualKeyboardStyles} maxWidth={400} alignment="center" />

下面列出你可以在主题或资源字典中覆盖的资源：

| 按键 | 类型 | 默认值 |
|---|---|---|
| `KeyboardActionButtonBackground` | Brush | `Goldenrod` |
| `KeyboardActionButtonBackgroundPressed` | Brush | `PaleGoldenrod` |
| `KeyboardButtonBackground` | Brush | `GhostWhite` |
| `KeyboardButtonBackgroundPressed` | Brush | `FloralWhite` |
| `KeyboardButtonBorderBrush` | Brush | `Black` |
| `KeyboardButtonFontSize` | Double | `24` |
| `KeyboardButtonForeground` | Brush | `Black` |
| `KeyboardFunctionalButtonBackground` | Brush | `LightSteelBlue` |
| `KeyboardFunctionalButtonBackgroundPressed` | Brush | `LightBlue` |
| `KeyboardPaneBackground` | Brush | `DarkGray` |
| `KeyboardPanePadding` | Thickness |  `4` |
| `KeyboardPopupKeySelectedBackground` | Brush | `PaleTurquoise` |

### 如何覆盖 {#how-to-override}

要定制外观，请在应用主题或资源字典中定义这些资源。例如：

```xml
<SolidColorBrush x:Key="KeyboardButtonForeground" Color="#FF0000" />
```

### 示例：自定义主题 {#example-custom-theme}

```xml
<ResourceDictionary>
  <SolidColorBrush x:Key="KeyboardPaneBackground" Color="#FFD700" />
  <system:Double x:Key="KeyboardButtonFontSize">36</system:Double>
  <!-- Add more overrides as needed -->
</ResourceDictionary>
```

## 输入法 {#input-methods}

| 标识符 | 说明 | 注释支持情况 |
| --- | --- | --- |
|`af:kbd:standard` | Afrikaans | |
|`ar:kbd:standard` | Arabic | |
|`hy-AM:kbd:standard` | Armenian (Armenia) Phonetic | |
|`az-AZ:kbd:standard` | Azerbaijani (Azerbaijan) | |
|`eu-ES:kbd:standard` | Basque (Spain) | |
|`be-BY:kbd:standard` | Belarusian (Belarus) | |
|`bn-BD:kbd:standard` | Bengali (Bangladesh) | |
|`bn-IN:kbd:standard` | Bengali (India) | |
|`bg:kbd:standard` | Bulgarian | |
|`bg:kbd:bds` | Bulgarian (BDS) | |
|`ca:kbd:standard` | Catalan | |
|`hr:kbd:standard` | Croatian | |
|`cs:kbd:standard` | Czech | |
|`da:kbd:standard` | Danish | |
|`nl:kbd:standard` | Dutch | |
|`nl-BE:kbd:standard` | Dutch (Belgium) | |
|`en-GB:kbd:standard` | English (Great Britain) | |
|`en-IN:kbd:standard` | English (India) | |
|`en-US:kbd:standard` | English (United States) | |
|`eo:kbd:standard` | Esperanto | |
|`et-EE:kbd:standard` | Estonian (Estonia) | |
|`fi:kbd:standard` | Finnish | |
|`fr:kbd:standard` | French | |
|`fr-CA:kbd:standard` | French (Canada) | |
|`fr-CH:kbd:standard` | French (Switzerland)  | |
|`gl-ES:kbd:standard` | Galician (Spain) | |
|`ka-GE:kbd:standard` | Georgian (Georgia) | |
|`de:kbd:standard` | German | |
|`de-CH:kbd:standard` | German (Switzerland) | |
|`el:kbd:standard` | Greek | |
|`hi:kbd:standard` | Hindi | |
|`hi:kbd:compact` | Hindi (Compact) | |
|`hu:kbd:standard` | Hungarian | |
|`is:kbd:standard` | Icelandic | |
|`it:kbd:standard` | Italian | |
|`it-CH:kbd:standard` | Italian (Switzerland) | |
|`ja:ime:kana` | Japanese (Kana) | |
|`ko:ime:hangul` | Korean (Hangul) | |
|`kn-IN:kbd:standard` | Kannada (India) | |
|`kk:kbd:standard` | Kazakh | |
|`km-KH:kbd:standard` | Khmer (Cambodia) | |
|`ky:kbd:standard` | Kyrgyz | |
|`lo-LA:kbd:standard` | Lao (Laos) | |
|`lv:kbd:standard` | Latvian | |
|`lt:kbd:standard` | Lithuanian | |
|`mk:kbd:standard` | Macedonian | |
|`ml-IN:kbd:standard` | Malayalam (India) | |
|`mr-IN:kbd:standard` | Marathi (India) | |
|`mn-MN:kbd:standard` | Mongolian (Mongolia) | |
|`ne-NP:kbd:romanized` | Nepali (Romanized) | |
|`ne-NP:kbd:traditional` | Nepali (Traditional) | |
|`nb:kbd:standard` | Norwegian Bokmål | |
|`fa:kbd:standard` | Persian | |
|`pl:kbd:standard` | Polish | |
|`pt-BR:kbd:standard` | Portuguese (Brazil) | |
|`pt-PT:kbd:standard` | Portuguese (Portugal) | |
|`ro:kbd:standard` | Romanian | |
|`ru:kbd:standard` | Russian | |
|`sr-Cyrl:kbd:standard` | Serbian (Cyrillic) | |
|`sr-Latn:kbd:standard` | Serbian (Latin) | |
|`sk:kbd:standard` | Slovak | |
|`sl:kbd:standard` | Slovenian | |
|`es:kbd:standard` | Spanish | |
|`es-419:kbd:standard` | Spanish (Latin America) | |
|`es-US:kbd:standard` | Spanish (United States) | |
|`sw:kbd:standard` | Swahili | |
|`sv:kbd:standard` | Swedish | |
|`tl:kbd:standard` | Tagalog | |
|`ta-IN:kbd:standard` | Tamil (India) | |
|`ta-SG:kbd:standard` | Tamil (Singapore) | |
|`te-IN:kbd:standard` | Telugu (India) | |
|`th:kbd:standard` | Thai | |
|`tr:kbd:standard` | Turkish | |
|`uk:kbd:standard` | Ukrainian | |
|`uz-UZ:kbd:standard` | Uzbek (Uzbekistan) | |
|`vi:kbd:standard` | Vietnamese | |
|`zu:kbd:standard` | Zulu | |
|`zh:ime:rime` | Chinese (RIME) | 需要 `Avalonia.Controls.VirtualKeyboard.Ime.Rime` 插件包。 |

## RIME 输入法引擎 {#rime-input-method-engine}

[RIME](https://rime.im/) 输入法引擎提供中文输入（拼音等）。它以独立插件包的形式分发，内含原生二进制文件和方案数据。

### Installing RIME

```bash
dotnet add package Avalonia.Controls.VirtualKeyboard.Ime.Rime
```

该包囊括了所有受支持平台的 RIME 原生二进制文件，以及朙月拼音（Luna Pinyin）方案数据。

### Enabling RIME

在你的 `AppBuilder` 上调用 `WithVirtualKeyboardRimePlugin()`，并确保 `VirtualKeyboardOptions` 中已设置 `DataPath`：

```csharp
using Avalonia.Controls;

public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .WithVirtualKeyboardOptions(new VirtualKeyboardOptions
        {
            DataPath = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                "MyApp", "keyboard-data")
        })
        .WithVirtualKeyboardRimePlugin()
        .LogToTrace();
```

:::warning
使用 RIME 时**必须**设置 `VirtualKeyboardOptions.DataPath`。该路径指向一个可写目录，RIME 会把用户词典和编译后的方案数据存放在那里。若未设置 `DataPath`，应用启动时会抛出 `InvalidOperationException`。
:::

### 在 XAML 中使用 RIME {#using-rime-in-xaml}

```xml
<VirtualKeyboardScope InputMethods="en-US:kbd:standard, zh:ime:rime">
    <StackPanel>
        <TextBox PlaceholderText="Type in English or Chinese"/>
    </StackPanel>
</VirtualKeyboardScope>
```

## 另请参阅 {#see-also}

- [VirtualKeyboardScope](/controls/input/text-input/virtualkeyboard/virtualkeyboardscope)：容器控件，可自动管理键盘的显示隐藏，