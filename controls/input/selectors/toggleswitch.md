---
id: toggleswitch
title: ToggleSwitch
description: 一个滑动式开关控件，用于二选一的设置项，开与关的内容都可以自定义。
doc-type: reference
---

[`ToggleSwitch`](/api/avalonia/controls/toggleswitch) 控件呈现一个可在开、关之间滑动的开关。它的行为和 [`CheckBox`](/api/avalonia/controls/checkbox) 相仿，但采用「轨道 + 滑钮」的视觉形式，在移动端和以触摸为主的界面上更自然。

当某项设置是即时生效的开关时（比如启用深色模式、开关通知），就用 `ToggleSwitch`。如果是让用户从列表中多选的表单字段，`CheckBox` 通常更合适。

## 常用属性 {#common-properties}

下面这些属性你多半会经常用到：

| 属性      | 类型      | 说明                                                        |
| ------------- | --------- | ------------------------------------------------------------------ |
| `IsChecked`   | `bool?`   | 获取或设置当前的开关状态：`true` 为开，`false` 为关。 |
| `OnContent`   | `object`  | 开启时显示的内容，默认为「On」。         |
| `OffContent`  | `object`  | 关闭时显示的内容，默认为「Off」。       |
| `KnobTransitions` | `Transitions` | 状态切换时作用于滑钮的过渡动画。    |

## 事件 {#events}

| 事件              | 说明                              |
| ------------------ | ---------------------------------------- |
| `IsCheckedChanged` | `IsChecked` 的值发生变化时引发。 |

## 基本示例 {#basic-example}

在 AXAML 中放一个 `ToggleSwitch`，并把 `IsChecked` 绑定到视图模型中的布尔属性：

```xml
<ToggleSwitch IsChecked="{Binding IsEnabled}" />
```

## 自定义开/关文字 {#custom-onoff-labels}

默认的「On」和「Off」可以换成你自己的文字：

```xml
<ToggleSwitch IsChecked="{Binding IsDarkMode}"
              OnContent="Dark"
              OffContent="Light" />
```

## 隐藏文字 {#hiding-the-labels}

把两个内容属性都设为空字符串，就只剩下那个滑动开关：

```xml
<ToggleSwitch IsChecked="{Binding IsActive}"
              OnContent=""
              OffContent="" />
```

如果周围的布局本就给这项设置配了标签，这样做正合适。

## 丰富的内容 {#rich-content}

开和关的内容可以是任意控件。下面的例子把 `PathIcon` 和 `TextBlock` 搭在一起：

```xml
<ToggleSwitch IsChecked="{Binding NotificationsEnabled}">
    <ToggleSwitch.OnContent>
        <StackPanel Orientation="Horizontal" Spacing="6">
            <PathIcon Data="{StaticResource bell_regular}" Width="14" />
            <TextBlock Text="Enabled" />
        </StackPanel>
    </ToggleSwitch.OnContent>
    <ToggleSwitch.OffContent>
        <StackPanel Orientation="Horizontal" Spacing="6">
            <PathIcon Data="{StaticResource bell_off_regular}" Width="14" />
            <TextBlock Text="Disabled" />
        </StackPanel>
    </ToggleSwitch.OffContent>
</ToggleSwitch>
```

## 绑定到视图模型 {#binding-to-a-view-model}

在视图模型中定义布尔属性，再把每个 `ToggleSwitch` 分别绑定到其中之一：

```csharp
public partial class SettingsViewModel : ObservableObject
{
    [ObservableProperty]
    private bool _isDarkMode;

    [ObservableProperty]
    private bool _notificationsEnabled = true;

    partial void OnIsDarkModeChanged(bool value)
    {
        // Apply theme change
    }
}
```

```xml
<StackPanel Spacing="12">
    <ToggleSwitch IsChecked="{Binding IsDarkMode}"
                  OnContent="Dark Mode" OffContent="Light Mode" />
    <ToggleSwitch IsChecked="{Binding NotificationsEnabled}"
                  OnContent="Notifications On" OffContent="Notifications Off" />
</StackPanel>
```

由于 `ToggleSwitch` 默认采用双向绑定，一拨动开关，视图模型中的属性立刻就更新了。

## 设置页范式 {#settings-form-pattern}

一种常见布局是：左边放说明文字，右边放一个不带文字的 `ToggleSwitch`：

```xml
<StackPanel Spacing="16">
    <Grid ColumnDefinitions="*,Auto">
        <StackPanel>
            <TextBlock Text="Auto-save" FontWeight="SemiBold" />
            <TextBlock Text="Save changes automatically"
                       Foreground="Gray" FontSize="12" />
        </StackPanel>
        <ToggleSwitch Grid.Column="1" IsChecked="{Binding AutoSave}"
                      OnContent="" OffContent="" />
    </Grid>

    <Grid ColumnDefinitions="*,Auto">
        <StackPanel>
            <TextBlock Text="Spell check" FontWeight="SemiBold" />
            <TextBlock Text="Check spelling as you type"
                       Foreground="Gray" FontSize="12" />
        </StackPanel>
        <ToggleSwitch Grid.Column="1" IsChecked="{Binding SpellCheck}"
                      OnContent="" OffContent="" />
    </Grid>
</StackPanel>
```

把 `OnContent` 和 `OffContent` 设为空字符串即可去掉多余的文字，因为各项设置已经由 `TextBlock` 元素说明过了。

## `ToggleSwitch` 与 `CheckBox` 的取舍 {#choosing-between-toggleswitch-and-checkbox}

| 考量点 | `ToggleSwitch` | `CheckBox` |
| ------------- | -------------- | ---------- |
| 视觉形式  | 滑动开关 | 勾选标记 |
| 最适合 | 设置项、即时生效的开关状态 | 表单字段、多选列表 |
| 是否支持三态 | No | 支持（通过 `IsThreeState`） |
| 平台观感 | 适合移动端与触摸操作 | 传统桌面风格 |

改动立即生效的，选 `ToggleSwitch`；需要用户确认或提交表单后才生效的，选 `CheckBox`。

## 另请参阅 {#see-also}

- [CheckBox](/controls/input/selectors/checkbox)
- [ToggleButton](/controls/input/buttons/togglebutton)
- [RadioButton](/controls/input/buttons/radiobutton)
