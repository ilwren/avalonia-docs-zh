---
id: export-chart
title: 图表导出
description: 通过异步 API 把图表控件导出为 PNG 或 JPEG 文件、PNG 流，或经由交互式保存对话框导出。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

图表控件从 `ChartBase` 继承了导出 API。用 `ExportAsync` 即可把当前图表视图渲染成图片文件、PNG 流，或交由保存对话框处理。

## 适用场景 {#when-to-use}

- **报表**：为生成的报表保存一张图表图片。
- **用户导出**：让用户在应用中保存当前的图表视图。
- **快照**：为需要位图输出的流程渲染图表图片。

## 代码示例 {#code-example}

### 导出为文件 {#export-to-file}

```csharp
var result = await chart.ExportAsync("sales-chart.png", width: 1200, height: 800, dpi: 144);

if (!result.Succeeded)
{
    // Use result.Canceled or result.Exception to handle the outcome.
}
```

### 导出为流 {#export-to-stream}

```csharp
await using var stream = System.IO.File.Create("sales-chart.png");
var result = await chart.ExportAsync(stream, width: 1200, height: 800);
```

## 方法 {#methods}

| 方法 | 说明 | 结果 |
| :--- | :--- | :--- |
| `ExportAsync(string path, int? width = null, int? height = null, double dpi = 96, CancellationToken cancellationToken = default)` | 导出到指定文件路径。若路径不带扩展名，则自动追加 `.png`。文件导出支持 PNG 和 JPEG。 | `ChartExportResult` |
| `ExportAsync(Stream stream, int? width = null, int? height = null, double dpi = 96, CancellationToken cancellationToken = default)` | 把 PNG 图片导出到流。 | `ChartExportResult` |
| `ExportAsync(CancellationToken cancellationToken = default)` | 弹出保存文件选择器，并导出到用户选定的文件。 | `ChartExportResult` |

## 结果与事件 {#result-and-events}

| 成员 | 说明 |
| :--- | :--- |
| `ChartExportResult.Succeeded` | 导出成功完成时为 `true`。 |
| `ChartExportResult.Canceled` | 导出被取消时为 `true`。 |
| `ChartExportResult.Target` | 文件路径或目标说明，比如 `stream`。 |
| `ChartExportResult.Exception` | 导致导出失败的异常（若有）。 |
| `ExportCompleted` | 导出成功后触发。事件数据提供 `Result` 和 `Target`。 |
| `ExportFailed` | 导出失败后触发。事件数据提供 `Target` 和 `Exception`。 |

## 注释支持情况 {#notes}

- `width` 和 `height` 默认取图表自身的尺寸，且必须解析为正值。
- 取消操作会返回一个标记为已取消的 `ChartExportResult`，并且不会触发 `ExportFailed`。
- 路径无效、尺寸无效以及流错误都会返回一个标记为失败的 `ChartExportResult`，并触发 `ExportFailed`。

## 另请参阅 {#see-also}

- [Interactions](/controls/data-display/charts/shared-elements/interactions-chart)
- [Legend](/controls/data-display/charts/shared-elements/legend-chart)
