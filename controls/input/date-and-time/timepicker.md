---
id: timepicker
title: TimePicker
description: 一个控件：用时、分（以及可选的秒）微调器让用户选定时间。
doc-type: reference
---

`TimePicker` 给出两到四个微调器，供用户选定时间值。它支持 24 小时制和 12 小时制，还可以选配秒的选择。点击控件时，这些微调器就会展开。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
|---|---|---|
| `SelectedTime` | `TimeSpan?` | 所选的时间值。未选择时间时为 `null`。 |
| `ClockIdentifier` | `string` | 设置时钟格式，可取 `12HourClock` 或 `24HourClock`。12 小时制会多出一个 AM/PM 微调器。 |
| `UseSeconds` | `bool` | 为 `true` 时额外显示一个「秒」微调器，默认值为 `false`。 |
| `MinuteIncrement` | `int` | 定义分钟的可选步长，默认值为 `1`。 |
| `SecondIncrement` | `int` | 定义秒的可选步长，默认值为 `1`。 |

## 时钟格式 {#clock-format}

`TimePicker` 默认采用带 AM/PM 微调器的 12 小时制。把 `ClockIdentifier` 设为 `24HourClock` 即可切换到 24 小时制：

```xml
<!-- 12-hour clock (default) with AM/PM spinner -->
<TimePicker ClockIdentifier="12HourClock" />

<!-- 24-hour clock without AM/PM spinner -->
<TimePicker ClockIdentifier="24HourClock" />
```

## Example

下面的例子演示如何做一个 24 小时制、以 20 分钟为一档的时间选择器：

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Margin="20"
            Spacing="4">
  <Label Content="Please choose your time:"/>
  <TimePicker ClockIdentifier="24HourClock"
              MinuteIncrement="20"/>
</StackPanel>
```
</XamlPreview>

## 初始化时间 {#initializing-the-time}

时间值可以作为特性直接写在 XAML 里。请使用 `Hh:Mm` 形式的字符串，其中 `Hh` 是小时（0 到 23），`Mm` 是分钟（0 到 59）：

```xml
<TimePicker SelectedTime="09:15"/>
```

若要写代码隐藏，可以这样初始化时间：

```csharp
TimePicker timePicker = new TimePicker
{
    SelectedTime = new TimeSpan(9, 15, 0) // Seconds are ignored.
};
```

把 `SelectedTime` 重置为 `null` 即可清空显示。

## 限定可选时间 {#constraining-the-time}

调整 `MinuteIncrement` 和 `SecondIncrement` 即可限定可选的时间。比如只允许按 15 分钟一档来选：

```xml
<TimePicker MinuteIncrement="15" />
```

若要显示秒并以 30 秒为一档：

```xml
<TimePicker UseSeconds="True" SecondIncrement="30" />
```

## 视图模型绑定 {#view-model-binding}

把 `SelectedTime` 绑定到视图模型中的 `TimeSpan?` 属性：

```xml
<TimePicker SelectedTime="{Binding AppointmentTime}"
            ClockIdentifier="12HourClock" />
```

```csharp
[ObservableProperty]
private TimeSpan? _appointmentTime = new TimeSpan(14, 30, 0);
```

订阅 `SelectedTimeChanged` 事件，或在视图模型中观察属性变化，即可对变更作出响应。

## 另请参阅 {#see-also}

- [DatePicker](/controls/input/date-and-time/datepicker)
- [CalendarDatePicker](/controls/input/date-and-time/calendardatepicker)
- [TimePicker API 参考](/api/avalonia/controls/timepicker)
- [GitHub 上的 `TimePicker.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/DateTimePickers/TimePicker.cs)
