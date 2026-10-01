---
id: separator
title: 分隔线
description: 一条视觉分隔线，用在 Menu、ContextMenu 和 MenuFlyout 中，把相关的菜单项归为一组。
doc-type: reference
---

[`Separator`](/api/avalonia/controls/separator) 控件在菜单项之间画一条水平线，让相关的命令在视觉上成组。它可以用在 `Menu`、`ContextMenu` 和 `MenuFlyout` 内部。

## 基本用法 {#basic-usage}

在 `MenuItem` 元素之间放一个 `<Separator/>` 元素即可画出分隔线：

<XamlPreview>

```xml
<Menu xmlns="https://github.com/avaloniaui">
  <MenuItem Header="_File">
    <MenuItem Header="_New"/>
    <MenuItem Header="_Open..."/>
    <Separator/>
    <MenuItem Header="_Exit"/>
  </MenuItem>
</Menu>
```

</XamlPreview>

上面的例子中，分隔线把文件相关的操作和退出命令分了开来。

## 在上下文菜单中 {#in-a-context-menu}

`Separator` 在 `ContextMenu` 中的用法完全相同：

<XamlPreview>

```xml
<TextBox xmlns="https://github.com/avaloniaui"
         Text="Right-click for options">
  <TextBox.ContextMenu>
    <ContextMenu>
      <MenuItem Header="Cut"/>
      <MenuItem Header="Copy"/>
      <MenuItem Header="Paste"/>
      <Separator/>
      <MenuItem Header="Select All"/>
    </ContextMenu>
  </TextBox.ContextMenu>
</TextBox>
```

</XamlPreview>

## 纵向变体 {#vertical-variant}

把 `Height` 设为 `NaN`、`Width` 设为 `1`，就能做出一条纵向分隔线：

<XamlPreview>

```xml
<StackPanel xmlns="https://github.com/avaloniaui"
            Orientation="Horizontal">
  <RadioButton GroupName="ViewMode" Content="List" />
  <RadioButton GroupName="ViewMode" Content="Preview" />
  <Separator Height="NaN" Width="1" />
  <Button Content="Save" />
</StackPanel>
```

</XamlPreview>

## 简写写法 {#shorthand-syntax}

把 `MenuItem` 的 header 设为 `"-"`，也能得到同样的分隔线：

```xml
<MenuItem Header="-" />
```

这种简写等价于使用 `<Separator/>`，在用数据绑定构建菜单时尤其方便。

## Styling

你可以在样式中针对 `Separator` 来定制它的外观。比如改变线条颜色：

```xml
<Style Selector="Separator">
  <Setter Property="Background" Value="Gray"/>
  <Setter Property="Margin" Value="4,2"/>
</Style>
```

## 另请参阅 {#see-also}

- [Separator API 参考](/api/avalonia/controls/separator)
- [GitHub 上的 `Separator.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Separator.cs)
- [Menu](/controls/menus/menu)
- [ContextMenu](/controls/menus/contextmenu)
- [MenuFlyout](/controls/menus/menuflyout)
