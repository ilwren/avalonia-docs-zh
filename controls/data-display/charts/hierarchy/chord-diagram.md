---
id: chord-diagram
title: 和弦图
description: 以环形版面呈现实体之间的相互关系，最适合表现贸易、迁徙这类复杂的有向流动。
doc-type: reference
tags:
  - avalonia pro
---

import chartsFlowChord from '/img/controls/charts/charts-flow-chord.png';

:::info
[图表](/controls/data-display/charts)需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

和弦图以环形版面呈现各实体之间的相互关系。要展现一组事物之间复杂的有向流动，用它正合适。

<Image light={chartsFlowChord} maxWidth={400} position="center" cornerRadius="true" alt="Chord diagram showing directional flows between entities arranged in a circle with connecting chords of varying widths." />

## 适用场景 {#when-to-use}
- **贸易往来**：呈现国家之间的进出口关系。
- **迁徙模式**：展示人口在不同地区之间的流动。
- **系统交互**：呈现软件系统中各模块之间的调用依赖。

## 代码示例 {#code-example}

### XAML
```xml
<ChordDiagramChart xmlns="https://github.com/avaloniaui" Name="ChordDiagramSample" Title="Trade Relations" Height="350"
                            ItemsSource="{Binding ChordData}"
                            SourcePath="Source"
                            TargetPath="Target"
                            ValuePath="Value" />
```

### 数据模型（C#） {#data-model-c}
```csharp
public record TradeLink(string Source, string Target, double Value);

public ObservableCollection<TradeLink> ChordData { get; } = new()
{
    new("USA", "China", 50),
    new("USA", "Europe", 40),
    new("Europe", "China", 30),
    new("China", "USA", 45),
    new("Europe", "USA", 35)
};
```

## 常用属性 {#common-properties}

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `ItemsSource` | 各条关系的集合。 | `null` |
| `SourcePath` | 指向起点实体的路径。 | `null` |
| `TargetPath` | 指向终点实体的路径。 | `null` |
| `ValuePath` | 指向关系强度/权重的路径。 | `null` |
| `ArcPadding` | 外环上各段之间的角度间隔。 | `0.02` |
| `ArcThickness` | 外弧的粗细。 | `20.0` |
| `ChordOpacity` | 连接和弦所用的不透明度。 | `0.6` |
| `ShowLabels` | 是否为外弧显示标签。 | `true` |
