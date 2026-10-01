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
| [凹凸图](/controls/data-display/charts/analytics/bump-chart) | 用交错的折线追踪名次随时间的变化。 |
| [斜率图](/controls/data-display/charts/analytics/slope-chart) | 用斜线比较两个时间点上的数值。 |
| [金字塔图](/controls/data-display/charts/analytics/pyramid-chart) | 把各段自上而下堆叠，呈现层级或顺序上的占比。 |
| [主题河流图](/controls/data-display/charts/analytics/theme-river-chart) | 用堆叠面积系列加居中的留白偏移，搭出主题河流式的版面。 |
| [图形条形图](/controls/data-display/charts/analytics/pictorial-bar-chart) | 用大小随数值变化的图标或形状取代普通条形。 |

### 气泡与堆积类 {#bubble-and-packed-charts}

用标记大小表示量级的图表，通常不设传统的坐标轴或网格。

| 图表 | 说明 |
| --- | --- |
| [气泡图](/controls/data-display/charts/bubble/bubble-chart) | 绘制 X、Y 值，并用气泡大小表示第三个指标。 |
| [气泡云图](/controls/data-display/charts/bubble/bubble-cloud-chart) | 不设坐标轴，把大小不一的气泡自然地聚成一簇。 |
| [紧凑气泡图](/controls/data-display/charts/bubble/packed-bubble-chart) | 把类别气泡紧密码进有限空间，用于部分与整体的比较。 |

### 笛卡尔类 {#cartesian-charts}

在横纵坐标轴上绘制数据的图表。趋势、对比、分布和相关性分析都靠它们。

| 图表 | 说明 |
| --- | --- |
| [条形图](/controls/data-display/charts/cartesian/bar-chart) | 用矩形条比较各类别之间的离散数量。 |
| [折线图](/controls/data-display/charts/cartesian/line-chart) | 用直线段连接数据点，呈现随时间的走势。 |
| [面积图](/controls/data-display/charts/cartesian/area-chart) | 填充折线下方的区域，强调累计总量或体量。 |
| [组合图](/controls/data-display/charts/cartesian/combo-chart) | 在同一张图上组合多种笛卡尔系列，并可选支持次 Y 轴。 |
| [散点图](/controls/data-display/charts/cartesian/scatter-chart) | 绘制一个个数据点，揭示两个变量之间的相关性。 |
| [样条图](/controls/data-display/charts/cartesian/spline-chart) | 用曲线连接数据点，呈现时序数据的平缓变化。 |
| [阶梯折线图](/controls/data-display/charts/cartesian/step-line-chart) | 用横竖阶梯连接各点，表现离散的状态跃迁。 |
| [堆叠条形图](/controls/data-display/charts/cartesian/stacked-bar-chart) | 用堆叠条形呈现各类别中部分与整体的关系。 |
| [堆叠面积图](/controls/data-display/charts/cartesian/stacked-area-chart) | 用层层堆叠的填充面积呈现随时间的累计总量。 |
| [区间面积图](/controls/data-display/charts/cartesian/range-area-chart) | 把高低区间画成两个数值之间的填充带。 |
| [瀑布图](/controls/data-display/charts/cartesian/waterfall-chart) | 呈现初始值如何在一连串正负变动中改变。 |
| [直方图](/controls/data-display/charts/cartesian/histogram-chart) | 把连续数值分入区间，呈现频数分布。 |
| [帕累托图](/controls/data-display/charts/cartesian/pareto-chart) | 结合条形与累计折线，找出起决定作用的因素。 |

### 环形类 {#circular-charts}

把数据表示为圆的各个扇段的图表。

| 图表 | 说明 |
| --- | --- |
| [饼图](/controls/data-display/charts/circular/pie-chart) | 把圆按比例切分成扇形，呈现部分与整体的关系。 |
| [环形图](/controls/data-display/charts/circular/donut-chart) | 中心镂空的饼图，常在中间显示总计。 |
| [半环形图](/controls/data-display/charts/circular/semi-donut-chart) | 半圆形的环形图，适合紧凑的部分与整体视图。 |

### 对比类 {#comparison-charts}

用于前后对比、背靠背比较和按比例分配的图表。

