---
id: index
title: 图表控件
description: Avalonia Charts 是一套 70 多种数据可视化控件和范式的库，服务于仪表板、金融、分析等各类场景。
doc-type: overview
tags:
  - avalonia pro
  - avalonia charts
---

Charts 提供一套数据可视化控件，以及成文的组合范式，可用来搭建仪表板、分析工具、金融工具、科研报告等等。工具提示、图例、交互等常见图表能力开箱即用，并与 Avalonia 的主题系统打通。

:::info
Charts 需要 [Avalonia Pro](https://avaloniaui.net/pricing)。
:::

## 快速上手 {#getting-started}

1. 运行 `dotnet add package` 安装 `Avalonia.Controls.Charts` NuGet 包。

```bash
dotnet add package Avalonia.Controls.Charts
```

2. 在可执行项目文件（`.csproj`）中填入你的 Avalonia 许可证密钥。密钥可以在 [Avalonia 门户](https://portal.avaloniaui.net)中获取。

```xml
<ItemGroup>
  <AvaloniaUILicenseKey Include="YOUR_LICENSE_KEY" />
</ItemGroup>
```

:::tip
对于多项目解决方案，可以把许可证密钥放进[环境变量](https://learn.microsoft.com/en-us/visualstudio/msbuild/how-to-use-environment-variables-in-a-build)或[共享 props 文件](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory?view=vs-2022#directorybuildprops-example)，免得到处重复。
:::

3. （可选）如果你想把 Charts 放在单独的 XML 命名空间下，可以使用 `https://avaloniaui.net/controls/charts`。这并非必需——默认的 `https://github.com/avaloniaui` 命名空间同样包含 `Avalonia.Controls.Charts`。

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:charts="https://avaloniaui.net/controls/charts">
    <StackPanel Spacing="16">
        <charts:CartesianChart Title="Revenue" Height="300" />
        <charts:SankeyChart Title="User flow" Height="300" />
    </StackPanel>
</UserControl>
```

关于安装 Avalonia Pro 控件的更多内容，请参阅[安装 Avalonia Pro](/tools/installing-avalonia-pro)。

## 适用场景举例 {#example-use-cases}

Charts 适合下列场景：

- **业务仪表板：** 用 KPI 卡片、趋势折线、条形对比和漏斗视图呈现运营数据。
- **金融应用：** 用 K 线、OHLC、平均 K 线等价格行为图表服务交易与行情分析。
- **分析与报表：** 用热力图、散点图、直方图和表格图探索并呈现数据集。
- **科学与统计视图：** 用箱线图、小提琴图、误差棒和马赛克图作分布分析。
- **流程与层级呈现：** 用桑基图、组织结构图、矩形树图和网络图呈现关系型数据。
- **地理数据：** 用分级统计图、气泡地图和热力图叠加层作区域对比。
- **进度与状态指示：** 用圆形仪表、线性仪表和液位仪表作实时监控。

## 数据源 {#data-sources}

笛卡尔系列可以通过 `ItemsSource`、`CategoryPath` 和 `ValuePath` 绑定到对象集合。对于简单的数值系列，`ItemsSource` 也可以直接是 `IList<double>`、`IList<int>`、`IList<float>`、`IList<decimal>` 或 `IList<Point>`。直接给出数值列表时，条目索引即作为类别值。

在计算取值范围和渲染连续数据时，系列会跳过 `NaN`、无穷大等非有限数值。

笛卡尔系列用 `EmptyPointMode` 控制如何处理所渲染系列中的 null 或非有限数据点。可选值有 `Zero`、`Gap`、`Average` 和 `Interpolate`，默认是 `Zero`。

## 图表的公共属性 {#common-chart-properties}

大多数图表控件通过 `ChartBase` 共享下列属性。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 显示在图表上方的文字。 | `null` |
| `Palette` | 可选的图表调色板，用于生成各系列或各条目的颜色。 | `null` |
| `LabelForeground` | 未指定更具体的标签画刷时，图表级标签所用的画刷。 | `null` |
| `PlotAreaContent` | 可选控件，摆放在实际绘图区之上。 | `null` |

若某种图表具备相应的视觉元素，它还会额外提供一些图表级的样式接口。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `AxisBrush` | 轴线、刻度、径向轴或同类刻度参考线所用的画刷。 | `null` |
| `GridLineBrush` | 图表级网格线所用的画刷。 | `null` |
| `PlotAreaBackground` | 仅用于数据绘图矩形区的画刷，不涉及整张图表的背景。 | `null` |

## 系列的公共属性 {#common-series-properties}

大多数系列通过 `ChartSeries` 共享下列属性。各图表页面还会列出其特定系列类型的额外属性。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `Title` | 在图例和自动生成的工具提示中显示的系列名称。 | `null` |
| `ItemsSource` | 该系列所用的数据集合。 | `null` |
| `ValuePath` | 主数值所用的属性路径。 | `null` |
| `Fill` | 填充系列区域或条目内部所用的画刷。 | `null` |
| `Stroke` | 系列轮廓、线条或条目边框所用的画刷。 | `null` |
| `StrokeThickness` | 基准线条粗细。部分默认主题会为特定类型设定专门的值。 | `1.0` |
| `PointBrushPath` | 可选的属性路径，用于为每个数据项解析出一个 `IBrush`。支持该特性的系列会把它用在各个数据点、标记、分段或扇区上。 | `null` |

## Animation

图表与系列共用同一套动画流水线。

| 属性 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `IsAnimationEnabled` | 启用图表的入场动画。 | `true` |
| `AnimationDuration` | 图表入场动画的时长。 | `00:00:01` |
| `Easing` | 作用于图表动画进度的缓动函数。 | `CubicEaseOut` |
| `AnimationDelay` | 系列级的延迟：动画开始前先等这么久。 | `00:00:00` |
| `AnimationProgress` | 系列级的动画进度，从 `0.0` 到 `1.0`。 | `1.0` |

## Extensibility

自定义笛卡尔系列需派生自 `CartesianSeries` 并实现 `RenderSeries(in SeriesRenderContext context)`。渲染上下文会提供图表实例、绘图区、类别映射、视口范围以及已解析的画刷，供系列的绘制逻辑取用。系列可以重写 `CreateLegendItem` 来定制自己的图例标记，也可以通过 `GetDataPoints()` 或相关的区间、极坐标数据点结构体对外提供数据，供范围计算、工具提示和交互使用。升级既有的自定义笛卡尔系列时，请把原先 `TryRenderSelf(...)` 中的渲染逻辑挪进 `RenderSeries(in SeriesRenderContext context)`。

金融叠加层只要实现 `IFinancialChartOverlaySeries`，就能在 `FinancialChart` 中绘制。叠加层特有的行为请参阅[金融图表](/controls/data-display/charts/financial/financial-chart)。

## 图表分类 {#chart-categories}

### 分析与 KPI 类 {#analytics-and-kpi-charts}

用于概括指标、发现规律、呈现结论的图表。

| 图表 | 说明 |
| --- | --- |
| [KPI 卡片](/controls/data-display/charts/analytics/kpi-card) | 展示一项关键指标，并配上趋势指示和迷你走势图。 |
| [热力图](/controls/data-display/charts/analytics/heatmap-chart) | 把一组数值以带颜色编码的网格呈现出来。 |
| [漏斗图](/controls/data-display/charts/analytics/funnel-chart) | 呈现一条逐级递减的顺序流程。 |
| [华夫图](/controls/data-display/charts/analytics/waffle-chart) | 用网格中点亮的格子表示百分比。 |
| [词云](/controls/data-display/charts/analytics/word-cloud-chart) | 按词频决定字号，凸显数据集中的高频词。 |
| [子弹图](/controls/data-display/charts/analytics/bullet-chart) | 在紧凑的版面里把主值与目标值及定性区间作对比。 |
| [日历热力图](/controls/data-display/charts/analytics/calendar-heatmap-chart) | 在逐周排布的日历网格中呈现每天的活跃强度。 |
| [矩阵图](/controls/data-display/charts/analytics/matrix-chart) | 用网格呈现两组类别之间的关系。 |
| [表格图](/controls/data-display/charts/analytics/table-chart) | 以行列形式呈现数据，并可按条件设置格式。 |
| [凹凸图](/controls/data-display/charts/analytics/bump-chart) | Tracks rank changes over time using crossed lines. |
| [斜率图](/controls/data-display/charts/analytics/slope-chart) | Compares values at two points in time using angled lines. |
| [Pyramid chart](/controls/data-display/charts/analytics/pyramid-chart) | Stacks segments vertically to show hierarchical or sequential proportions. |
| [Theme river chart](/controls/data-display/charts/analytics/theme-river-chart) | Builds a theme-river-style layout with stacked area series and a centered spacer offset. |
| [Pictorial bar chart](/controls/data-display/charts/analytics/pictorial-bar-chart) | Replaces standard bars with icons or shapes sized by value. |

### Bubble and packed charts

Charts that encode magnitude with marker size and often omit traditional axes or grids.

| 图表 | 说明 |
| --- | --- |
| [气泡图](/controls/data-display/charts/bubble/bubble-chart) | Plots X and Y values and uses bubble size for a third measure. |
| [气泡云图](/controls/data-display/charts/bubble/bubble-cloud-chart) | Arranges sized bubbles in an organic, clustered layout without axes. |
| [紧凑气泡图](/controls/data-display/charts/bubble/packed-bubble-chart) | Packs category bubbles tightly into a compact space for part-to-whole comparison. |

### Cartesian charts

Charts that plot data on horizontal and vertical axes. Use these for trends, comparisons, distributions, and correlations.

| 图表 | 说明 |
| --- | --- |
| [条形图](/controls/data-display/charts/cartesian/bar-chart) | Compares discrete quantities across categories using rectangular bars. |
| [折线图](/controls/data-display/charts/cartesian/line-chart) | Connects data points with straight segments to show trends over time. |
| [面积图](/controls/data-display/charts/cartesian/area-chart) | Fills the area below a line to emphasize cumulative totals or volume. |
| [组合图](/controls/data-display/charts/cartesian/combo-chart) | Combines multiple Cartesian series types on one plot, with optional secondary Y-axis support. |
| [散点图](/controls/data-display/charts/cartesian/scatter-chart) | Plots individual data points to reveal correlations between two variables. |
| [样条图](/controls/data-display/charts/cartesian/spline-chart) | Connects data points with curved lines to show gradual changes in time-dependent data. |
| [Step line chart](/controls/data-display/charts/cartesian/step-line-chart) | Connects points with horizontal and vertical steps for discrete state changes. |
| [堆叠条形图](/controls/data-display/charts/cartesian/stacked-bar-chart) | Shows part-to-whole relationships across categories using stacked bars. |
| [Stacked area chart](/controls/data-display/charts/cartesian/stacked-area-chart) | Shows cumulative totals over time using stacked filled areas. |
| [Range area chart](/controls/data-display/charts/cartesian/range-area-chart) | Displays high-low ranges as a filled band between two values. |
| [瀑布图](/controls/data-display/charts/cartesian/waterfall-chart) | Shows how an initial value changes through a series of positive and negative contributions. |
| [Histogram chart](/controls/data-display/charts/cartesian/histogram-chart) | Groups continuous values into bins to show frequency distribution. |
| [Pareto chart](/controls/data-display/charts/cartesian/pareto-chart) | Combines bars and a cumulative line to identify significant factors. |

### Circular charts

Charts that represent data as segments of a circle.

| 图表 | 说明 |
| --- | --- |
| [饼图](/controls/data-display/charts/circular/pie-chart) | Divides a circle into proportional slices to show part-to-whole relationships. |
| [Donut chart](/controls/data-display/charts/circular/donut-chart) | A pie chart with a hollow center, often used to display a total in the middle. |
| [Semi-donut chart](/controls/data-display/charts/circular/semi-donut-chart) | A half-circle donut for compact part-to-whole views. |

### Comparison charts

Charts for before-and-after analysis, back-to-back comparison, and proportional allocation.

| 图表 | 说明 |
| --- | --- |
| [双向条形图](/controls/data-display/charts/comparison/diverging-bar-chart) | Extends bars left and right from a centered baseline. |
| [Dumbbell chart](/controls/data-display/charts/comparison/dumbbell-chart) | Connects two values per category with a line and markers. |
| [Mekko 图](/controls/data-display/charts/comparison/mekko-chart) | Combines variable-width columns with stacked segments to show size and composition. |
| [镜像条形图](/controls/data-display/charts/comparison/mirror-bar-chart) | Places two bar series back to back around a center line. |
| [议席图](/controls/data-display/charts/comparison/parliament-chart) | Displays seat distribution in a hemicycle layout. |
| [人口金字塔图](/controls/data-display/charts/comparison/population-pyramid-chart) | Shows two opposing population distributions by ordered bands. |
| [龙卷风图](/controls/data-display/charts/comparison/tornado-chart) | Draws bidirectional horizontal bars for sensitivity or ranked comparisons. |
| [Venn diagram chart](/controls/data-display/charts/comparison/venn-diagram-chart) | Visualizes set overlap and intersection values. |

### Engineering and scientific charts

Charts for technical surfaces, multivariate scientific views, and specialized coordinate systems.

| 图表 | 说明 |
| --- | --- |
| [地毯图](/controls/data-display/charts/engineering/carpet-plot-chart) | Maps two independent variables and one dependent variable onto a skewed grid. |
| [Hexbin chart](/controls/data-display/charts/engineering/hexbin-chart) | Aggregates dense 2D point clouds into hexagonal density bins. |
| [史密斯圆图](/controls/data-display/charts/engineering/smith-chart) | Visualizes complex impedance or admittance data on a normalized radio frequency grid. |
| [三元图](/controls/data-display/charts/engineering/ternary-chart) | Plots three-part compositions that sum to a constant. |
| [风玫瑰图](/controls/data-display/charts/engineering/wind-rose-chart) | Shows directional frequency distributions as stacked polar sectors. |

### Financial charts

Specialized charts for price and market data analysis.

| 图表 | 说明 |
| --- | --- |
| [金融图表](/controls/data-display/charts/financial/financial-chart) | Hosts financial series such as candlestick and OHLC on shared price axes. |
| [K 线图](/controls/data-display/charts/financial/candlestick-chart) | Shows open, high, low, and close prices per period as candle shapes. |
| [OHLC 图](/controls/data-display/charts/financial/ohlc-chart) | Displays OHLC price data as vertical bars with tick marks. |
| [Heikin-Ashi chart](/controls/data-display/charts/financial/heikin-ashi-chart) | A smoothed candlestick variant that filters out short-term noise. |
| [Hilo chart](/controls/data-display/charts/financial/hilo-chart) | Plots only the high and low values per period as a vertical line. |
| [Kagi chart](/controls/data-display/charts/financial/kagi-chart) | Filters small price moves to show significant direction changes. |
| [Renko chart](/controls/data-display/charts/financial/renko-chart) | Plots price movement as fixed-size bricks, ignoring time. |
| [Point and figure chart](/controls/data-display/charts/financial/point-and-figure-chart) | Uses columns of X and O symbols to track supply and demand. |

### Gauges

Visual displays of a single value relative to a range. Common in monitoring dashboards and real-time status panels.

| 图表 | 说明 |
| --- | --- |
| [圆形仪表](/controls/data-display/charts/gauges/circular-gauge-chart) | A dial-style gauge with a needle or arc indicator. |
| [仪表图](/controls/data-display/charts/gauges/gauge-chart) | Displays a single value on a semi-circular dial with optional needle. |
| [Linear gauge](/controls/data-display/charts/gauges/linear-gauge-chart) | A horizontal or vertical track with a pointer or fill. |
| [Gradient ring chart](/controls/data-display/charts/gauges/gradient-ring-chart) | Draws multiple concentric progress rings against a shared maximum. |
| [Liquid fill gauge](/controls/data-display/charts/gauges/liquid-fill-gauge) | Represents a percentage as a rising liquid level inside a shape. |
| [Progress donut](/controls/data-display/charts/gauges/progress-donut-chart) | A circular arc that fills proportionally to indicate progress. |

### Hierarchy and flow charts

Charts for visualizing relationships, flows, and tree structures.

| 图表 | 说明 |
| --- | --- |
| [流程图](/controls/data-display/charts/hierarchy/flow-chart) | Visualizes workflows, decision trees, and system maps using nodes and directed edges. |
| [Sankey chart](/controls/data-display/charts/hierarchy/sankey-chart) | Shows flow quantities between nodes using proportional bands. |
| [Alluvial chart](/controls/data-display/charts/hierarchy/alluvial-chart) | Tracks how items transition between categories across stages. |
| [矩形树图](/controls/data-display/charts/hierarchy/treemap-chart) | Represents hierarchical data as nested rectangles sized by value. |
| [Sunburst chart](/controls/data-display/charts/hierarchy/sunburst-chart) | Displays hierarchy as concentric rings radiating from a center. |
| [圆堆积图](/controls/data-display/charts/hierarchy/circle-packing-chart) | Nests circles to represent hierarchical proportions. |
| [Flame graph](/controls/data-display/charts/hierarchy/flame-graph) | Shows hierarchical stacks of cost or duration data from bottom to top. |
| [Icicle chart](/controls/data-display/charts/hierarchy/icicle-chart) | Shows hierarchy as stacked rectangular bands from top to bottom. |
| [Dendrogram chart](/controls/data-display/charts/hierarchy/dendrogram-chart) | A tree diagram used in clustering and classification contexts. |
| [Indented tree chart](/controls/data-display/charts/hierarchy/indented-tree-chart) | Displays hierarchy as an indented list with expandable nodes. |
| [Radial tree chart](/controls/data-display/charts/hierarchy/radial-tree-chart) | Arranges a tree hierarchy in a circular layout. |
| [Organization chart](/controls/data-display/charts/hierarchy/organization-chart) | Visualizes reporting structures and team hierarchies. |
| [思维导图](/controls/data-display/charts/hierarchy/mindmap-chart) | Builds an ideation layout on top of `FlowChart` with diverging nodes and links. |
| [Network chart](/controls/data-display/charts/hierarchy/network-chart) | Plots nodes and edges to show relationships without a fixed hierarchy. |
| [Force-directed graph](/controls/data-display/charts/hierarchy/force-directed-graph) | Arranges nodes using simulated physical forces to reveal clusters. |
| [Chord diagram](/controls/data-display/charts/hierarchy/chord-diagram) | Shows pairwise relationships between entities as arcs around a circle. |
| [Arc diagram](/controls/data-display/charts/hierarchy/arc-diagram-chart) | Displays connections between nodes laid out on a straight axis. |
| [工序流程图](/controls/data-display/charts/hierarchy/process-flow-chart) | Uses `FlowChart` to represent sequential or branching workflows. |

### Maps

Charts that overlay data onto geographic or custom spatial layouts.

| 图表 | 说明 |
| --- | --- |
| [Choropleth map](/controls/data-display/charts/maps/choropleth-map-chart) | Colors map regions by a numeric value to show geographic distribution. |
| [Bubble map](/controls/data-display/charts/maps/bubble-map-chart) | Places sized circles on a map to represent values at specific locations. |
| [Heatmap](/controls/data-display/charts/maps/heatmap-map-chart) | Applies a color gradient over a map to show intensity or density. |
| [Shape map](/controls/data-display/charts/maps/shape-map-chart) | Renders custom regions as a data-driven map. |
| [Seat map](/controls/data-display/charts/maps/seat-map-chart) | Displays venue or floor-plan layouts with interactive seat selection. |

### Radial charts

Charts that use a circular coordinate system rather than Cartesian axes.

| 图表 | 说明 |
| --- | --- |
| [极坐标图](/controls/data-display/charts/radial/polar-chart) | Plots arbitrary angle and radius values in a polar coordinate system. |
| [Radar chart](/controls/data-display/charts/radial/radar-chart) | Plots multivariate data as a polygon on a circular grid of axes. |
| [Polar area chart](/controls/data-display/charts/radial/polar-area-chart) | Divides a circle into equal-angle segments sized by value. |
| [Nightingale Rose chart](/controls/data-display/charts/radial/nightingale-rose-chart) | A polar area chart where radius, not area, encodes the value. |
| [Radial bar chart](/controls/data-display/charts/radial/radial-bar-chart) | Displays categories as arcs of varying length around a center point. |
| [Radial line chart](/controls/data-display/charts/radial/radial-line-chart) | A line chart projected onto a circular axis. |

### Scheduling and timeline charts

Charts for time-based planning, project management, and sequential data.

| 图表 | 说明 |
| --- | --- |
| [Gantt chart](/controls/data-display/charts/scheduling/gantt-chart) | Shows tasks and their durations across a horizontal time axis. |
| [时间线图](/controls/data-display/charts/scheduling/timeline-chart) | Displays events in chronological order along a linear axis. |
| [Swimlane chart](/controls/data-display/charts/scheduling/swimlane-chart) | Organizes tasks into parallel rows to show ownership or phase. |
| [Spiral timeline chart](/controls/data-display/charts/scheduling/spiral-timeline-chart) | Arranges time-based data along a spiral for cyclical patterns. |
| [Sparkline chart](/controls/data-display/charts/scheduling/sparkline-chart) | An inline miniature chart for showing trends within a small space. |

### Statistical charts

Charts for distributional and comparative statistical analysis.

| 图表 | 说明 |
| --- | --- |
| [Beeswarm plot chart](/controls/data-display/charts/statistical/beeswarm-plot-chart) | Displays individual observations as non-overlapping dots within each category. |
| [Box plot chart](/controls/data-display/charts/statistical/boxplot-chart) | Summarizes a distribution using medians, quartiles, and outliers. |
| [等值线图](/controls/data-display/charts/statistical/contour-plot-chart) | Displays 2D scalar fields as contour lines and optional filled bands. |
| [Density plot chart](/controls/data-display/charts/statistical/density-plot-chart) | Uses kernel density estimation to render a smooth distribution curve. |
| [Error bar chart](/controls/data-display/charts/statistical/error-bar-chart) | Adds error or uncertainty indicators to data points. |
| [Mosaic chart](/controls/data-display/charts/statistical/mosaic-chart) | Visualizes proportions across two categorical variables as nested rectangles. |
| [平行坐标图](/controls/data-display/charts/statistical/parallel-coordinates-chart) | Compares multivariate records as lines across parallel axes. |
| [Ridgeline chart](/controls/data-display/charts/statistical/ridgeline-chart) | Stacks multiple overlapping distributions for shape comparison. |
| [Strip plot chart](/controls/data-display/charts/statistical/strip-plot-chart) | Displays individual observations per category with jitter and optional mean lines. |
| [Violin plot chart](/controls/data-display/charts/statistical/violin-plot-chart) | Combines a box plot with a kernel density shape to show distribution. |

## Shared elements

Most chart types share the following configurable elements:

| 元素 | 说明 |
| --- | --- |
| [Legend](/controls/data-display/charts/shared-elements/legend-chart) | Identifies each data series by name and color. |
| [Tooltip](/controls/data-display/charts/shared-elements/tooltip-chart) | Shows data values on hover or tap. |
| [Crosshairs](/controls/data-display/charts/shared-elements/crosshairs-chart) | Draws intersecting lines that follow the pointer across the chart. |
| [Data labels](/controls/data-display/charts/shared-elements/data-labels-chart) | Renders the value of each data point directly on the chart. |
| [Chart export](/controls/data-display/charts/shared-elements/export-chart) | Saves a chart view to a PNG or JPEG file, PNG stream, or save dialog. |
| [Markers](/controls/data-display/charts/shared-elements/markers-chart) | Adds point symbols at each data value. |
| [Trendline](/controls/data-display/charts/shared-elements/trendline-chart) | Overlays a regression or moving-average line on a series. |
| [Annotations](/controls/data-display/charts/shared-elements/annotations-chart) | Places labels, lines, or shapes at specific data coordinates. |
| [坐标轴定制](/controls/data-display/charts/shared-elements/axis-customization-chart) | Controls tick marks, labels, gridlines, and scale. |
| [Interactions](/controls/data-display/charts/shared-elements/interactions-chart) | Configures zoom, pan, selection, hover highlighting, and trackball behavior. |

## 另请参阅 {#see-also}

- [Avalonia Pro pricing and access](https://avaloniaui.net/pricing)
