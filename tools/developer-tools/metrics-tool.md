---
id: metrics-tool
title: 指标工具
description: 在 Avalonia 开发者工具中用计数器、直方图等 .NET 指标工具监控应用的健康状况，并创建自定义指标源。
doc-type: reference
---

指标是随时间上报的数值度量，通常用来监控应用健康状况并触发告警。

Meter 提供程序是 .NET 6 引入的。越来越多的库乃至 .NET 自身的组件（比如 HttpClient）开始支持它，提供颇有价值的诊断度量。

指标工具主要有四类：
- Counter——只增不减的单值度量，通常表示“累计”量，比如抛出异常的总次数。
- UpDownCounter——与 Counter 类似，但允许负增量，比如内存工作集。  
- Histogram——度量值的分布，帧渲染耗时或 HTTP 请求耗时就是例子。`Developer Tools` 还会为直方图显示颇为实用的 P50（中位数）、P90 和 P95 分位数。
- Gauge——不保留历史数据的度量，只显示最新值。**注意**：`Developer Tools` 目前还不支持。

![Histogram](/img/tools/dev-tools/metrics-histogram.png)

## 禁用/启用默认源 {#disablingenabling-default-sources}

`Developer Tools` 默认只接纳 `Avalonia` 和 `System.Runtime` 这两个 meter 提供程序。

点击 **+** 按钮即可禁用它们或启用别的。
所有工具按其 meter 提供程序分组，分组名通常就是定义它们的命名空间。

注意这份列表是动态的：只有当提供程序至少推送过一次度量之后，对应的工具才会出现。比如 HttpClient（`System.Http` 命名空间）的工具，要等第一个请求发出之后才会显示。

![Meter 筛选](/img/tools/dev-tools/meters-filter.png)

:::note

注意，`Avalonia` 的 meter 自框架 11.3.0 版本起才有，`System.Runtime` 则要 .NET 9 起才有。
若你的应用两条都不满足，默认看到的就是一张空的 meter 列表。

:::


## 编写自定义指标源 {#writing-custom-metric-sources}


关于如何编写自定义指标源，可参照 .NET 的[创建指标](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/metrics-instrumentation)文档；写好之后便可在 `Developer Tools` 或官方的 `dotnet-counters` 命令行工具中查看。

最简单的例子大致是这样：

```csharp
static Meter s_meter = new Meter("SimpleToDoList");
static UpDownCounter<int> s_tasksCount = s_meter.CreateUpDownCounter<int>("tasks.count");
static Counter<int> s_tasksResolved = s_meter.CreateCounter<int>("tasks.resolved.total");

private void OnTaskAdded() => s_tasksCount.Add(1);
private void OnTaskRemoved() => s_tasksCount.Add(-1);
private void OnTaskResolved() => s_tasksResolved.Add(1);
```

一旦代码推送过至少一次度量，这个 `SimpleToDoList` 就会出现在 **+** 按钮的浮出菜单里，可以选中它在工具中显示。

## 另请参阅 {#see-also}

- [性能分析工具](/tools/developer-tools/profiler-tool)
- [安装开发者工具](/tools/developer-tools/installation)