| 图表 | 说明 |
| --- | --- |
| [双向条形图](/controls/data-display/charts/comparison/diverging-bar-chart) | 条形从居中的基准线向左右两侧延伸。 |
| [哑铃图](/controls/data-display/charts/comparison/dumbbell-chart) | 用一条连线和两个标记点连接每个类别的两个数值。 |
| [Mekko 图](/controls/data-display/charts/comparison/mekko-chart) | 把宽度不等的柱子与堆叠分段结合，同时呈现规模与构成。 |
| [镜像条形图](/controls/data-display/charts/comparison/mirror-bar-chart) | 把两组条形系列以中线为轴背靠背排布。 |
| [议席图](/controls/data-display/charts/comparison/parliament-chart) | 以半圆形版面呈现议席分布。 |
| [人口金字塔图](/controls/data-display/charts/comparison/population-pyramid-chart) | 按有序分段呈现相对的两组人口分布。 |
| [龙卷风图](/controls/data-display/charts/comparison/tornado-chart) | 绘制双向横条，用于敏感性分析或带排名的对比。 |
| [韦恩图](/controls/data-display/charts/comparison/venn-diagram-chart) | 呈现集合之间的重叠与交集数值。 |

### 工程与科学类 {#engineering-and-scientific-charts}

用于技术曲面、多变量科学视图和专用坐标系的图表。

| 图表 | 说明 |
| --- | --- |
| [地毯图](/controls/data-display/charts/engineering/carpet-plot-chart) | 把两个自变量和一个因变量映射到倾斜的网格上。 |
| [六边形分箱图](/controls/data-display/charts/engineering/hexbin-chart) | 把密集的二维点云聚合成六边形密度分箱。 |
| [史密斯圆图](/controls/data-display/charts/engineering/smith-chart) | 在归一化的射频网格上呈现复阻抗或复导纳数据。 |
| [三元图](/controls/data-display/charts/engineering/ternary-chart) | 绘制三者之和恒定的三元组成。 |
| [风玫瑰图](/controls/data-display/charts/engineering/wind-rose-chart) | 以堆叠的极坐标扇区呈现各方向上的频数分布。 |

### 金融类 {#financial-charts}

专门用于价格与行情数据分析的图表。

| 图表 | 说明 |
| --- | --- |
| [金融图表](/controls/data-display/charts/financial/financial-chart) | 在共享的价格坐标轴上承载 K 线、OHLC 等金融系列。 |
| [K 线图](/controls/data-display/charts/financial/candlestick-chart) | 用蜡烛形状展示每个周期的开、高、低、收价格。 |
| [OHLC 图](/controls/data-display/charts/financial/ohlc-chart) | 用带刻度的竖向柱体呈现 OHLC 价格数据。 |
| [平均 K 线图](/controls/data-display/charts/financial/heikin-ashi-chart) | 经过平滑的 K 线变体，滤除短期噪声。 |
| [高低图](/controls/data-display/charts/financial/hilo-chart) | 只用一条竖线绘出每个周期的最高价和最低价。 |
| [卡吉图](/controls/data-display/charts/financial/kagi-chart) | 滤掉小幅价格波动，只显示显著的方向变化。 |
| [砖形图](/controls/data-display/charts/financial/renko-chart) | 用大小固定的砖块表示价格变动，忽略时间维度。 |
| [点数图](/controls/data-display/charts/financial/point-and-figure-chart) | 用一列列 X 和 O 符号追踪供需变化。 |

### Gauges

把单个数值放在一个取值范围内直观呈现。监控仪表板和实时状态面板中很常见。

| 图表 | 说明 |
| --- | --- |
| [圆形仪表](/controls/data-display/charts/gauges/circular-gauge-chart) | 带指针或弧形指示的表盘式仪表。 |
| [仪表图](/controls/data-display/charts/gauges/gauge-chart) | 在半圆形表盘上呈现单个数值，可选配指针。 |
| [线性仪表](/controls/data-display/charts/gauges/linear-gauge-chart) | 带指针或填充的横向或纵向轨道。 |
| [渐变圆环图](/controls/data-display/charts/gauges/gradient-ring-chart) | 以共享的最大值为参照，绘制多个同心进度环。 |
| [液位仪表](/controls/data-display/charts/gauges/liquid-fill-gauge) | 用形状内不断上升的液面表示百分比。 |
| [进度环形图](/controls/data-display/charts/gauges/progress-donut-chart) | 按比例填充的圆弧，用来指示进度。 |

### 层级与流向类 {#hierarchy-and-flow-charts}

