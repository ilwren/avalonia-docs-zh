---
id: elements-tool
title: 元素工具
doc-type: reference
---

元素树把视觉层级和逻辑层级合在一处呈现。为了性能考虑，它只加载可见的元素，并以逻辑树为骨架来组织结构。模板内容则折叠收进 `/template/` 节点里。

![元素工具](/img/tools/dev-tools/elements-tool.png)

## 检视模式 {#inspect-mode}

元素工具提供了几种方式，可直接从运行中的应用里认出并选中特定的 UI 元素：

- **焦点跟踪**——启用后，应用中当前获得焦点的元素会自动在元素树里被选中。用 <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>K</kbd>（macOS 上是 <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>K</kbd>）切换该模式，你与应用交互时焦点变化便会被自动跟踪。

- **检视元素**——该模式把光标变成元素选取器。用 <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd>（macOS 上是 <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>C</kbd>）激活后，在应用里点击任意元素，元素树中便会立刻定位并选中它。这样一来，你眼前看到的界面与其底层结构之间就有了一座直通桥。

有了这两种检视模式，你不必在元素层级里一层层翻找就能定位到目标。

## 上下文菜单 {#context-menu}

右键菜单提供了浏览和操作元素树的常用动作：

右键点击某个元素，可以用到各种展开选项，按不同的详尽程度探查层级。“Expand Children” 展开直接子级，“Recursively” 和 “Recursively with templates” 则可以挖得更深。

此外还能折叠节点、复制元素或其选择器、让元素获得焦点、把元素滚动到可见范围内，以及使视觉失效重绘。对 Window 元素还有一项特别能力：渲染 `FPS` 这类调试叠加层。

整棵树都支持搜索，你可以按名称或类型迅速找到特定元素。

![元素树右键菜单](/img/tools/dev-tools/elements-context-menu.png)

## 伪类选择器 {#pseudoclasses-selector}

工具会为每个元素显示其上定义的伪类。想测试元素在不同状态下的表现时，这一点尤其有用——不必靠手动交互去一个个触发状态。

开发带伪类的自定义控件时，加上 `[PseudoClassesAttribute]` 能让它与开发者工具配合得更好，IDE 的自动补全也更给力。

## 元素属性 {#element-properties}

属性面板显示元素树中所选元素的详细信息，列出影响该元素的所有属性、样式和取值。

![属性列表](/img/tools/dev-tools/properties-list.png)

面板会列出赋给该元素的所有 Avalonia 属性。开发者可以：
- 按名称筛选属性
- 按字母顺序或按取值排序
- 按类别对属性分组
- 用专门的编辑器修改取值（ColorPicker、BrushPicker、Image/Geometry 预览）
- 带嵌套网格的属性可以点开，用来预览 `DataContext` 或 `Image.Source` 之类的属性。

### 属性详情 {#property-details}

选中某个属性后，还可以通过两个专门的选项卡查看更多详情。

#### 样式与取值 {#styles-and-values}

Avalonia 的属性遵循一套基于优先级的机制，同一个属性可以被赋予多个值。属性面板把这种层层叠加的结构摊开给你看：

![样式 setter](/img/tools/dev-tools/properties-style-setters.png)

每个属性可以有多个 setter，各自带着不同的优先级和条件。比如一个按钮，常态、悬停和按下三种状态下的背景色可能各不相同。DevTools 会把这些 setter 悉数列出，当前生效的那个默认展开。

未生效的 setter（条件当前不成立的那些）呈折叠且灰显状态。这种视觉上的层次让开发者一眼看清当前套用的是哪条样式、为什么是它，排查样式问题也就容易多了。

#### 绑定表达式 {#binding-expressions}

“Binding Expressions” 选项卡揭示属性是如何与数据源挂上钩的：

![绑定表达式](/img/tools/dev-tools/properties-bindings.png)

当属性用了数据绑定时，这个选项卡会显示绑定关系的关键信息：
- 绑定的 Source 和 Path
- 绑定失败时的校验错误
- Mode、Converter、FallbackValue 等其他绑定参数

对于存在校验错误的属性，面板会显示异常类型和消息，连带内部异常也一并列出，为调试提供更多线索。

有些属性用的是 MultiBinding 表达式，把多个来源合在一起：

![MultiBinding 表达式](/img/tools/dev-tools/properties-multi-bindings.png)

