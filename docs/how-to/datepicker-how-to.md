---
id: datepicker-how-to
title: "操作指南：使用日期和时间选择器"
description: 用 Avalonia 的各种选择器绑定日期、格式化显示、校验输入并限定日期范围。
doc-type: how-to
---

本指南介绍 DatePicker、TimePicker、CalendarDatePicker 与 Calendar 的用法：绑定日期、格式化、校验以及日期范围。

## DatePicker Basics

`DatePicker` 用微调控件来选择日、月、年：

```xml
<DatePicker />
```

### 设置初始日期 {#setting-an-initial-date}

日期属性必须在代码中设置（不能写成 XAML 特性），因为没有内置的字符串到 DateTimeOffset 的转换器：

```csharp
myDatePicker.SelectedDate = new DateTimeOffset(new DateTime(2025, 6, 15));
```

或者绑定到视图模型的属性：

```csharp
[ObservableProperty]
private DateTimeOffset? _birthDate;
```

```xml
<DatePicker SelectedDate="{Binding BirthDate}" />
```

## Custom Date Formats

控制日期各部分的显示方式：

```xml
<!-- Show abbreviated day name -->
<DatePicker DayFormat="ddd dd" />

<!-- Show full month name -->
<DatePicker MonthFormat="MMMM" />

<!-- Four-digit year -->
<DatePicker YearFormat="yyyy" />
```

常用格式字符串：

| 格式 | 输出示例 |
|---|---|
| `d` | 5 |
| `dd` | 05 |
| `ddd` | Mon |
| `dddd` | Monday |
| `M` | 6 |
| `MM` | 06 |
| `MMM` | Jun |
| `MMMM` | June |
| `yy` | 25 |
| `yyyy` | 2025 |

## Hiding Date Parts

只显示你需要的字段：

```xml
<!-- Month and year only (no day) -->
<DatePicker DayVisible="False" />

<!-- Year only -->
<DatePicker DayVisible="False" MonthVisible="False" />
```

## TimePicker

`TimePicker` 提供小时和分钟的微调框：

```xml
<TimePicker />
```

### 12 小时制与 24 小时制 {#12-hour-vs-24-hour-clock}

```xml
<!-- 12-hour with AM/PM -->
<TimePicker ClockIdentifier="12HourClock" />

<!-- 24-hour -->
<TimePicker ClockIdentifier="24HourClock" />
```

### 分钟步进 {#minute-increments}

```xml
<!-- 15-minute intervals -->
<TimePicker MinuteIncrement="15" />
```

### 绑定选中的时间 {#binding-the-selected-time}

```csharp
[ObservableProperty]
private TimeSpan? _alarmTime;
```

```xml
<TimePicker SelectedTime="{Binding AlarmTime}" />
```

## CalendarDatePicker

`CalendarDatePicker` 显示一个文本框，点开后弹出完整的日历下拉面板：

```xml
<CalendarDatePicker PlaceholderText="Select a date"
                    SelectedDate="{Binding EventDate}" />
```

### 显示格式 {#display-format}

```xml
<CalendarDatePicker DisplayFormat="yyyy-MM-dd"
                    SelectedDate="{Binding EventDate}" />
```

### 禁选日期 {#blackout-dates}

禁止选择特定日期：

```csharp
calendarDatePicker.BlackoutDates.Add(
    new CalendarDateRange(DateTime.Today, DateTime.Today.AddDays(3)));
```

## Calendar Control

`Calendar` 直接显示整月视图，方便就地选日期：

```xml
<Calendar SelectedDate="{Binding SelectedDate}"
          SelectionMode="SingleDate" />
```

### 选择模式 {#selection-modes}

```xml
<!-- Single date -->
<Calendar SelectionMode="SingleDate" />

<!-- Range of dates -->
<Calendar SelectionMode="SingleRange" />

<!-- Multiple individual dates -->
<Calendar SelectionMode="MultipleRange" />

<!-- No selection (display only) -->
<Calendar SelectionMode="None" />
```