用于呈现关系、流动和树状结构的图表。

| 图表 | 说明 |
| --- | --- |
| [流程图](/controls/data-display/charts/hierarchy/flow-chart) | 用节点和有向边呈现工作流、决策树和系统图。 |
| [桑基图](/controls/data-display/charts/hierarchy/sankey-chart) | 用宽度成比例的色带呈现节点之间的流量。 |
| [冲积图](/controls/data-display/charts/hierarchy/alluvial-chart) | 追踪事项在各阶段之间于不同类别间的流转。 |
| [矩形树图](/controls/data-display/charts/hierarchy/treemap-chart) | 把层级数据画成按数值定尺寸的嵌套矩形。 |
| [旭日图](/controls/data-display/charts/hierarchy/sunburst-chart) | 以自中心向外辐射的同心环呈现层级。 |
| [圆堆积图](/controls/data-display/charts/hierarchy/circle-packing-chart) | 用层层嵌套的圆表示层级占比。 |
| [火焰图](/controls/data-display/charts/hierarchy/flame-graph) | 自下而上呈现层级化的开销或耗时数据。 |
| [冰柱图](/controls/data-display/charts/hierarchy/icicle-chart) | 自上而下以一排排矩形带呈现层级。 |
| [聚类树图](/controls/data-display/charts/hierarchy/dendrogram-chart) | 用于聚类和分类场景的树状图。 |
| [缩进树图](/controls/data-display/charts/hierarchy/indented-tree-chart) | 以可展开节点的缩进列表呈现层级。 |
| [径向树图](/controls/data-display/charts/hierarchy/radial-tree-chart) | 以环形版面排布树状层级。 |
| [组织结构图](/controls/data-display/charts/hierarchy/organization-chart) | 呈现汇报关系和团队层级。 |
| [思维导图](/controls/data-display/charts/hierarchy/mindmap-chart) | 在 `FlowChart` 之上搭出发散式的节点与连接，用于梳理想法。 |
| [网络图](/controls/data-display/charts/hierarchy/network-chart) | 绘制节点和边，呈现不依赖固定层级的关系。 |
| [力导向图](/controls/data-display/charts/hierarchy/force-directed-graph) | 借助模拟的物理作用力排布节点，揭示簇群。 |
| [和弦图](/controls/data-display/charts/hierarchy/chord-diagram) | 以圆周上的弧线呈现实体之间的两两关系。 |
| [弧线图](/controls/data-display/charts/hierarchy/arc-diagram-chart) | 呈现沿直线轴排布的节点之间的连接。 |
| [工序流程图](/controls/data-display/charts/hierarchy/process-flow-chart) | 用 `FlowChart` 呈现顺序式或分支式的工作流。 |

### Maps

把数据叠加到地理版图或自定义空间版面上的图表。

| 图表 | 说明 |
| --- | --- |
| [分级统计地图](/controls/data-display/charts/maps/choropleth-map-chart) | 按数值给地图各区域着色，呈现地理分布。 |
| [气泡地图](/controls/data-display/charts/maps/bubble-map-chart) | 在地图上放置大小不等的圆，表示各地点的数值。 |
| [Heatmap](/controls/data-display/charts/maps/heatmap-map-chart) | 在地图上叠加颜色渐变，呈现强度或密度。 |
| [形状地图](/controls/data-display/charts/maps/shape-map-chart) | 把自定义区域渲染成数据驱动的地图。 |
| [座位图](/controls/data-display/charts/maps/seat-map-chart) | 呈现场馆或平面布局，并支持交互式选座。 |

### 径向类 {#radial-charts}

采用环形坐标系而非笛卡尔坐标轴的图表。

| 图表 | 说明 |
| --- | --- |
| [极坐标图](/controls/data-display/charts/radial/polar-chart) | 在极坐标系中绘制任意角度和半径的数值。 |
| [雷达图](/controls/data-display/charts/radial/radar-chart) | 在环形轴网上把多变量数据画成一个多边形。 |
| [极坐标面积图](/controls/data-display/charts/radial/polar-area-chart) | 把圆划分成等角度的扇段，各段大小由数值决定。 |
| [南丁格尔玫瑰图](/controls/data-display/charts/radial/nightingale-rose-chart) | 一种极坐标面积图，用半径而非面积表示数值。 |
| [径向条形图](/controls/data-display/charts/radial/radial-bar-chart) | 围绕中心点，把各类别画成长短不一的弧。 |
| [径向折线图](/controls/data-display/charts/radial/radial-line-chart) | 投影到环形坐标轴上的折线图。 |

