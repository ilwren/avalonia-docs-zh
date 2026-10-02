---
id: progressbar
title: ProgressBar
description: 一条横向或纵向的进度条，按比例填充来表示取值，可显示文字说明，也支持进度未知时的不确定模式。
doc-type: reference
---

`ProgressBar` 把取值以按比例填充的进度条呈现出来，并可选地显示一段文字说明。它适合表示文件下载、安装、数据处理等耗时操作的完成状态。

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性             | 说明                                                                                     |
|----------------------|-------------------------------------------------------------------------------------------------|
| `Minimum`            | 取值范围的最小值，默认 `0`。                                                |
| `Maximum`            | 取值范围的最大值，默认 `100`。                                              |
| `Value`              | 当前取值（位于取值范围之内）。                                                             |
| `IsIndeterminate`    | 为 `true` 时，进度条显示一个动画指示器，而不是按比例填充。             |
| `Orientation`        | 设置进度条的方向，可选 `Horizontal`（默认）或 `Vertical`。                               |
| `Foreground`         | 用于绘制进度条已填充部分的画刷。                                          |
| `ShowProgressText`   | 为 `true` 时，进度条上会叠加一段文字，显示当前进度。             |
| `ProgressTextFormat` | 控制进度文字如何呈现的格式字符串，详见下一节。         |

## Example

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Margin="20">
  <ProgressBar  Margin="0 10" Height="20"
                Minimum="0" Maximum="100" Value="14"
                ShowProgressText="True"/>
  <ProgressBar  Margin="0 10" Height="20"
                Minimum="0" Maximum="100" Value="92"
                Foreground="Red"
                ShowProgressText="True"/>
</StackPanel>
```

</XamlPreview>

## 不确定模式 {#indeterminate-mode}

当工作总量未知时，把 `IsIndeterminate` 设为 `True`。此时进度条显示循环动画而非按比例填充，既表明工作正在进行，又不必给出具体的完成百分比。

```xml
<ProgressBar IsIndeterminate="True" Height="20" />
```

连接远程服务器、等待外部进程、加载大小未知的数据等场景都适合用它。

要切回确定模式，把 `IsIndeterminate` 设为 `False`，并随着操作推进更新 `Value`：

```xml
<ProgressBar IsIndeterminate="{Binding IsLoading}"
             Value="{Binding Progress}"
             Minimum="0" Maximum="100"
             Height="20" />
```

## 用 `ProgressTextFormat` 自定义进度文字 {#customizing-progress-text-with-progresstextformat}

默认情况下，`ShowProgressText` 会根据 [`Value`](/api/avalonia/controls/primitives/rangebase#value-property)、[`Minimum`](/api/avalonia/controls/primitives/rangebase#minimum-property) 和 [`Maximum`](/api/avalonia/controls/primitives/rangebase#maximum-property) 算出完成百分比并显示出来。把 `ProgressTextFormat` 设为一个格式字符串即可自定义显示内容。该字符串会传给 [`string.Format`](https://docs.microsoft.com/en-us/dotnet/api/system.string.format#system-string-format(system-string-system-object()))，可用的格式项如下：

| 索引 | 说明                                                                                                    |
|-------|----------------------------------------------------------------------------------------------------------------|
| `0`   | 当前的 `Value`。                                                                                           |
| `1`   | 换算成 0 到 100 的百分比（例如 `Minimum = 0`、`Maximum = 50`、`Value = 25` 得到 `50`）。 |
| `2`   | `Minimum` 的取值。                                                                                           |
| `3`   | `Maximum` 的取值。                                                                                           |

| 最小值 | 最大值 | 值 | `ProgressTextFormat`                | 输出                       |
|-----|-----|-------|-------------------------------------|------------------------------|
| 0   | 20  | 17    | `{}{0}/{3} Tasks Complete ({1:0}%)` | `17/20 Tasks Complete (85%)` |

本例中 `{0}` 恰好位于字符串开头，因此必须在前面加 `{}` 转义。

## 纵向摆放 {#vertical-orientation}

设置 `Orientation` 属性即可让进度条纵向显示：

```xml
<ProgressBar Orientation="Vertical" Height="200" Width="20"
             Minimum="0" Maximum="100" Value="65"
             ShowProgressText="True" />
```

## 绑定到视图模型 {#binding-to-a-view-model}

把 `Value` 绑定到视图模型的属性上，就能跟踪异步操作的进度：

```xml
<ProgressBar Minimum="0" Maximum="100"
             Value="{Binding DownloadProgress}"
             ShowProgressText="True"
             ProgressTextFormat="{}{1:0}%" />
```

```csharp
[ObservableProperty]
private double _downloadProgress;

public async Task DownloadFileAsync()
{
    for (int i = 0; i <= 100; i += 10)
    {
        await Task.Delay(500);
        DownloadProgress = i;
    }
}
```

## Styling

你可以通过主题资源、或者针对模板部件来重新设计 `ProgressBar` 的样式。该控件暴露了以下关键模板部件：

| 部件名称              | 说明                                           |
|------------------------|-------------------------------------------------------|
| `PART_Indicator`       | 表示已填充区域的 `Border` 元素。 |
| `PART_ProgressBarText` | 显示进度文字的 `TextBlock`。   |

要改变轨道背景或指示器颜色，可以覆盖相应的主题资源，或者直接设置属性：

```xml
<ProgressBar Height="20" Value="60" Maximum="100"
             Foreground="Green"
             Background="LightGray" />
```

若想做更深入的定制，可以整个换掉 `ControlTheme`：

```xml
<ProgressBar Height="20" Value="50" Maximum="100">
  <ProgressBar.Styles>
    <Style Selector="ProgressBar /template/ Border#PART_Indicator">
      <Setter Property="CornerRadius" Value="4" />
    </Style>
  </ProgressBar.Styles>
</ProgressBar>
```

## 另请参阅 {#see-also}

- [Slider](/controls/input/selectors/slider)
- [ProgressBar API 参考](/api/avalonia/controls/progressbar)
- [GitHub 上的 `ProgressBar.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ProgressBar.cs)
