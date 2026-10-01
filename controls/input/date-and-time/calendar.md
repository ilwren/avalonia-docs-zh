---
id: calendar
title: Calendar
---

import CalendarBasicUsageScreenshot from '/img/controls/calendar/calendar3.gif';
import CalendarSingleSelectionScreenshot from '/img/controls/calendar/calendar.gif';
import CalendarMultipleSelectionScreenshot from '/img/controls/calendar/calendar2.gif';
import CalendarCustomRangeScreenshot from '/img/controls/calendar/calendar4.gif';

calendar 是一个供用户选择日期或日期区间的控件。

<Image light={CalendarBasicUsageScreenshot} alt="An animation of a calendar switching between year, month and day views." position="center" maxWidth={400} cornerRadius="true"/>

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table><thead><tr><th width="251">Property</th><th>说明</th></tr></thead><tbody><tr><td><code>SelectionMode</code></td><td>指明允许哪种选择方式，可选：单个日期、单个区间、多个区间，以及不可选。</td></tr><tr><td><code>DisplayMode</code></td><td>定义日历从哪一层级开始逐级展开，可选：十年、年和月（默认）。 </td></tr><tr><td><code>SelectedDate</code></td><td>当前选中的日期。</td></tr><tr><td><code>SelectedDates</code></td><td>已选日期的集合，包含单个区间和多个区间中的各个日期。</td></tr><tr><td><code>DisplayDate</code></td><td>控件首次显示时所展示的日期。</td></tr><tr><td><code>DisplayDateStart</code></td><td>可显示的最早日期。</td></tr><tr><td><code>DisplayDateEnd</code></td><td>可显示的最晚日期。</td></tr><tr><td><code>BlackoutDates</code></td><td>一组日期，它们会显示为不可用，无法被选中。</td></tr><tr><td><code>AllowTapRangeSelection</code></td><td>When <code>true</code> （默认值），先点一下起始日期、再点一下结束日期，即可选择一个日期区间。它适用于 <code>SingleRange</code> and <code>MultipleRange</code> 这几种选择模式。</td></tr></tbody></table>

## 示例 {#examples}

这是一个只能选单个日期的基础日历，所选日期显示在下方的文本块中。

```xml
<StackPanel Margin="20">
  <Calendar SelectionMode="SingleDate"/>
  <TextBlock Margin="20" 
             Text="{Binding #calendar.SelectedDate}"/>
</StackPanel>
```

<Image light={CalendarSingleSelectionScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

这个例子允许选择多个区间：

```xml
  <StackPanel Margin="20">
    <Calendar SelectionMode="MultipleRange"/>
  </StackPanel>
```

<Image light={CalendarMultipleSelectionScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

要选择一个区间，先点击起始日期，再点击结束日期。这种「点选」行为由 `AllowTapRangeSelection` 属性控制，默认是开启的。另一种办法是按住 Shift 键再点击结束日期来延展区间。按住 Ctrl 键点击其他日期，还能追加更多日期和区间。

这个例子自定义了起止日期，并把部分日期设为不可用。它用的是窗口的 C# 代码隐藏。

```xml
<UserControl xmlns="https://github.org/avaloniaui">
<StackPanel Margin="20">
  <Calendar x:Name="calendar" SelectionMode="SingleDate"/>
</StackPanel>
</UserControl>
```


```csharp title='C#'
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        var today = DateTime.Today;
        calendar.DisplayDateStart = today.AddDays(-25);
        calendar.DisplayDateEnd = today.AddDays(25);
        calendar.BlackoutDates.Add(
            new CalendarDateRange( today.AddDays(5), today.AddDays(10)));
    } 
}
```


<Image light={CalendarCustomRangeScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 另请参阅 {#see-also}

- [Calendar API 参考](/api/avalonia/controls/calendar)
- [GitHub 上的 `Calendar.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Calendar/Calendar.cs)
