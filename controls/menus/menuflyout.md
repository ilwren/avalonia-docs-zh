---
id: menuflyout
title: MenuFlyout
description: 一个浮出控件，用于展示一份简单的命令菜单，通常挂在按钮或其他控件上。
doc-type: reference
---

import MenuFlyoutScreenshot from '/img/reference/controls/menuflyout/menuflyout-button.gif';

`MenuFlyout` 让你把一份简单的菜单作为控件的浮出内容来承载。你可以拿它当作 [ContextMenu](/controls/menus/contextmenu) 的替代方案。

菜单浮出控件的属性与 [Flyout](/controls/layout/containers/flyout) 相同。

## Example

下面是菜单浮出控件的一个简单例子：

<XamlPreview>

```xml
<Button xmlns="https://github.com/avaloniaui"
        Content="Button"
        HorizontalAlignment="Center">
  <Button.Flyout>
    <MenuFlyout>
      <MenuItem Header="Open"/>
      <MenuItem Header="-"/>
      <MenuItem Header="Close"/>        
    </MenuFlyout>
  </Button.Flyout>
</Button>
```

</XamlPreview>

:::info
请注意 `<Separator/>` 元素在菜单浮出控件中不起作用。要画分隔线，请像上面那样用 header 设为 '-' 的 `<MenuItem>` 元素。
:::

## 搭配命令与图标 {#with-commands-and-icons}

```xml
<Button Content="Actions">
    <Button.Flyout>
        <MenuFlyout>
            <MenuItem Header="Open" Command="{Binding OpenCommand}">
                <MenuItem.Icon>
                    <PathIcon Data="{StaticResource open_regular}" />
                </MenuItem.Icon>
            </MenuItem>
            <MenuItem Header="-" />
            <MenuItem Header="Delete" Command="{Binding DeleteCommand}"
                      CommandParameter="{Binding SelectedItem}" />
        </MenuFlyout>
    </Button.Flyout>
</Button>
```

## Dynamic MenuFlyout

下面这个例子中的 `MenuFlyout` 是运行时动态生成的，数据源是一个元素类型为 `MyMenuItemViewModel` 的集合 `MyMenuItems`。

```xml
<Button Content="Button">
  <Button.Flyout>
    <MenuFlyout ItemsSource="{Binding MyMenuItems}">
      <MenuFlyout.ItemContainerTheme>
        <ControlTheme TargetType="MenuItem" BasedOn="{StaticResource {x:Type MenuItem}}" 
          x:DataType="l:MyMenuItemViewModel">

          <Setter Property="Header" Value="{Binding Header}"/>
          <Setter Property="ItemsSource" Value="{Binding Items}"/>
          <Setter Property="Command" Value="{Binding Command}"/>
          <Setter Property="CommandParameter" Value="{Binding CommandParameter}"/>
          
        </ControlTheme>
      </MenuFlyout.ItemContainerTheme>
    </MenuFlyout>
  </Button.Flyout>
</Button>
```

## Placement

设置 `Placement` 属性即可控制浮出内容相对目标控件出现的位置。该属性接受 `FlyoutPlacementMode` 取值，可选项包括 `Top`、`Bottom`、`Left`、`Right`、`TopEdgeAlignedLeft`、`TopEdgeAlignedRight`、`BottomEdgeAlignedLeft`、`BottomEdgeAlignedRight` 等。

```xml
<Button Content="Options">
    <Button.Flyout>
        <MenuFlyout Placement="BottomEdgeAlignedLeft">
            <MenuItem Header="Settings"/>
            <MenuItem Header="About"/>
        </MenuFlyout>
    </Button.Flyout>
</Button>
```

若不设置 `Placement`，浮出控件会采用由其所附着控件决定的默认位置。

## 另请参阅 {#see-also}

- [MenuFlyout API 参考](/api/avalonia/controls/menuflyout)
- [GitHub 上的 `MenuFlyout.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Flyouts/MenuFlyout.cs)
- [Separator](/controls/menus/separator)
- [Menu](/controls/menus/menu)
