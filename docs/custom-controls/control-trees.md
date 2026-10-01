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

When building custom controls, you often need to respond to a control being added to or removed from a tree. Override these methods to hook into tree lifecycle events.

- `OnAttachedToLogicalTree` / `OnDetachedFromLogicalTree` for setup and cleanup of data bindings, subscriptions, or inherited properties.
- `OnAttachedToVisualTree` / `OnDetachedFromVisualTree` for rendering-related setup, such as acquiring platform resources.

Here is an example showing how to hook your custom control to the visual tree lifecycle.

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

## Where to mutate `LogicalChildren`

When a custom container needs to add or remove logical children programmatically (for example, inserting separators between items), do this inside a structured lifecycle hook, e.g., `OnApplyTemplate`, rather than a property-change callback like `DataContextChanged` or `OnPropertyChanged`. Mutating `LogicalChildren` while the logical tree is being walked can result in binding errors.

See [Mutating the logical tree](/docs/fundamentals/visual-and-logical-trees#mutating-the-logical-tree) for more information on safe and unsafe contexts.

## 另请参阅 {#see-also}

- [Visual and logical trees](/docs/fundamentals/visual-and-logical-trees): Fundamental concepts.
- [Custom templated controls](/docs/custom-controls/templated-controls): How templates expand into the visual tree.
- [Defining events](/docs/custom-controls/defining-events): Add routed events that travel through the control tree.
- [Creating custom controls](/docs/custom-controls): Overview of the custom control types.