### 显示模式 {#display-modes}

```xml
<!-- Show month view (default) -->
<Calendar DisplayMode="Month" />

<!-- Start from year picker -->
<Calendar DisplayMode="Year" />

<!-- Start from decade picker -->
<Calendar DisplayMode="Decade" />
```

### 日期范围限制 {#date-range-limits}

限定可浏览的日期范围：

```xml
<Calendar DisplayDateStart="2025-01-01"
          DisplayDateEnd="2025-12-31" />
```

### 在代码中设置禁选日期 {#blackout-dates-in-code}

```csharp
// Block weekends
for (var date = startDate; date <= endDate; date = date.AddDays(1))
{
    if (date.DayOfWeek is DayOfWeek.Saturday or DayOfWeek.Sunday)
        calendar.BlackoutDates.Add(new CalendarDateRange(date));
}
```

## Date Validation

校验选中的日期是否落在允许的范围内：

```csharp
public partial class BookingViewModel : ObservableValidator
{
    [ObservableProperty]
    [NotifyDataErrorInfo]
    [CustomValidation(typeof(BookingViewModel), nameof(ValidateFutureDate))]
    private DateTimeOffset? _departureDate;

    public static ValidationResult? ValidateFutureDate(DateTimeOffset? date, ValidationContext context)
    {
        if (date.HasValue && date.Value.Date <= DateTimeOffset.Now.Date)
            return new ValidationResult("Departure date must be in the future.");
        return ValidationResult.Success;
    }
}
```

## 显示时的日期格式化 {#date-formatting-in-display}

在 TextBlock 中显示格式化后的选中日期：

```xml
<StackPanel Spacing="8">
    <DatePicker SelectedDate="{Binding SelectedDate}" />
    <TextBlock Text="{Binding SelectedDate, StringFormat='Selected: {0:d}'}" />
</StackPanel>
```

## 把日期和时间组合起来 {#combining-date-and-time}

两个选择器搭配使用，凑成完整的日期时间：

```xml
<StackPanel Orientation="Horizontal" Spacing="12">
    <DatePicker SelectedDate="{Binding EventDate}" />
    <TimePicker SelectedTime="{Binding EventTime}" ClockIdentifier="24HourClock" />
</StackPanel>
```

在视图模型中把它们合到一起：

```csharp
public DateTime? CombinedDateTime
{
    get
    {
        if (EventDate is null) return null;
        var date = EventDate.Value.Date;
        return EventTime.HasValue
            ? date.Add(EventTime.Value)
            : date;
    }
}
```

## Key Properties Reference

### DatePicker

| 属性 | 类型 | 说明 |
|---|---|---|
| `SelectedDate` | `DateTimeOffset?` | 选中的日期。 |
| `DayVisible` | `bool` | 显示或隐藏「日」微调框。 |
| `MonthVisible` | `bool` | 显示或隐藏「月」微调框。 |
| `YearVisible` | `bool` | 显示或隐藏「年」微调框。 |
| `DayFormat` | `string` | 「日」的显示格式。 |
| `MonthFormat` | `string` | 「月」的显示格式。 |
| `YearFormat` | `string` | 「年」的显示格式。 |

### TimePicker

| 属性 | 类型 | 说明 |
|---|---|---|
| `SelectedTime` | `TimeSpan?` | 选中的时间。 |
| `ClockIdentifier` | `string` | `"12HourClock"` or `"24HourClock"`. |
| `MinuteIncrement` | `int` | 「分钟」微调框的步长。 |

## See Also

- [DatePicker 控件参考](/controls/input/date-and-time/datepicker)：属性表。
- [TimePicker 控件参考](/controls/input/date-and-time/timepicker)：时间选择控件。
- [Calendar 控件参考](/controls/input/date-and-time/calendar)：完整的日历显示。
- [数据校验](/docs/data-binding/binding-validation)：校验绑定的值。
