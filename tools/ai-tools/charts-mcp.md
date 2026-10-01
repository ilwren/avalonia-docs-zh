---
id: charts-mcp
title: Charts MCP
sidebar_label: Charts MCP
doc-type: how-to
description: "配置 Charts MCP 服务器，让 AI 助手能生成 Avalonia 图表预览和代码。"
keywords:
  - mcp
  - model context protocol
  - ai assistant
  - charts
  - avalonia charts
  - copilot
  - claude
  - cursor
  - windsurf
  - gemini
  - ai tools
tags:
  - mcp
  - ai
  - avalonia charts
  - avalonia pro
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Charts 模型上下文协议（MCP）服务器让 AI 助手能依据自然语言请求创建并渲染 Avalonia Charts。助手可以挑选图表类型、提供 JSON 数据、调整尺寸、主题、标签、调色板等常用选项，然后拿到渲染好的 PNG 预览图以及 C# 和 XAML 代码片段。

Charts MCP 以本地 stdio MCP 服务器的形式运行。它从 `Avalonia.Controls.Charts` 创建控件，并经由 Avalonia Headless 和 Skia 渲染。生成图表、试验图表样式和搭代码骨架都可以用它。

:::note
Charts MCP 不会挂到正在运行的 Avalonia 应用上，也不会检视视觉树。若要实时检视运行中的应用，请用 [DevTools MCP](/tools/developer-tools/mcp)。
:::

关于 MCP 的总体介绍，请见 [AI 工具](/tools/ai-tools/)。

## 前置条件 {#prerequisites}

配置 MCP 服务器前，请先确认你具备：

