---
id: calendardatepicker
title: CalendarDatePicker
description: 一个带文本框的下拉日历控件，用户既可以从日历中选日期，也可以直接键入。
doc-type: reference
---

import CalendarDatePickerScreenshot from '/img/gitbook-import/assets/calendardatepicker.gif';

`CalendarDatePicker` 把一个文本框和一个下拉按钮组合在一起，点下拉按钮即可展开完整日历，直观地挑选日期。再点一次按钮（或选定某个日期）日历便收起，所选日期随即填进文本框。

你也可以直接在文本框里键入日期。该控件接受多种日期格式，并会把它们统一成未选日期时占位文字所示的那种格式。

:::info
关于该控件中日历部分的细节，请参阅 [Calendar](/controls/input/date-and-time/calendar) 参考。
:::

## 常用属性 {#common-properties}

下面这些属性你多半会经常用到：

| 属性 | 类型 | 说明 |
|---|---|---|
| `SelectedDate` | `DateTime?` | 当前选中的日期；未选中任何日期时为 `null`。 |
| `DisplayDate` | `DateTime` | 日历展开时显示的月份。 |
| `DisplayDateStart` | `DateTime?` | 可选的最早日期。 |
| `DisplayDateEnd` | `DateTime?` | 可选的最晚日期。 |
| `PlaceholderText` | `string` | 未选中日期时显示的占位文字。 |
| `PlaceholderForeground` | `IBrush` | 渲染占位文字所用的画刷。 |
| `IsTodayHighlighted` | `bool` | 是否在视觉上高亮今天的日期，默认值为 `true`。 |
| `SelectedDateFormat` | `CalendarDatePickerFormat` | 显示格式：`Short` 或 `Long`。 |
| `CustomDateFormatString` | `string` | 使用自定义格式时所用的日期格式字符串。 |
| `IsDropDownOpen` | `bool` | 日历下拉当前是否处于展开状态。 |

## 绑定到视图模型 {#binding-to-a-view-model}

```xml title="XAML"
<CalendarDatePicker SelectedDate="{Binding BirthDate}"
                    PlaceholderText="Select date of birth"
                    DisplayDateEnd="{Binding Today}" />
```

```csharp title="C#"
[ObservableProperty]
private DateTimeOffset? _birthDate;

public DateTimeOffset Today { get; } = DateTimeOffset.Now;
```

## 限定日期范围 {#date-range-restriction}

用 `DisplayDateStart` 和 `DisplayDateEnd` 可以限定可选的日期范围：

```xml title="XAML"
<CalendarDatePicker SelectedDate="{Binding CheckInDate}"
                    DisplayDateStart="2024-01-01"
                    DisplayDateEnd="2025-12-31"
                    PlaceholderText="Check-in date" />
```

## 实用提示 {#practical-notes}

- **键入输入**：当用户键入的日期落在 `DisplayDateStart`/`DisplayDateEnd` 范围之外时，控件会拒绝该值并清空文本框。
- **空值处理**：请把 `SelectedDate` 绑定到可空的 `DateTimeOffset?` 属性，这样控件才能表示「未选择」。
- **格式定制**：把 `SelectedDateFormat` 设为 `CalendarDatePickerFormat.Custom` 并给出 `CustomDateFormatString`（例如 `"yyyy-MM-dd"`），即可控制所选日期在文本框中的呈现方式。
- **键盘支持**：用户可以用 `Alt+Down` 展开下拉，用 `Escape` 收起。

## Example

下面的例子展示点击按钮后弹出的基础单日期选择日历：

<XamlPreview>

```xml title="XAML"
<UserControl xmlns="https://github.com/avaloniaui"
             Padding="20">
  <StackPanel Margin="20">
    <CalendarDatePicker />
  </StackPanel>
</UserControl>
```

</XamlPreview>

## 另请参阅 {#see-also}

- [Calendar](/controls/input/date-and-time/calendar)
- [DatePicker](/controls/input/date-and-time/datepicker)
- [TimePicker](/controls/input/date-and-time/timepicker)
- [CalendarDatePicker API 参考](/api/avalonia/controls/calendardatepicker)
- [GitHub 上的 `CalendarDatePicker.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/CalendarDatePicker/CalendarDatePicker.cs)
