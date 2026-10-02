---
id: focus
title: 焦点
description: 学会在 Avalonia 中管理键盘焦点，内容包括 Tab 导航、方向（XYFocus）导航、焦点事件、伪类以及 FocusManager。
doc-type: explanation
---

import DirectionalNavigationScreenshot from '/img/concepts/ui-concepts/user-input/directional-navigation.gif';

焦点指的是预期要接收键盘输入的那个 [`InputElement`](/api/avalonia/input/inputelement)。获得焦点的控件通常会带上一个视觉标记。最为人熟知的例子是内有光标闪烁的 `TextBox`，不过 `Button` 和 [`Slider`](/api/avalonia/controls/slider) 这类非文本控件同样参与焦点机制。

弄懂焦点的运作方式，有助于你做出无障碍、键盘友好的应用。本页介绍焦点的核心属性、事件、伪类，以及两套内置的导航方案（Tab 导航与方向导航）。

## `IsFocused` and `Focusable`

`IsFocused` 是个只读属性，用来表明某个 `InputElement` 当前是否持有焦点。

`Focusable` 属性决定某个 `InputElement` 能否获得焦点。无法获得焦点的元素仍可用指针操作，因此你应当尽量为它们提供可用的键盘等价方式（比如快捷键）。

```xml
<!-- Prevent a button from receiving keyboard focus -->
<Button Content="Click only" Focusable="False" />
```

## 显式设置焦点 {#explicit-focusing}

要显式把焦点交给某个 `InputElement`，请在代码中调用它的 `Focus()` 方法。你还可以选择性地指定 [`NavigationMethod`](/api/avalonia/input/navigationmethod) 和 `KeyModifiers`，以模拟由特定导航流程引发的聚焦。显式聚焦常用于：表单加载时把焦点落在某个 `InputElement` 上，或者在当前输入填妥之后用代码把焦点移到下一个控件。

```csharp
// Focus a control when the view loads
myTextBox.Focus(NavigationMethod.Unspecified, KeyModifiers.None);
```

| `NavigationMethod` | 触发方式说明        |
|:--------------------|:---------------------------|
| `Tab`               | 按下 Tab 键              |
| `Pointer`           | 指针交互        |
| `Directional`       | 二维方向导航（[`XYFocus`](/api/avalonia/input/xyfocus)） |
| `Unspecified`       | Default                    |

## 焦点事件 {#focus-events}

`InputElement` 公开了 `GotFocus` 和 `LostFocus` 事件。`GotFocusEventArgs` 中含有引发本次焦点变化的 `NavigationMethod` 和 `KeyModifiers`，你可以据此调整界面的行为。

```csharp
myTextBox.GotFocus += (sender, e) =>
{
    if (e.NavigationMethod == NavigationMethod.Tab)
    {
        // Select all text when the user tabs into the field
        myTextBox.SelectAll();
    }
};
```

## 焦点伪类 {#focus-pseudoclasses}

当你给 `Focusable` 的控件写样式时，这些伪类很有用。

| 伪类      | 说明                                                   |
|:-----------------|:--------------------------------------------------------------|
| `:focus`         | 控件持有焦点。                                        |
| `:focus-within`  | 控件持有焦点，或者它的某个后代持有焦点。 |
| `:focus-visible` | 控件持有焦点，并且应当显示视觉标记。      |

:::tip
`FocusAdorner` 属性会在 `:focus-visible` 的控件周围显示默认的焦点视觉效果，通常是一个 `Border`。若你用 `:focus-visible` 自己画了标记，请把 `FocusAdorner` 设为 `null`，免得出现两重标记。
:::

## `FocusManager`

`FocusManager` 提供对焦点功能的全局访问，比如取出当前获得焦点的元素或清除焦点。更多内容请参阅 [FocusManager 文档](/docs/services/focus-manager)。

```csharp
// Get the focus manager from a TopLevel
var focusManager = TopLevel.GetTopLevel(myControl)?.FocusManager;

// Get the currently focused element
var focused = focusManager?.GetFocusedElement();
```

## Tab 焦点导航 {#tab-focus-navigation}

按下 Tab 键时发生的就是 Tab 焦点导航。凡是 `IsTabStop` 属性为 `true` 的 `InputElement` 都会参与 Tab 导航。`TabIndex` 属性指定优先级，数值越小越先被访问到。当多个控件的 `TabIndex` 相同时，顺序取决于视觉树的遍历次序。

`KeyboardNavigation.TabNavigation` 附加属性会给任何充当容器的 `InputElement` 设上一个 `KeyboardNavigationMode`，从而改变 Tab 导航在其子元素间穿行的方式。

