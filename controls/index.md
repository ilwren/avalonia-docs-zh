---
id: index
title: 控件
sidebar_label: 首页
hide_table_of_contents: true
---

import DocsCard from '@site/src/components/global/DocsCard';
import DocsCards from '@site/src/components/global/DocsCards';
import Pill from '@site/src/components/global/Pill';

<head>
  <title>Avalonia 文档：控件库</title>
  <meta
    name="description"
    content="Avalonia comes with lots of high-quality UI controls, including buttons, lists, tabs and more, to quickly and easily build your app's user interface."
  />
  <style>{`
    :root {
      --doc-item-container-width: 60rem;
    }
  `}</style>
</head>

Avalonia 应用由一个个称为「控件」的高层积木搭成，你可以用它们快速搭建界面。Avalonia 自带大量控件，涵盖按钮、列表、选项卡等等。本章讲解 Avalonia 控件的核心用法；详细信息请查阅 [API 参考](/api)。


<DocsCards>
<DocsCard header="Border" href="/controls/layout/containers/border" icon="/icons/border-icon@2x.png" darkIcon="/icons/border-icon-dark@2x.png">
  <p>一个装饰器，在子内容四周绘制边框和背景。</p>
</DocsCard>

<DocsCard header="Button" href="/controls/input/buttons/button" icon="/icons/button-icon@2x.png" darkIcon="/icons/button-icon-dark@2x.png">
  <p>按钮让用户发起操作，是与应用交互、在应用中穿行的基本手段。</p>
</DocsCard>

<DocsCard header="Calendar" href="/controls/input/date-and-time/calendar" icon="/icons/calendar-icon@2x.png" darkIcon="/icons/calendar-icon-dark@2x.png">
  <p>一个完整的日历视图，让用户直观地浏览和选择日期。</p>
</DocsCard>

<DocsCard header="Charts" href="/controls/data-display/charts" icon="/icons/charts-icon@2x.png" darkIcon="/icons/charts-icon-dark@2x.png">
  <p>数据可视化控件，可用于搭建仪表板、金融工具、科研报告等。</p>
  <Pill>Avalonia Pro</Pill>
</DocsCard>

<DocsCard header="Checkbox" href="/controls/input/selectors/checkbox" icon="/icons/checkbox-icon@2x.png" darkIcon="/icons/checkbox-icon-dark@2x.png">
  <p>复选框适合二选一的决定，比如功能开关、问卷选项或任务清单。</p>
</DocsCard>

<DocsCard header="ComboBox" href="/controls/input/selectors/combobox" icon="/icons/combobox-icon@2x.png" darkIcon="/icons/combobox-icon-dark@2x.png">
  <p>ComboBox 显示当前选中项，点击后展开可选项列表。</p>
</DocsCard>

<DocsCard header="DatePicker" href="/controls/input/date-and-time/datepicker" icon="/icons/datepicker-icon@2x.png" darkIcon="/icons/datepicker-icon-dark@2x.png">
  <p>日期选择器以紧凑的界面让用户挑选日期。</p>
</DocsCard>

<DocsCard header="Grid" href="/controls/layout/panels/grid" icon="/icons/grid-icon@2x.png" darkIcon="/icons/grid-icon-dark@2x.png">
  <p>Grid 是一个强大的布局控件，把其他控件按行列排布。</p>
</DocsCard>

<DocsCard header="Image" href="/controls/media/image" icon="/icons/image-icon@2x.png" darkIcon="/icons/image-icon-dark@2x.png">
  <p>显示图片，并决定它们如何与其他界面元素相互影响。</p>
</DocsCard>

<DocsCard header="Label" href="/controls/data-display/text-display/label" icon="/icons/label-icon@2x.png" darkIcon="/icons/label-icon-dark@2x.png">
  <p>一个文本标签，可为其目标控件提供访问键支持。</p>
</DocsCard>

<DocsCard header="ListBox" href="/controls/data-display/collections/listbox" icon="/icons/listbox-icon@2x.png" darkIcon="/icons/listbox-icon-dark@2x.png">
  <p>列表成行展示信息，比如联系人、语言或音乐流派。</p>
</DocsCard>

<DocsCard header="Markdown" href="/controls/data-display/text-display/markdown" icon="/icons/markdownrenderer-icon@2x.png" darkIcon="/icons/markdownrenderer-icon-dark@2x.png">
  <p>在应用中直接渲染并展示 Markdown 格式的文本内容。</p>
  <Pill>Avalonia Pro</Pill>
</DocsCard>

<DocsCard header="MediaPlayer" href="/controls/media/mediaplayer" icon="/icons/mediaplayer-icon@2x.png" darkIcon="/icons/mediaplayer-icon-dark@2x.png">
  <p>功能完备的媒体播放控件，可播放音频和视频。</p>
  <Pill>Avalonia Pro</Pill>
</DocsCard>

<DocsCard header="Menu" href="/controls/menus/menu" icon="/icons/menu-icon@2x.png" darkIcon="/icons/menu-icon-dark@2x.png">
  <p>用菜单组织各项功能，让导航更顺手。</p>
</DocsCard>

<DocsCard header="On-Screen Keyboard" href="/controls/input/text-input/virtualkeyboard" icon="/icons/onscreenkeyboard-icon@2x.png" darkIcon="/icons/onscreenkeyboard-icon-dark@2x.png">
  <p>虚拟键盘，供没有实体键盘的设备通过触摸输入文字。</p>
  <Pill>Avalonia Pro</Pill>