### 排期与时间线类 {#scheduling-and-timeline-charts}

用于时间规划、项目管理和顺序数据的图表。

| 图表 | 说明 |
| --- | --- |
| [甘特图](/controls/data-display/charts/scheduling/gantt-chart) | 在横向时间轴上呈现各项任务及其工期。 |
| [时间线图](/controls/data-display/charts/scheduling/timeline-chart) | 沿线性轴按时间先后呈现各个事件。 |
| [泳道图](/controls/data-display/charts/scheduling/swimlane-chart) | 把任务编入并列的行，体现责任归属或所处阶段。 |
| [螺旋时间线图](/controls/data-display/charts/scheduling/spiral-timeline-chart) | 沿螺旋线排布时间数据，呈现周期性规律。 |
| [迷你走势图](/controls/data-display/charts/scheduling/sparkline-chart) | 行内的微型图表，在极小的空间里呈现走势。 |

### 统计类 {#statistical-charts}

用于分布分析和统计对比的图表。

| 图表 | 说明 |
| --- | --- |
| [蜂群图](/controls/data-display/charts/statistical/beeswarm-plot-chart) | 在每个类别内把各个观测值画成互不重叠的点。 |
| [箱线图](/controls/data-display/charts/statistical/boxplot-chart) | 用中位数、四分位数和异常值概括一组分布。 |
| [等值线图](/controls/data-display/charts/statistical/contour-plot-chart) | 用等值线和可选的填充带呈现二维标量场。 |
| [密度图](/controls/data-display/charts/statistical/density-plot-chart) | 用核密度估计绘出平滑的分布曲线。 |
| [误差棒图](/controls/data-display/charts/statistical/error-bar-chart) | 为数据点添加误差或不确定性指示。 |
| [马赛克图](/controls/data-display/charts/statistical/mosaic-chart) | 用嵌套矩形呈现两个分类变量上的占比。 |
| [平行坐标图](/controls/data-display/charts/statistical/parallel-coordinates-chart) | 在一组平行轴上以折线比较多变量记录。 |
| [山脊图](/controls/data-display/charts/statistical/ridgeline-chart) | 把多条相互重叠的分布叠放在一起，便于比较形态。 |
| [带状散点图](/controls/data-display/charts/statistical/strip-plot-chart) | 按类别呈现各个观测值，带抖动偏移和可选的均值线。 |
| [小提琴图](/controls/data-display/charts/statistical/violin-plot-chart) | 把箱线图与核密度形状结合起来呈现分布。 |

## 共用元素 {#shared-elements}

大多数图表类型都共用下列可配置的元素：

| 元素 | 说明 |
| --- | --- |
| [Legend](/controls/data-display/charts/shared-elements/legend-chart) | 按名称和颜色标识各个数据系列。 |
| [Tooltip](/controls/data-display/charts/shared-elements/tooltip-chart) | 在悬停或点按时显示数据值。 |
| [Crosshairs](/controls/data-display/charts/shared-elements/crosshairs-chart) | 绘制随指针移动、相互交叉的十字准线。 |
| [数据标签](/controls/data-display/charts/shared-elements/data-labels-chart) | 把每个数据点的数值直接标在图上。 |
| [图表导出](/controls/data-display/charts/shared-elements/export-chart) | 把图表视图保存为 PNG 或 JPEG 文件、PNG 流，或通过保存对话框导出。 |
| [Markers](/controls/data-display/charts/shared-elements/markers-chart) | 在每个数据值处添加标记符号。 |
| [Trendline](/controls/data-display/charts/shared-elements/trendline-chart) | 在系列上叠加一条回归线或移动平均线。 |
| [Annotations](/controls/data-display/charts/shared-elements/annotations-chart) | 在指定的数据坐标处放置标签、线条或图形。 |
| [坐标轴定制](/controls/data-display/charts/shared-elements/axis-customization-chart) | 控制刻度线、标签、网格线和刻度范围。 |
| [Interactions](/controls/data-display/charts/shared-elements/interactions-chart) | 配置缩放、平移、选择、悬停高亮和轨迹球行为。 |

## 另请参阅 {#see-also}

- [Avalonia Pro 定价与获取方式](https://avaloniaui.net/pricing)
