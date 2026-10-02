---
id: windowdrawndecorations
title: WindowDrawnDecorations
description: 一个逻辑元素，负责在客户端绘制并管理窗口装饰（如标题栏和边框），同时定义标题栏按钮的交互行为。
doc-type: reference
---

`WindowDrawnDecorations` 不是可视控件，而是一个逻辑元素：它持有标题栏、边框等窗口装饰的模板和属性，以便在客户端完成它们的绘制与呈现。

此外，`WindowDrawnDecorations` 还定义了标题栏按钮的交互逻辑。

这个控件取代了早期版本（Avalonia 12 之前）中的 `TitleBar`、`CaptionButtons` 和 `ChromeOverlayLayer` 类。

## 适用场景 {#when-to-use}

需要自定义窗口装饰时就用 `WindowDrawnDecorations`，比如标题栏、边框、标题栏按钮、缩放手柄等等。

## 命名空间 {#namespace}

位于 `Avalonia.Controls.Chrome`。

## 视觉树结构 {#visual-tree-structure}

`WindowDrawnDecorations` 中的可视元素分为**底层**、**覆盖层**和**浮层**三层，按下面的结构组装成视觉树：

```
Visual root
├── Underlay layer        (from template: borders, background, shadow area content)
├── TopLevel/Window       (client area: Window.Bounds matches this)
├── Overlay layer         (from template: titlebar, caption buttons)
├── FullscreenPopover     (from template: hover-triggered titlebar for full-screen)
└── Resize hit-test zones (automatic)
```

