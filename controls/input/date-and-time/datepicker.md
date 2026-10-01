---
id: datepicker
title: DatePicker
description: 一个基于微调列的控件，让用户分别挑选年、月、日来选定日期。
doc-type: reference
---

import DatePickerScreenshot from '/img/controls/datepicker/datepicker.gif';

`DatePicker` 控件给出三列微调器，供用户挑选日期值。点击控件时，这些微调列就会展开。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性 | 说明 |
|---|---|
| `SelectedDate` | 所选日期，类型为 `DateTimeOffset?`（未选中时为 null）。 |
| `DayVisible` | 设置「日」这一列是否可见。 |
| `MonthVisible` | 设置「月」这一列是否可见。 |
| `YearVisible` | 设置「年」这一列是否可见。 |
| `DayFormat` | 日期中「日」部分的格式字符串。 |
| `MonthFormat` | 日期中「月」部分的格式字符串。 |
| `YearFormat` | 日期中「年」部分的格式字符串。 |
| `MinYear` | 可选的最早年份。 |
| `MaxYear` | 可选的最晚年份。 |

## Example

下面的例子用 `DayFormat` 特性，让日期同时显示星期名和数字：

```xml
<StackPanel Margin="20">
  <DatePicker DayFormat="ddd dd"/>
</StackPanel>
```

<Image light={DatePickerScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 隐藏日期中的某些部分 {#hiding-date-parts}

把可见性属性设为 `False`，就能只显示你需要的那几个日期部分：

```xml
<!-- Month and year only -->
<DatePicker DayVisible="False" />

<!-- Year only -->
<DatePicker DayVisible="False" MonthVisible="False" />
```

## 限定日期范围 {#constraining-the-date-range}

用 `MinYear` 和 `MaxYear` 可以限定用户能选的年份范围。当选择必须落在某个已知有效区间内时（比如出生日期或有效期），这很有用。

```xml
<DatePicker MinYear="2000/01/01" MaxYear="2030/12/31" />
```

这些值也可以在代码隐藏中设置：

```csharp
datePicker.MinYear = new DateTimeOffset(new DateTime(2000, 1, 1));
datePicker.MaxYear = new DateTimeOffset(new DateTime(2030, 12, 31));
```

## 定制显示格式 {#customizing-the-display-format}

选择器的每一列都支持标准的 .NET 日期格式字符串。把它们组合起来，就能精确控制用户看到的样子：

```xml
<!-- Full month name, abbreviated day name, four-digit year -->
<DatePicker MonthFormat="MMMM" DayFormat="ddd dd" YearFormat="yyyy" />

<!-- Numeric month, day number only, two-digit year -->
<DatePicker MonthFormat="MM" DayFormat="dd" YearFormat="yy" />
```

## 初始化日期 {#initializing-the-date}

该控件的日期属性无法在 AXAML 中用字符串特性设置，因为并没有从字符串到 `DateTimeOffset` 的内置转换。

可以在代码隐藏中设置该值：

```csharp
datePicker.SelectedDate = new DateTimeOffset(new DateTime(1950, 1, 1));
```

## 绑定到视图模型 {#binding-to-a-view-model}

多数应用中，你会把 `SelectedDate` 绑定到视图模型的某个属性上。该属性应当是可空的 `DateTimeOffset`，这样才能表示「未选择」的状态。

```csharp
public class MyViewModel : ObservableObject
{
    [ObservableProperty]
    private DateTimeOffset? _selectedDate;
}
```

```xml
<DatePicker SelectedDate="{Binding SelectedDate}" />
```

若需要在用户改变日期时作出响应，可以订阅 `SelectedDateChanged` 事件，或在视图模型中使用属性变更回调：

```csharp
public partial class MyViewModel : ObservableObject
{
    [ObservableProperty]
    private DateTimeOffset? _selectedDate;

    partial void OnSelectedDateChanged(DateTimeOffset? value)
    {
        // Respond to the new date value here.
    }
}
```

## 另请参阅 {#see-also}

- [Calendar](/controls/input/date-and-time/calendar)
- [CalendarDatePicker](/controls/input/date-and-time/calendardatepicker)
- [TimePicker](/controls/input/date-and-time/timepicker)
- [DatePicker API 参考](/api/avalonia/controls/datepicker)
- [GitHub 上的 `DatePicker.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/DateTimePickers/DatePicker.cs)