- **已安装 .NET SDK。**该服务器是以 .NET 工具的形式分发的。
- **含 Charts 的有效 Avalonia Pro 许可证。**Charts 包含在 [Avalonia Pro](https://avaloniaui.net/pricing) 中，Community、Plus 以及旧的 Accelerate 订阅不含此项。
- **一个含有 Charts MCP 包的 NuGet 源。**只有当 `Avalonia.Controls.Charts.Mcp` 及其配套的运行时包（如 `Avalonia.Controls.Charts.Mcp.osx-arm64`）能从你配置的某个 NuGet 源取到时，`dotnet tool install` 命令才跑得通。
- **一个支持 MCP 的编辑器或助手。**VS Code、Visual Studio、Rider、Cursor、Windsurf、Claude Code、Claude Desktop 和 Gemini CLI 都可以配置 MCP 服务器。

## 安装服务器 {#install-the-server}

1. 配置一个含有 `Avalonia.Controls.Charts.Mcp` 及其配套运行时包的 NuGet 包源。
2. 运行 `dotnet tool install`，把 Charts MCP 服务器安装为全局 .NET 工具。

```bash
dotnet tool install --global Avalonia.Controls.Charts.Mcp
```

3. 若 `dotnet` 报告找不到该包，请确认所需的包源已配置并已启用。可运行下面这条命令查看你的 NuGet 源。

```bash
dotnet nuget list source
```

4. 运行下面的命令即可访问 Charts MCP 服务器。多数编辑器配置好之后会自动这么做。

```bash
mcp-server-charts
```

:::tip
若安装完后命令行仍找不到 `mcp-server-charts`，请检查 .NET 全局工具目录是否在你的 `PATH` 里。在 macOS 和 Linux 上通常是 `~/.dotnet/tools`，在 Windows 上通常是 `%USERPROFILE%\.dotnet\tools`。
:::

渲染图表要求 MCP 服务器进程中有含 Charts 的有效 Avalonia Pro 许可证。请在环境中设置 `AVALONIA_LICENSE_KEY`；若编辑器不会继承 shell 变量，则在 MCP 客户端配置里加上 `"env": { "AVALONIA_LICENSE_KEY": "your-license-key" }`。切勿把密钥提交进仓库。

## 从源码运行 {#run-from-source}

如果你用的是源码检出而非已安装的工具：

1. 构建 MCP 项目。

```bash
dotnet build /absolute/path/to/Avalonia.Controls.Charts/src/Avalonia.Controls.Charts.Mcp/Avalonia.Controls.Charts.Mcp.csproj
```

2. 把 MCP 客户端配置成运行：

```bash
dotnet run --project /absolute/path/to/Avalonia.Controls.Charts/src/Avalonia.Controls.Charts.Mcp/Avalonia.Controls.Charts.Mcp.csproj
```

:::note
从源码运行主要是给贡献者和本地验证用的。生成图表需要有效的 Avalonia Pro（或更高）许可证。若渲染图表时报出图表初始化或许可证相关的错误，请核对你这份构建或包的 Charts 许可证配置。
:::

## 在编辑器中配置 MCP 服务器 {#set-up-the-mcp-server-in-your-editor}

下面的示例用的是全局 .NET 工具命令。如果你是[从源码运行](#run-from-source)，请把 `"command": "mcp-server-charts"` 换成：

```json
"command": "dotnet",
"args": [
    "run",
    "--project",
    "/absolute/path/to/Avalonia.Controls.Charts/src/Avalonia.Controls.Charts.Mcp/Avalonia.Controls.Charts.Mcp.csproj"
]
```

<Tabs groupId="editor">
<TabItem value="vscode" label="VS Code">

#### 方式 A：命令面板 {#option-a-command-palette}

1. 打开命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`）。
2. Run **MCP: Add Server**.
3. 服务器类型选 **stdio**。
4. 命令填 `mcp-server-charts`。
5. 服务器名称设为 `avalonia_charts`。
6. 选择把该服务器装到当前工作区还是全局。

#### 方式 B：手动配置 {#option-b-manual-configuration}

把下列内容加进工作区根目录的 `.vscode/mcp.json`：

```json title=".vscode/mcp.json"
{
    "servers": {
        "avalonia_charts": {
            "type": "stdio",
            "command": "mcp-server-charts"
        }
    }
}
```

</TabItem>
<TabItem value="visual-studio" label="Visual Studio">

Visual Studio 2022（17.x 及更高版本）通过 `mcp.json` 配置文件支持 MCP 服务器。

在解决方案目录中新建或编辑 `.mcp.json`：

```json title=".mcp.json"
{
    "servers": {
        "avalonia_charts": {
            "type": "stdio",
            "command": "mcp-server-charts"
        }
    }
}
```

:::tip
Visual Studio 同样会读取 `.vscode/mcp.json`。若你已在同一解决方案中为 VS Code 配置过 Charts MCP，Visual Studio 可以自动发现该配置。
:::

</TabItem>
<TabItem value="rider" label="Rider">

JetBrains Rider 可通过 AI Assistant 插件支持 MCP 服务器。

1. 打开 **Settings** → **Tools** → **AI Assistant** → **Model Context Protocol (MCP)**。
2. Click **Add**.
3. Select **STDIO**.
4. 粘贴下面这段 JSON 配置：

```json
{
    "mcpServers": {
        "avalonia_charts": {
            "command": "mcp-server-charts"
        }
    }
}
```

5. 点击 **OK**，再点 **Apply**。

</TabItem>
<TabItem value="cursor" label="Cursor">

把下列内容加进项目目录下的 `.cursor/mcp.json`，若要全局配置则加进 `~/.cursor/mcp.json`：

```json title=".cursor/mcp.json"
{
    "mcpServers": {
        "avalonia_charts": {
            "command": "mcp-server-charts"
        }
    }
}
```

</TabItem>
<TabItem value="windsurf" label="Windsurf">

把下列内容加进 `~/.codeium/windsurf/mcp_config.json`：

```json title="~/.codeium/windsurf/mcp_config.json"
{
    "mcpServers": {
        "avalonia_charts": {
            "command": "mcp-server-charts"
        }
    }
}
```

</TabItem>
<TabItem value="claude-code" label="Claude Code">

在终端里运行这条命令：

```bash
claude mcp add --transport stdio --scope user avalonia_charts -- mcp-server-charts
```

验证是否添加成功：

```bash
claude mcp list
```

</TabItem>
<TabItem value="claude-desktop" label="Claude Desktop">

1. 打开 **Settings** → **Developer**，点击 **Edit Config**。
2. 把 Charts MCP 服务器加进 `claude_desktop_config.json`：

```json
{
    "mcpServers": {
        "avalonia_charts": {
            "command": "mcp-server-charts"
        }
    }
}
```

3. 保存文件。
4. Restart Claude Desktop.

:::note
Claude Desktop 不会从你的 shell 配置里继承环境变量。若服务器需要环境变量，请在这份配置中加上 `env` 块。
:::

</TabItem>
<TabItem value="gemini-cli" label="Gemini CLI">

把下列内容加进 `~/.gemini/settings.json` 或项目级的 `.gemini/settings.json`：

```json title="~/.gemini/settings.json"
{
    "mcpServers": {
        "avalonia_charts": {
            "command": "mcp-server-charts"
        }
    }
}
```

</TabItem>
</Tabs>

## 验证连接 {#verify-the-connection}

配置好 MCP 服务器后，按下面的步骤确认它确实在工作：

1. **确认服务器正在运行。**打开编辑器的 MCP 面板或状态指示器（在 VS Code 中即命令面板里的 **MCP: List Servers**），确认 `avalonia_charts` 以已连接服务器的身份出现。
2. **用一句提示词试一下。**问问你的 AI 助手：

```text
List the available Avalonia chart tools and show me the data format for a bar chart.
```

你也可以这样测试图表渲染：

```text
Create a dark themed Avalonia bar chart titled Quarterly Revenue with Q1=125, Q2=148, Q3=171, and Q4=193. Use a blue and green palette.
```

## 用法示例 {#usage-examples}

用自然语言描述你想要的图表，AI 助手会自动调用相应的 MCP 工具。

### 生成图表预览 {#generating-a-chart-preview}

```text
Create a line chart comparing monthly signups from January through June. Use the default light theme and include the generated Avalonia code.
```

### 挑选图表类型 {#choosing-a-chart-type}

```text
Read the Avalonia Charts catalog resource and recommend a chart for showing stage-by-stage sales conversions.
```

### 指定使用某个工具 {#using-a-specific-tool}

```text
Use avalonia_sankey_chart to show product flow from Acquisition to Activation to Retention. Render it at 900x520.
```

### 生成应用代码 {#creating-app-code}

```text
Create an Avalonia combo chart with a bar series for revenue and a line series for margin. Return the generated C# and XAML so I can adapt it to MVVM.
```

### 调试数据格式 {#debugging-data-formats}

```text
Show me the required data format for avalonia_calendar_heatmap, then render a small example.
```

## 可用的工具 {#available-tools}

Charts MCP 服务器开放了 86 个图表生成工具和一个目录工具。

### Catalog

| 工具 | 说明 |
|------|-------------|
| `avalonia_list_charts` | 列出所有可用图表，附带说明和示例数据格式。 |

### Cartesian

| 工具 | 说明 |
|------|-------------|
| `avalonia_line_chart` | 趋势与时间序列数据。 |
| `avalonia_area_chart` | 带填充区域的定量数据。 |
| `avalonia_bar_chart` | 比较各类别之间的数值。 |
| `avalonia_scatter_chart` | 两个变量之间的关系。 |
| `avalonia_combo_chart` | 组合系列，比如柱状与折线同台呈现。 |

### Circular

| 工具 | 说明 |
|------|-------------|
| `avalonia_pie_chart` | 各部分占整体的比例。 |
| `avalonia_donut_chart` | 中间带空心的占比图。 |
| `avalonia_progress_donut` | 单值环形进度。 |
| `avalonia_semi_donut` | 半圆形占比。 |
| `avalonia_nightingale_rose` | 极区图，也叫南丁格尔玫瑰图。 |
| `avalonia_radial_bar_chart` | 沿圆周排布的柱条。 |
| `avalonia_sunburst_chart` | 层级化的占比。 |

### Gauge

| 工具 | 说明 |
|------|-------------|
| `avalonia_gauge_chart` | 标准的表盘式仪表。 |
| `avalonia_bullet_chart` | 将表现与目标值、区间作对照。 |
| `avalonia_circular_gauge` | 圆形指针式指示器。 |
| `avalonia_linear_gauge` | 水平或垂直的刻度指示器。 |
| `avalonia_gradient_ring_chart` | 以彩色圆环呈现进度或数值。 |
| `avalonia_liquid_fill_gauge` | 以液面高度呈现数值。 |

### Polar

| 工具 | 说明 |
|------|-------------|
| `avalonia_radar_chart` | 多变量对比。 |
| `avalonia_polar_chart` | 角度与径向的折线数据。 |
| `avalonia_wind_rose_chart` | 方向性频次分布。 |
| `avalonia_smith_chart` | 复阻抗与工程数据。 |
| `avalonia_polar_area_chart` | 等角度、变半径的扇形。 |

### Statistical

| 工具 | 说明 |
|------|-------------|
| `avalonia_violin_plot` | 分布密度与取值范围。 |
| `avalonia_boxplot_chart` | 四分位数、中位数与离群值。 |
| `avalonia_ridgeline_chart` | 多组分布的对比。 |
| `avalonia_beeswarm_plot` | 逐点呈现的分布。 |
| `avalonia_contour_plot` | 二维密度等值线。 |
| `avalonia_density_plot` | 核密度估计。 |
| `avalonia_strip_plot` | 沿单一分类轴分布的点。 |

### 对比与排名 {#comparison-and-ranking}

| 工具 | 说明 |
|------|-------------|
| `avalonia_tornado_chart` | 按类别成对对比。 |
| `avalonia_bump_chart` | 名次随时间的变化。 |
| `avalonia_slope_chart` | 前后状态的变化。 |
| `avalonia_dumbbell_chart` | 区间或差距的对比。 |
| `avalonia_pareto_chart` | 频次加累计百分比。 |
| `avalonia_mirror_bar_chart` | 背靠背的水平柱条。 |
| `avalonia_diverging_bar_chart` | 正负两向对置的数值。 |
| `avalonia_pyramid_chart` | 层级化拆解。 |
| `avalonia_population_pyramid` | 年龄与人口结构。 |
| `avalonia_funnel_chart` | 依次推进的流程阶段。 |

### 流向与网络 {#flow-and-network}

| 工具 | 说明 |
|------|-------------|
| `avalonia_sankey_chart` | 多个类别之间的流量。 |
| `avalonia_arc_diagram` | 有序节点之间的连线。 |
| `avalonia_chord_diagram` | 环形排布的相互关系。 |
| `avalonia_alluvial_chart` | 结构随步骤或时间的变化。 |
| `avalonia_flow_chart` | 通用的流程图。 |
| `avalonia_network_chart` | 节点与连线的关系。 |
| `avalonia_force_directed_graph` | 基于力学模拟的节点图布局。 |
| `avalonia_organization_chart` | 传统的层级树。 |

### 占比与层级 {#proportional-and-hierarchical}

| 工具 | 说明 |
|------|-------------|
| `avalonia_treemap_chart` | 用嵌套矩形表现层级。 |
| `avalonia_icicle_chart` | 邻接图式的层级。 |
| `avalonia_circle_packing_chart` | 层级以嵌套圆形紧凑排布。 |
| `avalonia_dendrogram_chart` | 层次聚类树。 |
| `avalonia_flame_graph` | 堆叠式或剖面式的层级可视化。 |
| `avalonia_indented_tree_chart` | 带缩进的层级树。 |
| `avalonia_radial_tree_chart` | 呈放射状排布的层级。 |
| `avalonia_waffle_chart` | 用于百分比的网格图。 |
| `avalonia_mekko_chart` | 宽度可变的堆叠柱状图。 |
| `avalonia_parliament_chart` | 半圆形的议席分布图。 |
| `avalonia_venn_chart` | 集合之间的关系与交集。 |

### 网格与矩阵 {#grid-and-matrix}

| 工具 | 说明 |
|------|-------------|
| `avalonia_heatmap_chart` | 用颜色网格表现数值强弱。 |
| `avalonia_matrix_chart` | 相关性或关系矩阵。 |
| `avalonia_carpet_plot` | 两个自变量对一个因变量。 |
| `avalonia_hexbin_chart` | X/Y 点的六边形分箱密度。 |
| `avalonia_mosaic_chart` | 按比例呈现分组与子分组。 |
| `avalonia_parallel_coordinates_chart` | 多维记录在若干平行轴上的呈现。 |
| `avalonia_ternary_chart` | 三元组成图。 |
| `avalonia_calendar_heatmap` | 按日期分布的活动热力图。 |

### 时间与排期 {#time-and-scheduling}

| 工具 | 说明 |
|------|-------------|
| `avalonia_gantt_chart` | 项目管理与任务排期。 |
| `avalonia_swimlane_chart` | 按泳道分组的工作流任务。 |
| `avalonia_event_timeline` | 按时间先后排列的事件。 |
| `avalonia_spiral_timeline` | 以螺旋形式表现时间。 |

### Financial

| 工具 | 说明 |
|------|-------------|
| `avalonia_candlestick_chart` | 金融价格走势。 |
| `avalonia_ohlc_chart` | 开高低收（OHLC）柱线。 |
| `avalonia_heikin_ashi_chart` | 经过平滑的 OHLC 趋势蜡烛图。 |
| `avalonia_kagi_chart` | 价格反转走势图。 |
| `avalonia_renko_chart` | 固定幅度的价格砖形图。 |
| `avalonia_point_and_figure_chart` | 以 X/O 柱列表现价格走势。 |

### Map

| 工具 | 说明 |
|------|-------------|
| `avalonia_choropleth_map` | 按数值为各地理区域着色。 |
| `avalonia_shape_map` | 自定义的多图层几何形状。 |

### 仪表板、数据、文本与气泡 {#dashboard-data-text-and-bubble}

| 工具 | 说明 |
|------|-------------|
| `avalonia_sparkline_chart` | 紧凑的迷你趋势线。 |
| `avalonia_kpi_card` | 带状态或变化量的指标展示。 |
| `avalonia_table_chart` | 带条件格式的表格数据。 |
| `avalonia_word_cloud` | 词频云图。 |
| `avalonia_bubble_chart` | 用 X、Y 和大小三个值绘制的气泡图。 |
| `avalonia_packed_bubble_chart` | 非层级的气泡紧凑排布。 |
| `avalonia_bubble_cloud` | 力导向的气泡云布局。 |

## 可用的资源 {#available-resources}

该服务器还开放了一些 MCP 资源，助手可以在调用图表工具之前读取它们，以便挑选图表类型、核对输入结构或选定配色。

| Resource URI | 说明 |
|--------------|-------------|
| `charts://catalog` | 按类别分组的完整图表目录。 |
| `charts://palettes` | 默认与推荐的调色板取值。 |
| `charts://data-formats` | 数据格式参考，取自目录中的示例。 |

## 输入与输出 {#inputs-and-outputs}

多数图表工具接受标题、一个 JSON 格式的 `data` 字符串、可选的宽高值以及可选的主题。部分工具还有图表专属参数，比如 `geoJson`、`nodes` 或 `innerRadius`。

JSON 属性名不区分大小写。例如 `Label`、`label` 和 `LABEL` 都映射到同一个属性。

```json
[
    { "Label": "Q1", "Value": 125 },
    { "Label": "Q2", "Value": 148 },
    { "Label": "Q3", "Value": 171 },
    { "Label": "Q4", "Value": 193 }
]
```

调色板以逗号分隔的颜色代码形式传入：

```text
#2196F3, #4CAF50, #FF9800
```

`theme` 接受 `Light` 或 `Dark`。图表生成成功时，响应中会包含渲染好的 `image/png` 预览图、生成的 C# 代码，以及（在支持的情况下）生成的 XAML。

## 隐私与安全 {#privacy-and-security}

Charts MCP 在本地运行。图表数据在 MCP 服务器进程中解析和渲染，服务器不会调用外部 LLM 提供方，也不会读取提供方的 API 密钥。

MCP 客户端收到的是渲染好的图表图片和生成的代码。生成的代码片段可能含有图表请求中的标签、数值、颜色等字段。

除非所连接的 MCP 客户端已获准接收这类数据，否则切勿把机密、凭据或敏感个人信息写进 JSON、标题、标签或说明中。

## 排查问题 {#troubleshooting}

### 找不到 `mcp-server-charts` 命令 {#mcp-server-charts-command-not-found}

`mcp-server-charts` 命令必须在系统的 `PATH` 中。若你是作为全局 .NET 工具安装的，请确认编辑器能访问到 `PATH`——在 macOS 和 Linux 上通常是 `~/.dotnet/tools`，在 Windows 上通常是 `%USERPROFILE%\.dotnet\tools`。

可运行下面的命令确认工具已安装：

```bash
dotnet tool list -g
```

### 编辑器里看不到 MCP 服务器 {#mcp-server-does-not-appear-in-the-editor}

- **重启你的编辑器。**添加或修改 MCP 配置文件后，多数编辑器都要重启才能发现新的 MCP 服务器。
- **核对配置文件的位置。**每种编辑器都有各自约定的配置路径，请见[你所用编辑器的配置说明](#set-up-the-mcp-server-in-your-editor)。
- **检查 JSON 是否合法。**配置文件里的语法错误会让服务器加载不起来。
- **改用绝对命令路径。**这往往能帮编辑器顺利找到 `mcp-server-charts`。

### 服务器起来了，但渲染图表失败 {#server-starts-but-chart-rendering-fails}

- **确认 Avalonia Pro Charts 许可证。**渲染图表要求服务器所在环境有有效的许可证密钥。你可以在 [Avalonia 门户](https://portal.avaloniaui.net/)查看自己的订阅和许可证密钥。
- **查看服务器日志。**日志写在 MCP 服务器输出目录下的 `logs/AvaloniaChartsMcpServer_*.log` 中，往往能看出是启动失败还是渲染失败。
- **先试一个简单的图表。**跑一次简单的 `avalonia_bar_chart` 调用，就能把配置问题和数据格式问题区分开。
- **临时调高日志级别。**可以把 `AVALONIA_CHARTS_MCP_LOG_LEVEL` 调到更详细的级别，排查完再调回去或移除。

### 格式错误 {#format-error}

- 检查调色板和颜色取值。用 `#2196F3` 这样的十六进制颜色最稳妥。
- 逗号分隔的调色板字符串中不要留空项。

## 另请参阅 {#see-also}

- [AI 工具概述](/tools/ai-tools/)
- [Avalonia Charts](/controls/data-display/charts/)
- [DevTools MCP](/tools/developer-tools/mcp)
- [Build MCP](/tools/ai-tools/build-mcp)
- [Parcel MCP](/tools/parcel/mcp)