这些层在代码中如何实现，请参阅 [`WindowDrawnDecorationsContent`](#windowdrawndecorationscontent)。

## WindowDrawnDecorationsTemplate

构建 `WindowDrawnDecorationsContent` 的自定义模板类型。（参见 [WindowDrawnDecorationsContent](#windowdrawndecorationscontent)。）

## WindowDrawnDecorationsContent

持有 `WindowDrawnDecorationsTemplate` 使用的三个模板槽位。逻辑子元素按上文[视觉树结构](#visual-tree-structure)所述分入各个视觉树层。

```csharp
public class WindowDrawnDecorationsContent : StyledElement
{
    public Control? Overlay { get; set; }           // titlebar, caption buttons
    public Control? Underlay { get; set; }          // borders, background, shadow
    public Control? FullscreenPopover { get; set; } // hover-triggered fullscreen titlebar
}
```

## 属性 {#properties}

| 属性 | 类型 | 可见性 | 说明 |
| --- | --- | --- | --- |
| `Template` | `WindowDrawnDecorationsTemplate` | Styled | 装饰模板。 |
| `DefaultTitleBarHeight` | `double` | Styled | 默认标题栏高度。未设置时由主题决定。 |
| `DefaultFrameThickness` | `Thickness` | Styled | 默认边框厚度。未设置时由主题决定。 |
| `DefaultShadowThickness` | `Thickness` | Styled | 默认阴影厚度。未设置时由主题决定。 |
| `TitleBarHeight` | `double` | Styled | 实际生效的标题栏高度。`Window` 上设置的本地值会覆盖它。 |
| `FrameThickness` | `Thickness` | Styled | 实际生效的边框厚度。`Window` 上设置的本地值会覆盖它。 |
| `ShadowThickness` | `Thickness` | Styled | 实际生效的阴影厚度。`Window` 上设置的本地值会覆盖它。 |
| `Content` | `WindowDrawnDecorationsContent?` | Read-only | 构建完成的模板内容。 |

## 装饰部件 {#decoration-parts}

可用的装饰部件如下：

- Shadow
- Border
- Titlebar
- 缩放手柄

具体能用哪些装饰部件因平台而异，比如 macOS 的缩放手柄由系统自己处理。

## Pseudoclasses

窗口状态变化时会应用相应的伪类，比如 `Window` 从普通变为全屏时。[装饰部件](#decoration-parts) 启用或停用时同样会应用伪类，比如进入全屏导致 `Shadow` 被停用时。

- `:normal`
- `:maximized`
- `:minimized`
- `:fullscreen`
- `:has-shadow`
- `:has-border`
- `:has-titlebar`

## 模板部件 {#template-parts}

`WindowDrawnDecorations` 在应用模板时获取模板部件，并解析其中指定的那些。所有模板部件都是可选的，比如你可以不提供全屏按钮。

这一功能取代了早期 Avalonia 版本中的 `CaptionButtons` 类。

| 部件 | 类型 | 说明 |
| --- | --- | --- |
| `PART_CloseButton` | `Button?` | 关闭按钮。 |
| `PART_MinimizeButton` | `Button?` | 最小化按钮。 |
| `PART_MaximizeButton` | `Button?` | 最大化切换按钮。 |
| `PART_FullScreenButton` | `Button?` | 全屏切换按钮。 |

## 元素角色 {#element-roles}

`ElementRole` 是一个[附加属性](/docs/properties#attached-properties)，用于给每个可视元素标注特定角色，以便跨平台地进行非客户区命中测试。它可以用在视觉树中的任意元素上，不限于装饰的子元素。

可用的元素角色如下：

| 角色 | 说明 |
| --- | --- |
| `None` | 无角色。该元素对命中测试不可见。 |
| `DecorationsElement` | 设在装饰模板元素上的可交互元素，输入会传递给该元素。 |
| `User` | 由用户代码设定的可交互元素，输入会传递给该元素。 |
| `TitleBar` | 标题栏拖动区域。按住并拖动该元素可移动窗口。 |
| `ResizeN` | 上边缘（北）的缩放手柄。 |
| `ResizeS` | 下边缘（南）的缩放手柄。 |
| `ResizeE` | 右边缘（东）的缩放手柄。 |
| `ResizeW` | 左边缘（西）的缩放手柄。 |
| `ResizeNE` | 右上角（东北）的缩放手柄。 |
| `ResizeSE` | 右下角（东南）的缩放手柄。 |
| `ResizeNW` | 左上角（西北）的缩放手柄。 |
| `ResizeSW` | 左下角（西南）的缩放手柄。 |
| `CloseButton` | 该元素执行关闭窗口的行为。 |
| `MaximizeButton` | 该元素执行最大化窗口的行为。 |
| `MinimizeButton` | 该元素执行最小化窗口的行为。 |
| `FullScreenButton` | 该元素执行切换全屏的行为。 |

在[下面的示例](#example)中，一个充当标题栏的 `TextBlock` 被标注了元素角色：`ElementRole="TitleBar"`。

## Example

```xml
<ControlTheme x:Key="{x:Type WindowDrawnDecorations}" TargetType="WindowDrawnDecorations">
    <Setter Property="DefaultTitleBarHeight" Value="32"/>
    <Setter Property="DefaultFrameThickness" Value="0,0,0,0"/>
    <Setter Property="DefaultShadowThickness" Value="16"/>
    <Setter Property="Template">
        <WindowDrawnDecorationsTemplate>
            <WindowDrawnDecorationsContent>

                <WindowDrawnDecorationsContent.Underlay>
                    <!-- Full-size: covers shadow area + frame + behind client area -->
                    <Panel>
                        <Border Margin="{TemplateBinding ShadowThickness}"
                                Background="{DynamicResource WindowBackground}"
                                BorderThickness="1"
                                BorderBrush="{DynamicResource WindowBorderBrush}"
                                BoxShadow="0 8 32 0 #40000000"/>
                    </Panel>
                </WindowDrawnDecorationsContent.Underlay>

                <WindowDrawnDecorationsContent.Overlay>
                    <!-- Positioned over the titlebar area -->
                    <DockPanel Height="{TemplateBinding TitleBarHeight}"
                               VerticalAlignment="Top"
                               Margin="{TemplateBinding ShadowThickness}">
                        <StackPanel DockPanel.Dock="Right" Orientation="Horizontal">
                            <Button x:Name="PART_MinimizeButton" Content="─"/>
                            <Button x:Name="PART_MaximizeButton" Content="□"/>
                            <Button x:Name="PART_CloseButton" Content="✕"/>
                        </StackPanel>
                        <TextBlock Text="{Binding Title}"
                                   VerticalAlignment="Center"
                                   Margin="12,0"
                                   WindowDecorationProperties.ElementRole="TitleBar"/>
                    </DockPanel>
                </WindowDrawnDecorationsContent.Overlay>

                <WindowDrawnDecorationsContent.FullscreenPopover>
                    <!-- Shown on hover at top edge in fullscreen -->
                    <DockPanel Height="{TemplateBinding TitleBarHeight}"
                               Background="#E0000000">
                        <StackPanel DockPanel.Dock="Right" Orientation="Horizontal">
                            <Button x:Name="PART_MinimizeButton" Content="─"/>
                            <Button x:Name="PART_MaximizeButton" Content="□"/>
                            <Button x:Name="PART_CloseButton" Content="✕"/>
                        </StackPanel>
                        <TextBlock Text="{Binding Title}"
                                   Foreground="White"
                                   VerticalAlignment="Center"
                                   Margin="12,0"/>
                    </DockPanel>
                </WindowDrawnDecorationsContent.FullscreenPopover>

            </WindowDrawnDecorationsContent>
        </WindowDrawnDecorationsTemplate>
    </Setter>

    <!-- Pseudoclass styling -->
    <Style Selector="^:maximized /template/ Border">
        <Setter Property="BorderThickness" Value="0"/>
    </Style>
    <Style Selector="^:fullscreen /template/ DockPanel">
        <Setter Property="IsVisible" Value="False"/>
    </Style>
</ControlTheme>
```

## 另请参阅 {#see-aslo}

- [Window 控件](/controls/primitives/window)
- [Avalonia v12 破坏性变更](/docs/avalonia12-breaking-changes)