---
id: control-trees
title: 控件树与自定义控件
description: 了解在编写自定义控件时，如何利用逻辑树和视觉树的生命周期事件。
doc-type: explanation
---

Avalonia 把控件组织成两棵相关联的树：**逻辑树**和**视觉树**。逻辑树体现应用中控件的层级关系，视觉树则囊括了所有正在渲染的视觉元素。

本文讲的是编写自定义控件时如何与这两棵控件树打交道。

关于控件树的更多内容，请参阅[视觉树与逻辑树](/docs/fundamentals/visual-and-logical-trees)。

## 自定义控件的附加/分离事件 {#attachmentdetachment-events-for-custom-controls}

编写自定义控件时，你常常需要在控件被加入或移出某棵树时做出反应。重写下面这些方法即可挂进树的生命周期事件。

- `OnAttachedToLogicalTree` / `OnDetachedFromLogicalTree`：用于准备和清理数据绑定、订阅或可继承属性。
- `OnAttachedToVisualTree` / `OnDetachedFromVisualTree`：用于渲染相关的准备工作，比如申请平台资源。

下面这个例子演示如何把自定义控件挂到视觉树的生命周期上。

```csharp
protected override void OnAttachedToVisualTree(VisualTreeAttachmentEventArgs e)
{
    base.OnAttachedToVisualTree(e);
    // Control is now part of the visual tree and can be rendered
}

protected override void OnDetachedFromVisualTree(VisualTreeAttachmentEventArgs e)
{
    base.OnDetachedFromVisualTree(e);
    // Clean up rendering resources
}
```

## 该在哪里改动 `LogicalChildren` {#where-to-mutate-logicalchildren}

当自定义容器需要以代码方式增删逻辑子元素时（比如在各项之间插入分隔符），请把这件事放进结构化的生命周期钩子（例如 `OnApplyTemplate`）里，而不要放在 `DataContextChanged`、`OnPropertyChanged` 这类属性变更回调中。在逻辑树正被遍历时改动 `LogicalChildren` 可能引发绑定错误。

关于哪些上下文安全、哪些不安全，详见[改动逻辑树](/docs/fundamentals/visual-and-logical-trees#mutating-the-logical-tree)。

## 另请参阅 {#see-also}

- [视觉树与逻辑树](/docs/fundamentals/visual-and-logical-trees)：基础概念。
- [自定义模板化控件](/docs/custom-controls/templated-controls)：模板如何展开成视觉树。
- [定义事件](/docs/custom-controls/defining-events)：添加可在控件树中传播的路由事件。
- [创建自定义控件](/docs/custom-controls)：各类自定义控件概览。
