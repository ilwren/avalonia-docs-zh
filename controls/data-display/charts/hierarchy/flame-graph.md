---
id: flame-graph
title: 火焰图
description: 自下而上呈现层级化的调用栈数据，常用于性能剖析和调用链分析。
doc-type: reference
tags:
  - avalonia pro
---

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

火焰图把层级化的开销、耗时或采样数据画成层层堆叠的矩形，根部在最下方，越往上调用层级越深。

## 适用场景 {#when-to-use}

- **剖析器输出**：在调用树中找出 CPU、内存或耗时的热点。
- **调用链检视**：弄清时间都耗在哪些嵌套操作上。
- **层级开销梳理**：在开销大的分支之间比较深度与宽度。

## 代码示例 {#code-example}

### XAML

```xml
<FlameGraph xmlns="https://github.com/avaloniaui" Title="CPU profile"
                             Height="320"
                             ItemsSource="{Binding StackTraceData}"
                             ValuePath="Duration"
                             LabelPath="MethodName"
                             ChildrenPath="SubCalls" />
```

### 数据模型（C#） {#data-model-c}

```csharp
public class FlameNode
{
    public string MethodName { get; set; } = string.Empty;
    public double Duration { get; set; }
    public ObservableCollection<FlameNode> SubCalls { get; set; } = new();
}

public ObservableCollection<FlameNode> StackTraceData { get; } = new()
{
    new FlameNode
    {
        MethodName = "Program.Main",
        Duration = 2000,
        SubCalls =
        {
            new FlameNode
            {
                MethodName = "App.OnFrameworkInitializationCompleted",
                Duration = 1950,
                SubCalls =
                {
                    new FlameNode { MethodName = "App.Initialize", Duration = 50 },
                    new FlameNode { MethodName = "Window.Show", Duration = 100 },
                    new FlameNode { MethodName = "Dispatcher.MainLoop", Duration = 1800 }
                }
            }
        }
    }
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 火焰图的根集合。 | `null` |
| `ValuePath` | 指向决定矩形宽度那个数值的路径。 | `null` |
| `LabelPath` | 指向项标签的路径。 | `null` |
| `ChildrenPath` | 指向子集合的路径。 | `null` |

## 另请参阅 {#see-also}

- [矩形树图](/controls/data-display/charts/hierarchy/treemap-chart)
- [流程图](/controls/data-display/charts/hierarchy/flow-chart)
