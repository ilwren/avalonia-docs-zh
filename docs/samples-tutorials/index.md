---
id: index
title: 示例与教程
description: 浏览 Avalonia 的教程、示例应用和速查指南，让学习事半功倍。
doc-type: overview
hide_table_of_contents: true
---

import DocsCard from '@site/src/components/global/DocsCard';
import DocsCards from '@site/src/components/global/DocsCards';

<head>
  <title>Avalonia 文档：示例与教程</title>
  <meta
    name="description"
    content="Explore Avalonia tutorials, sample apps, and quick guides to accelerate your learning."
  />
  <style>{`
    :root {
      --doc-item-container-width: 60rem;
    }
  `}</style>
</head>

浏览教程、示例应用和速查指南，让 Avalonia 的学习事半功倍。

## Tutorials

<DocsCards>

  <DocsCard header="Starter Tutorial" href="/docs/get-started/starter-tutorial">
    <p>一步步做出你的第一个 Avalonia 应用，从控件、布局一路讲到事件和数据转换。</p>
  </DocsCard>

  <DocsCard header="ToDo List App" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/CompleteApps/SimpleToDoList">
    <p>用 MVVM 模式做一个待办清单应用，涉及绑定、命令、样式和基本的输入输出。</p>
  </DocsCard>

  <DocsCard header="Music Store App" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/CompleteApps/Avalonia.MusicStore">
    <p>做一个图形化的唱片店应用，涉及对话框、图片、集合和数据持久化。</p>
  </DocsCard>

</DocsCards>

## MVVM 示例 {#mvvm-samples}

<DocsCards>

  <DocsCard header="Basic MVVM" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/MVVM/BasicMvvmSample">
    <p>用 MVVM 模式接收并处理用户输入的文本。</p>
  </DocsCard>

  <DocsCard header="Binding and converters" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/BindingsAndConverters">
    <p>把日期转换成字符串，并据此算出一个人的年龄。</p>
  </DocsCard>

  <DocsCard header="Value converter" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/MVVM/ValueConversionSample">
    <p>在绑定中引入转换器，为视图算出新的值。</p>
  </DocsCard>

  <DocsCard header="Commands" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/MVVM/CommandSample">
    <p>如何用命令从界面调用 ViewModel 中的方法。</p>
  </DocsCard>

  <DocsCard header="Data validation" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/MVVM/ValidationSample">
    <p>校验属性，并在取值非法时显示错误信息。</p>
  </DocsCard>

  <DocsCard header="Dialog manager" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/ViewInteraction/DialogManagerSample">
    <p>编写一个对话框管理服务，方便在应用中弹出对话框。</p>
  </DocsCard>

</DocsCards>

## 数据模板示例 {#data-templates-samples}

<DocsCards>

  <DocsCard header="Basic DataTemplate" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/DataTemplates/BasicDataTemplateSample">
    <p>用 DataTemplate 掌控数据的显示方式。</p>
  </DocsCard>

  <DocsCard header="FuncDataTemplate" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/DataTemplates/FuncDataTemplateSample">
    <p>用 FuncDataTemplate 在代码中创建更高级的 DataTemplate。</p>
  </DocsCard>

  <DocsCard header="IDataTemplate" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/DataTemplates/IDataTemplateSample">
    <p>在自己的类中实现 IDataTemplate，完全掌控 DataTemplate。</p>
  </DocsCard>

</DocsCards>

## 样式与绘图示例 {#styles-and-drawing-samples}

<DocsCards>

  <DocsCard header="Button customization" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/ButtonCustomize">
    <p>创建可复用的样式，定制按钮的外观。</p>
  </DocsCard>

  <DocsCard header="Making lists" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/MakingLists">
    <p>借助绑定和 ListBox 控件做出数据列表。</p>
  </DocsCard>

  <DocsCard header="Native menus" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/NativeMenuOps">
    <p>在 macOS 和 Linux 上为 Avalonia 应用启用原生菜单。</p>
  </DocsCard>

  <DocsCard header="Splash screen" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/SplashScreen">
    <p>做一个在 MainWindow 之前加载的自定义启动画面。</p>
  </DocsCard>

  <DocsCard header="Rect painter" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/Drawing/RectPainter">
    <p>做一个能响应鼠标的自绘控件，拼出一个简易画图应用。</p>
  </DocsCard>

  <DocsCard header="Loading images" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/LoadingImages">
    <p>看看如何通过 XAML、绑定以及从网络加载图片。</p>
  </DocsCard>

  <DocsCard header="Using fonts" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/GoogleFonts">
    <p>在应用中使用自定义字体，比如 Google 字体。</p>
  </DocsCard>

  <DocsCard header="Battle City" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/Drawing/BattleCity">
    <p>一个 Avalonia 版的 2D 小游戏示例，全程没写一行渲染代码。</p>
  </DocsCard>