</DocsCard>

<DocsCard header="PdfViewer" href="/controls/data-display/pdfviewer" icon="/icons/pdfviewer-icon@2x.png" darkIcon="/icons/pdfviewer-icon-dark@2x.png">
  <p>在桌面、移动和浏览器上查看、搜索、批注、填写并打印 PDF 文档。</p>
  <Pill>Avalonia Pro</Pill>
</DocsCard>

<DocsCard header="Panel" href="/controls/layout/panels/panel" icon="/icons/panel-icon@2x.png" darkIcon="/icons/panel-icon-dark@2x.png">
  <p>所有面板元素的基类，用于摆放和排布子控件。</p>
</DocsCard>

<DocsCard header="RadioButton" href="/controls/input/buttons/radiobutton" icon="/icons/radiobutton-icon@2x.png" darkIcon="/icons/radiobutton-icon-dark@2x.png">
  <p>单选按钮用于呈现一组互斥的选项。</p>
</DocsCard>

<DocsCard header="Rectangle" href="/docs/graphics-animation/drawing-graphics" icon="/icons/rectangle-icon@2x.png" darkIcon="/icons/rectangle-icon-dark@2x.png">
  <p>一个基础图形原语，用于在界面中绘制矩形和正方形。</p>
</DocsCard>

<DocsCard header="RichTextEditor" href="/controls/input/text-input/richtexteditor" icon="/icons/rte-icon@2x.png" darkIcon="/icons/rte-icon-dark@2x.png">
  <p>一套富文本方案，支持格式设置、对齐、撤销/重做等常见操作。</p>
  <Pill>Avalonia Pro</Pill>
</DocsCard>

<DocsCard header="ScrollViewer" href="/controls/layout/containers/scrollviewer" icon="/icons/scrollviewer-icon@2x.png" darkIcon="/icons/scrollviewer-icon-dark@2x.png">
  <p>一个容器控件，当子内容超出可用空间时提供滚动能力。</p>
</DocsCard>

<DocsCard header="Slider" href="/controls/input/selectors/slider" icon="/icons/slider-icon@2x.png" darkIcon="/icons/slider-icon-dark@2x.png">
  <p>滑块让用户沿轨道拖动滑钮来选取数值。</p>
</DocsCard>

<DocsCard header="SplitView" href="/controls/layout/containers/splitview" icon="/icons/splitview-icon@2x.png" darkIcon="/icons/splitview-icon-dark@2x.png">
  <p>一个带可折叠侧栏和内容区的容器，很适合做导航布局。</p>
</DocsCard>

<DocsCard header="StackPanel" href="/controls/layout/panels/stackpanel" icon="/icons/stackpanel-icon@2x.png" darkIcon="/icons/stackpanel-icon-dark@2x.png">
  <p>把子控件排成一行或一列。</p>
</DocsCard>

<DocsCard header="Tab" href="/controls/navigation/tabcontrol" icon="/icons/tabcontrol-icon@2x.png" darkIcon="/icons/tabcontrol-icon-dark@2x.png">
  <p>选项卡提供分页式导航 —— 现代应用中的标准导航范式。</p>
</DocsCard>

<DocsCard header="TableView" href="/controls/data-display/structured-data/tableview" icon="/icons/tableview-icon@2x.png" darkIcon="/icons/tableview-icon-dark@2x.png">
  <p>一个只读的表格控件，按可配置的列来呈现数据。</p>
</DocsCard>

<DocsCard header="TextBlock" href="/controls/data-display/text-display/textblock" icon="/icons/textblock-icon@2x.png" darkIcon="/icons/textblock-icon-dark@2x.png">
  <p>一个轻量控件，用于显示少量只读文本。</p>
</DocsCard>

<DocsCard header="TextBox" href="/controls/input/text-input/textbox" icon="/icons/textbox-icon@2x.png" darkIcon="/icons/textbox-icon-dark@2x.png">
  <p>文本框提供文字输入区域，几乎任何应用都离不开它。</p>
</DocsCard>

<DocsCard header="ToggleSwitch" href="/controls/input/selectors/toggleswitch" icon="/icons/toggleswitch-icon@2x.png" darkIcon="/icons/toggleswitch-icon-dark@2x.png">
  <p>开关让用户在开与关之间切换，适合设置项这类二元选项。</p>
</DocsCard>

<DocsCard header="TreeDataGrid" href="/controls/data-display/structured-data/treedatagrid" icon="/icons/treeview-icon@2x.png" darkIcon="/icons/treeview-icon-dark@2x.png">
  <p>把树视图与数据网格结合起来，用于展示复杂的扁平或层级数据。</p>
  <Pill>Avalonia Pro</Pill>
</DocsCard>

<DocsCard header="UniformGrid" href="/controls/layout/panels/uniformgrid" icon="/icons/uniformgrid-icon@2x.png" darkIcon="/icons/uniformgrid-icon-dark@2x.png">
  <p>一个网格面板，自动把所有单元格调成等大，形成均匀布局。</p>
</DocsCard>

<DocsCard header="WebView" href="/controls/web/nativewebview" icon="/icons/webview-icon@2x.png" darkIcon="/icons/webview-icon-dark@2x.png">
  <p>借助原生浏览器引擎，把网页内容直接嵌进你的应用。</p>
</DocsCard>

</DocsCards>