## 元素 3D 查看器 {#element-3d-viewer}

3D 查看器把应用的视觉树以三维形式呈现出来，让你在空间视角下探查 UI 元素的层叠与层级关系。

![3D 查看器选项卡](/img/tools/dev-tools/3d-viewer-mini-demo.gif)

### 打开 3D 查看器 {#accessing-the-3d-viewer}

在开发者工具面板中，点击属性视图工具栏上的 “3D Viewer” 按钮即可打开；
也可以在元素树的右键菜单中选 “Open 3D Viewer”。

任何视觉元素子树都可以查看，模板和根 Application 除外。

:::note

此功能需要 Avalonia 11.2.0 或更高版本。

:::

### 功能一览 {#features}

3D 查看器把视觉树的每一层渲染成三维空间中的一个平面。

元素按其 Z-index 和渲染顺序摆放，哪些元素相互重叠、各自处于怎样的层叠上下文，一目了然

#### Navigation Controls

在三维空间里挪动视角，从不同角度审视你的界面：

- **旋转**：按住并拖动即可旋转视图
- **平移**：按住右键拖动可移动相机位置
- **缩放**：用鼠标滚轮放大或缩小
- **重置**：双击把视图恢复到默认位置

#### Visualization Settings

自定义 3D 视图呈现元素的方式：

- **Draw as Gradient**：开启后用渐变着色呈现元素，深度感更强
- **Draw Borders**：启用或禁用元素边框的渲染，画面可以更清爽
- **Layer Distance**：调整视觉树各层之间的间距
- **Layer Range**：设定层索引的上下限，专注于视觉树中某一段深度范围

### 3D Viewer Use Cases

- **调试 Z-Index 问题**：找出并解决元素层叠顺序上的毛病
- **看懂复杂布局**：把嵌套的面板与控件之间的关系可视化
- **精简视觉树**：发现多余的嵌套或冗余的容器
- **讲解 UI 架构**：作为教学工具演示视觉树的概念

## 应用内叠加层 {#in-app-overlay}

Avalonia 开发者工具能把视觉叠加层直接画在运行中的应用上，让你不改代码就能直观查看、调试 UI 组件。

### 启用叠加层 {#enabling-overlays}

有两种方式可以启用叠加层：

#### 1. Via Elements Tree

在开发者工具的元素树中把鼠标悬停到某个元素上，叠加层会自动出现。

![从元素树触发叠加层](/img/tools/dev-tools/overlay-tree-inspect.png)

#### 2. 通过 “Highlight Elements” 模式的快捷键 {#2-via-highlight-elements-mode-shortcut}

直接在你的应用中进入检视模式：
- 按 <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>H</kbd>（Windows/Linux）或 <kbd>⌘</kbd> <kbd>⇧</kbd> <kbd>H</kbd>（macOS）
- 把鼠标悬停到任意元素上即可看到它的叠加层
- 需要时再按一次同样的快捷键即可关闭该模式

![用快捷键检视应用内叠加层](/img/tools/dev-tools/overlay-shortcut-inspect.png)

### 可用的叠加层 {#available-overlays}

#### 信息提示框 {#info-tooltip}

悬停时显示元素的详细信息：

- **基本信息**：元素类型、名称和样式类
- **布局属性**：尺寸、外边距、内边距、约束和 Z-Index
- **视觉属性**：边框与背景细节、颜色和不透明度
- **文本属性**：前景色、字体设置
- **控件专属属性**：选区画刷、图像细节

![信息提示框](/img/tools/dev-tools/overlay-info-tooltip.png)

#### 布局叠加层 {#layout-overlay}

用不同颜色的高亮呈现 UI 结构：

- **Margin**：以半透明高亮标出外边距所占空间
- **Padding**：以半透明高亮标出内边距
- **Bounds**：沿控件实际边界画出实线边框

![外边距/内边距布局叠加层](/img/tools/dev-tools/overlay-margin-padding.png)

#### 标尺叠加层 {#ruler-overlay}

提供度量参照：

- 沿窗口边缘的水平和垂直标尺
- 把内容边界连到标尺上的参考线

![Ruler](/img/tools/dev-tools/overlay-ruler.png)

## 另请参阅 {#see-also}

- [事件工具](/tools/developer-tools/events-tool)
- [开发者工具快捷键](/tools/developer-tools/shortcuts)