```xml
<!-- Cycle tab focus within the StackPanel -->
<StackPanel KeyboardNavigation.TabNavigation="Cycle">
    <TextBox TabIndex="0" Watermark="First field" />
    <TextBox TabIndex="1" Watermark="Second field" />
    <TextBox TabIndex="2" Watermark="Third field" />
</StackPanel>
```

| `KeyboardNavigationMode` | 容器内的遍历方式                                  |
|:--------------------------|:----------------------------------------------------------|
| `Continue`                | 走完这些项目后继续前进，进入下一个容器          |
| `Cycle`                   | 在本容器的项目之间循环，到头后绕回开头        |
| `Contained`               | 停在第一项或最后一项处                        |
| `Once`                    | 容器及其子元素作为一个整体，只获得一次焦点 |
| `None`                    | Tab 导航不会聚焦到这些项目上               |
| `Local`                   | `TabIndex` 只在本地子树的项目范围内起作用 |

## 方向焦点导航 {#directional-focus-navigation}

通过 `XYFocus` 进行的焦点导航是一套二维方向方案：从当前获得焦点的控件出发，沿左、右、上、下四个方位作空间导航。默认情况下，`XYFocus.NavigationModes` 设置为允许 `Gamepad` 和 `Remote` 导航。

| `KeyDeviceType` | 设备                                    |
|:----------------|:------------------------------------------|
| `Disabled`      | 禁用任何按键设备的 XY 导航。 |
| `Keyboard`      | 可使用键盘方向键。          |
| `Gamepad`       | 可使用游戏手柄的方向键。      |
| `Remote`        | 可使用遥控器。               |
| `Enabled`       | 所有设备都可使用。                  |

在能原生发出这类输入的设备上（比如 Android），手柄输入是受支持的。不过 Avalonia 目前还缺少跨平台的手柄 API，因而无法做到开箱即用的广泛支持。

### 导航策略 {#navigation-strategy}

启用二维方向导航后，系统会用一套消歧策略来挑出导航目标。

| `XYFocusNavigationStrategy`    | 导航目标                                                             |
|:-------------------------------|:------------------------------------------------------------------------------|
| `Auto`                         | 沿用祖先的策略；若所有祖先都没指定，则采用 `Projection`。  |
| `Projection`                   | 沿导航方向投出一条射线，碰到的第一个元素。 |
| `NavigationDirectionDistance`  | 距这条导航射线所在轴线最近的元素。                           |
| `RectilinearDistance`          | 按曼哈顿距离最短原则选出的最近元素。                     |

### 显式导航 {#explicit-navigation}

`XYFocus` 让每个控件都能通过 `XYFocus.Up`、`XYFocus.Down`、`XYFocus.Left` 和 `XYFocus.Right` 指定某个方向被按下时的显式导航目标，其优先级高于任何导航策略。

:::caution
焦点接管（focus engagement）尚未实现，因此当方向焦点导航遇上那些自己也要处理方向输入的控件时，可能会有些局限，视觉表现上尤其如此。
:::

### Example

下面的例子演示如何在 `WrapPanel` 中使用方向焦点导航，其中显式允许了从第一个元素绕到最后一个、以及反过来的导航。

`Slider` 示范了把导航与控件交互混在一起的做法。在桌面端，当 `Slider` 获得焦点时按下 Enter 键，就进入交互状态，此时按键改为调整 `Slider.Value` 而不再触发导航；再按一次 Enter 则结束交互，恢复方向焦点导航。

```xml title="DirectionalNavigation.axaml"
<Window
    XYFocus.NavigationModes="Enabled"
    XYFocus.UpNavigationStrategy="Projection"
    XYFocus.DownNavigationStrategy="Projection"
    XYFocus.LeftNavigationStrategy="Projection"
    XYFocus.RightNavigationStrategy="Projection">
    <Grid>
        <WrapPanel>
            <Button x:Name="first"
                Content="First"
                XYFocus.Left="{Binding #last}" />
            <Button Content="Second" />
            <Button Content="Third" />

            <Slider Width="100" Maximum="100" />

            <Button Content="Fourth" />
            <Button x:Name="last"
                Content="Last"
                XYFocus.Right="{Binding #first}" />
        </WrapPanel>
    </Grid>
</Window>
```

<Image light={DirectionalNavigationScreenshot} alt="Directional Navigation Example" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [键盘与快捷键](/docs/input-interaction/keyboard-and-hotkeys)：按键绑定与键盘快捷键。
- [FocusManager](/docs/services/focus-manager)：全局焦点管理服务。
- [指针事件](/docs/input-interaction/pointer)：指针设备的各类事件。
- [路由事件](/docs/input-interaction/routed-events)：事件如何在元素树中传递。
