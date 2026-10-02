---
id: resources-tool
title: 资源工具
doc-type: reference
description: 用 DevTools 中的资源工具在运行时检视、浏览并编辑 Avalonia 应用的资源层级。
---

资源工具把应用的资源层级呈现出来，让你在运行时检视、浏览并修改资源。借助它，你能摸清 Avalonia 应用中的资源是怎么组织、怎么解析的。

查找资源时，Avalonia 会沿这套层级一路搜寻，直到找到匹配的键。资源工具把应用级的层级可视化，让你一眼看清哪些资源是全局可用的。

关于 Avalonia 资源的更多信息，请见[如何使用资源](https://docs.avaloniaui.net/docs/guides/styles-and-resources/resources)。

:::note

控件专属的资源（定义在单个控件上或控件模板内部的那些）目前还不会在此工具中显示。

:::

## 浏览资源提供程序树 {#navigating-the-resource-providers-tree}

左侧面板显示一棵资源提供程序树，其中包括：

1. Application（根级）
2. 资源字典
3. 主题字典
4. Styles
5. 其他非字典型的资源提供程序

树中每个节点代表一个资源作用域。选中某个节点，右侧面板便会显示它的资源。

![资源树](/img/tools/dev-tools/resources-providers-list.png)

## 检视与编辑资源 {#inspecting-and-editing-resources}

右侧面板显示所选提供程序中可用的资源。

你可以直接在这个视图里编辑资源，试各种值，改动会立刻反映到你的应用上。

![提供程序树](/img/tools/dev-tools/resources-provider-values.png)

:::note

向提供程序中新增资源目前还不支持。

:::

### 资源编辑与 XAML 的对应关系 {#how-resource-editing-maps-to-xaml}

你在资源工具中改某个资源值时，改的就是 XAML 资源定义在运行时创建出的那个对象。举例来说，设你的 `App.axaml` 中有这样几条 XAML 资源定义：

```xml
<Application.Resources>
    <SolidColorBrush x:Key="PrimaryBrush" Color="#0078D4" />
    <x:Double x:Key="DefaultFontSize">14</x:Double>
    <Thickness x:Key="StandardPadding">8,12,8,12</Thickness>
</Application.Resources>
```

这些资源会出现在资源工具的 **Application** 节点下。你可以选中 `PrimaryBrush`，在运行时改它的 `Color` 属性，不必重新构建就能预览另一种主题色。

若你的控件是用 `DynamicResource` 引用这些资源的，它们会自动更新：

```xml
<Button Background="{DynamicResource PrimaryBrush}"
        FontSize="{DynamicResource DefaultFontSize}"
        Padding="{DynamicResource StandardPadding}"
        Content="Save" />
```

等调到满意的值，再把它们抄回 XAML 源码中固化下来。

## 筛选与排序 {#filtering-and-sorting}

资源工具提供了几种选项，帮你找到特定资源：

- **Include Nested**：启用后会显示所选节点及其子节点下所有可用的资源，模拟运行时资源查找的效果。借此你能看清从层级中某一处出发都能取到哪些资源。
- **Sort by**：按键名的字母顺序排列，或按类型分组。
- **Order**：升序或降序排列。
- **Search filter**：按键名或类型搜索资源。

![筛选视图](/img/tools/dev-tools/resources-filter.png)

## 另请参阅 {#see-also}

- [元素工具](/tools/developer-tools/elements-tool)
- [资产工具](/tools/developer-tools/assets-tool)
- [如何使用资源](https://docs.avaloniaui.net/docs/guides/styles-and-resources/resources)
