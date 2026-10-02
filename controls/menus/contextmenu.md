---
id: contextmenu
title: ContextMenu
description: 一个弹出菜单，用户右键点击控件时出现，提供与上下文相关的操作。
doc-type: reference
---

[`ContextMenu`](/api/avalonia/controls/contextmenu) 是一个弹出菜单，右键点击控件时出现，提供与该控件或其内容相关的操作。你通过附加属性把 `ContextMenu` 挂到任意宿主控件上，于是应用中的任何视觉元素都能拥有自己的右键菜单。

:::info
想了解附加属性的工作方式，请见[附加属性](/docs/custom-controls/defining-properties#attached-properties)。
:::

## 基本示例 {#basic-example}

本例把上下文菜单挂在了一个多行文本框上。在预览区里点右键即可看到效果。

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui">
  <TextBox AcceptsReturn="True" TextWrapping="Wrap" Text="Right-click here">
    <TextBox.ContextMenu>
      <ContextMenu>
        <MenuItem Header="Copy"/>
        <MenuItem Header="Paste"/>
      </ContextMenu>
    </TextBox.ContextMenu>
  </TextBox>
</UserControl>
```

</XamlPreview>

## 命令与图标 {#commands-and-icons}

把菜单项绑定到命令、再配上图标，就能做出一个功能完备的上下文菜单：

```xml
<ListBox ItemsSource="{Binding Items}">
    <ListBox.ContextMenu>
        <ContextMenu>
            <MenuItem Header="Edit" Command="{Binding EditCommand}">
                <MenuItem.Icon>
                    <PathIcon Data="{StaticResource edit_regular}" />
                </MenuItem.Icon>
            </MenuItem>
            <MenuItem Header="Delete" Command="{Binding DeleteCommand}">
                <MenuItem.Icon>
                    <PathIcon Data="{StaticResource delete_regular}" />
                </MenuItem.Icon>
            </MenuItem>
            <Separator />
            <MenuItem Header="Properties" Command="{Binding PropertiesCommand}" />
        </ContextMenu>
    </ListBox.ContextMenu>
</ListBox>
```

用 `Separator` 元素把相关的菜单项在视觉上归为一组。

## 把上下文传给命令 {#passing-context-to-commands}

用 `CommandParameter` 把相关的数据项传给你的命令。当上下文菜单挂在列表或集合控件上、而你需要知道用户右键点的是哪一项时，这招尤其有用：

```xml
<ListBox.ContextMenu>
    <ContextMenu>
        <MenuItem Header="Delete"
                  Command="{Binding DeleteCommand}"
                  CommandParameter="{Binding $parent[ListBox].SelectedItem}" />
    </ContextMenu>
</ListBox.ContextMenu>
```

`$parent[ListBox].SelectedItem` 绑定会沿视觉树向上找到父级 `ListBox`，再读取它的 `SelectedItem` 属性。

## 动态构建菜单项 {#dynamically-building-menu-items}

若菜单项取决于运行时数据，可以把 `ItemsSource` 绑定到视图模型中的某个集合：

```xml
<TextBlock Text="Right-click me">
    <TextBlock.ContextMenu>
        <ContextMenu ItemsSource="{Binding ContextActions}" />
    </TextBlock.ContextMenu>
</TextBlock>
```

绑定集合中的每一项都会变成一个 `MenuItem`。你可以用 `DataTemplate` 或 `ItemContainerTheme` 控制这些项的呈现方式。

## 处理打开与关闭 {#handling-opening-and-closing}

处理 `Opening` 和 `Closing` 事件即可响应上下文菜单的生命周期。`Opening` 事件带有一个 `CancelEventArgs` 参数，于是你可以在条件不满足时阻止菜单弹出：

```csharp
private void ContextMenu_Opening(object? sender, System.ComponentModel.CancelEventArgs e)
{
    if (!IsActionAllowed)
    {
        e.Cancel = true; // Prevents the context menu from opening
    }
}
```

```xml
<ContextMenu Opening="ContextMenu_Opening" Closing="ContextMenu_Closing">
    <MenuItem Header="Copy" />
</ContextMenu>
```

当你需要按条件决定是否显示上下文菜单、或者想在菜单出现前更新它的条目时，这很有用。

## 上下文浮出控件 {#context-flyout}

你也可以用 `ContextFlyout` 代替 `ContextMenu`。上下文浮出控件能装下任意内容，而不只是菜单项，界面表现力更强：

```xml
<Border Background="LightGray" Padding="20">
    <Border.ContextFlyout>
        <Flyout>
            <StackPanel Spacing="8" Width="200">
                <TextBlock Text="Options" FontWeight="Bold" />
                <Button Content="Action" />
            </StackPanel>
        </Flyout>
    </Border.ContextFlyout>
    <TextBlock Text="Right-click for options" />
</Border>
```

:::caution
同一个控件不能同时挂上 `ContextFlyout` 和 `ContextMenu`。两个都设了的话，只有一个会生效。
:::

## 常用属性 {#useful-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `ItemsSource` | `IEnumerable` | 把菜单项绑定到一个集合，从而动态生成它们。 |
| `Opening` | `event` | 上下文菜单打开前引发。把 `Cancel` 设为 `true` 可阻止它弹出。 |
| `Closing` | `event` | 上下文菜单关闭时引发。 |
| `Placement` | `PlacementMode` | 控制上下文菜单相对指针出现的位置。 |

## 另请参阅 {#see-also}

- [Menu](/controls/menus/menu)
- [MenuFlyout](/controls/menus/menuflyout)
- [Flyout](/controls/layout/containers/flyout)
- [ContextMenu API 参考](/api/avalonia/controls/contextmenu)
- [GitHub 上的 `ContextMenu.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/ContextMenu.cs)