</DocsCards>

## 自定义控件示例 {#custom-controls-samples}

<DocsCards>

  <DocsCard header="Rating control" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/CustomControls/RatingControlSample">
    <p>做一个评分控件，让用户点击星星来投票。</p>
  </DocsCard>

  <DocsCard header="Snowflake control" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/CustomControls/SnowflakesControlSample">
    <p>做一个重写 OnRender 的自定义控件，用上更高级的渲染方式。</p>
  </DocsCard>

</DocsCards>

## 测试示例 {#testing-samples}

<DocsCards>

  <DocsCard header="Headless testing with XUnit" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/Testing/TestableApp.Headless.XUnit">
    <p>借助 Avalonia 的无头平台配合 XUnit，在没有可见图形界面的情况下测试应用。</p>
  </DocsCard>

  <DocsCard header="Headless testing with NUnit" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/Testing/TestableApp.Headless.NUnit">
    <p>借助 Avalonia 的无头平台配合 NUnit，在没有可见图形界面的情况下测试应用。</p>
  </DocsCard>

  <DocsCard header="Testing with Appium" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/Testing/TestableApp.Appium">
    <p>针对按钮点击、文本输入、页面导航等界面交互的自动化测试。</p>
  </DocsCard>

</DocsCards>

## Charts

:::info
[`Charts`](/controls/data-display/charts) 是 [Avalonia Pro](https://avaloniaui.net/pricing) 的一部分。
:::

<DocsCards>
  <DocsCard header="Charts samples" href="https://github.com/AvaloniaUI/AvaloniaPro.Samples/tree/main/ChartsSample">
    <p>如何在浏览器、桌面、Android 和 iOS 等各平台上实现图表。</p>
  </DocsCard>
</DocsCards>

## RichTextEditor

:::info
[`RichTextEditor`](/controls/input/text-input/richtexteditor) 是 [Avalonia Pro](https://avaloniaui.net/pricing) 的一部分。
:::

<DocsCards>
  <DocsCard header="RichTextEditor demo" href="https://github.com/AvaloniaUI/AvaloniaPro.Samples/tree/main/RichTextEditorSample/RichTextEditor.Demo">
    <p>演示 RichTextEditor 常用功能的示例项目。</p>
  </DocsCard>

  <DocsCard header="Document viewer" href="https://github.com/AvaloniaUI/AvaloniaPro.Samples/tree/main/RichTextEditorSample/DocumentViewer.Demo">
    <p>演示把 RichTextEditor 当作文档查看器使用的示例项目。</p>
  </DocsCard>
</DocsCards>

## 其他示例 {#other-samples}

<DocsCards>

  <DocsCard header="Clipboard operations" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/ClipboardOps">
    <p>与设备剪贴板打交道，复制和粘贴文本。</p>
  </DocsCard>

  <DocsCard header="Drag-and-drop operations" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/DragDropOps">
    <p>在 Avalonia 应用中实现拖放。</p>
  </DocsCard>

  <DocsCard header="Native file operations" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/FileOps">
    <p>使用原生的「另存为」和「打开文件」对话框。</p>
  </DocsCard>

  <DocsCard header="IoC file operations" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/IoCFileOps">
    <p>结合控制反转（IoC）使用原生的「另存为」和「打开文件」对话框。</p>
  </DocsCard>

  <DocsCard header="Localization" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/Localization">
    <p>一个 Avalonia 应用本地化的示例。</p>
  </DocsCard>

  <DocsCard header="Basic view locator" href="https://github.com/AvaloniaUI/Avalonia.Samples/tree/main/src/Avalonia.Samples/Routing/BasicViewLocatorSample">
    <p>用视图定位器切换界面内容。</p>
  </DocsCard>

  <DocsCard header="Native AOT" href="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/NativeAot">
    <p>把应用配置为用原生预编译（AOT）构建。</p>
  </DocsCard>

</DocsCards>

## 另请参阅 {#see-also}

- [入门](/docs/get-started/create-your-first-project)：创建你的第一个 Avalonia 应用。
- [控件参考](/controls)：Avalonia 控件的完整文档。
