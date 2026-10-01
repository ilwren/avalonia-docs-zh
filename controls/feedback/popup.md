---
id: popup
title: Popup
---

[`Popup`](/api/avalonia/controls/primitives/popup) 是一个底层控件，把内容显示在浮于其他内容之上的悬浮窗口里。`Flyout`、[`ToolTip`](/api/avalonia/controls/tooltip)、`ComboBox` 下拉列表和上下文菜单等高层控件都建立在它之上。只有当这些控件提供不了你想要的定位或关闭行为时，才需要直接使用 `Popup`。

:::info
绝大多数场景下，请优先选用 `Flyout`、`ToolTip` 或 `ContextMenu`，而不是 `Popup`。这些高层控件已经帮你处理好了无障碍访问、键盘导航和点击外部自动关闭的行为。
:::

## 常用属性 {#useful-properties}

| 属性 | 类型 | 说明 |
|---|---|---|
| `IsOpen` | `bool` | 控制弹出窗口当前是否可见。 |
| `Child` | `Control` | 弹出窗口内部显示的内容。 |
| `Placement` | `PlacementMode` | 弹出窗口相对目标的定位方式。可选 `Bottom`、`Top`、`Left`、`Right`、`Center`、`Pointer`、`AnchorAndGravity`，默认 `Bottom`。 |
| `PlacementTarget` | `Control` | 弹出窗口定位时所参照的控件，默认是该弹出窗口的父级。 |
| `PlacementAnchor` | `PopupAnchor` | 目标控件上的锚点。 |
| `PlacementGravity` | `PopupGravity` | 弹出窗口从锚点向哪个方向展开。 |
| `HorizontalOffset` | `double` | 相对于计算所得位置的水平偏移。 |
| `VerticalOffset` | `double` | 相对于计算所得位置的垂直偏移。 |
| `IsLightDismissEnabled` | `bool` | 为 `true` 时，用户点击弹出窗口外部即将其关闭。默认 `false`。 |
| `Topmost` | `bool` | 弹出窗口是否显示在所有其他窗口之上。默认 `false`。 |
| `WindowManagerAddShadowHint` | `bool` | 是否应用投影（取决于平台）。默认 `true`。 |
| `OverlayDismissEventPassThrough` | `bool` | 为 `true` 时，关闭弹出窗口的那次指针事件会继续传递给下层控件。默认 `false`。 |
| `CustomPopupPlacementCallback` | `CustomPopupPlacementCallback` | 一个完全自定义弹出窗口定位的回调。一旦设置，它会覆盖 `Placement` 属性。 |

## 事件 {#events}

| 事件 | 说明 |
|---|---|
| `Opened` | 弹出窗口打开后引发。 |
| `Closed` | 弹出窗口关闭后引发。 |

## 基本示例 {#basic-example}

```xml
<Panel>
    <Button x:Name="ToggleButton" Content="Show Popup"
            Click="OnTogglePopup" />

    <Popup x:Name="MyPopup"
           PlacementTarget="{Binding #ToggleButton}"
           Placement="Bottom"
           IsLightDismissEnabled="True">
        <Border Background="{DynamicResource SystemControlBackgroundAltHighBrush}"
                BorderBrush="{DynamicResource SystemControlForegroundBaseMediumBrush}"
                BorderThickness="1" CornerRadius="4" Padding="12">
            <TextBlock Text="This is popup content." />
        </Border>
    </Popup>
</Panel>
```

```csharp
private void OnTogglePopup(object sender, RoutedEventArgs e)
{
    MyPopup.IsOpen = !MyPopup.IsOpen;
}
```

## 定位模式 {#placement-modes}

`Placement` 属性控制弹出窗口出现的位置：

| 模式 | 行为 |
|---|---|
| `Bottom` | 在目标下方，左对齐。 |
| `Top` | 在目标上方，左对齐。 |
| `Left` | 在目标左侧，上对齐。 |
| `Right` | 在目标右侧，上对齐。 |
| `Center` | 覆盖在目标上并居中。 |
| `Pointer` | 在指针当前所在位置。 |
| `AnchorAndGravity` | 用 `PlacementAnchor` 和 `PlacementGravity` 做精确定位。 |

## Binding `IsOpen`

按 MVVM 的做法，可以把 `IsOpen` 绑定到视图模型的属性上：

```xml
<Popup IsOpen="{Binding IsPopupVisible}"
       PlacementTarget="{Binding #AnchorControl}"
       Placement="Bottom"
       IsLightDismissEnabled="True">
    <Border Background="White" Padding="16" CornerRadius="4"
            BoxShadow="0 2 8 0 #40000000">
        <StackPanel Spacing="8">
            <TextBlock Text="Choose an option:" FontWeight="SemiBold" />
            <Button Content="Option A" Command="{Binding SelectOptionCommand}"
                    CommandParameter="A" />
            <Button Content="Option B" Command="{Binding SelectOptionCommand}"
                    CommandParameter="B" />
        </StackPanel>
    </Border>
</Popup>
```

## 自定义定位 {#custom-placement}

若内置的定位模式满足不了你的定位逻辑，就用 `CustomPopupPlacementCallback`。该回调会收到一个已按默认值初始化好的 `CustomPopupPlacement` 对象，你修改它的属性即可控制定位：

```csharp
myPopup.CustomPopupPlacementCallback = placement =>
{
    placement.Anchor = PopupAnchor.TopRight;
    placement.Gravity = PopupGravity.BottomRight;
    placement.Offset = new Point(8, 0);
};
```

这个回调在 `PopupFlyoutBase`、`ContextMenu` 上同样可用，在 `ToolTip` 上则以附加属性的形式提供：

```csharp
ToolTip.SetCustomPopupPlacementCallback(myControl, placement =>
{
    placement.Offset = new Point(0, -10);
});
```

## Popup、Flyout 与 ToolTip 的取舍 {#popup-vs-flyout-vs-tooltip}

| 特性 | Popup | Flyout | ToolTip |
|---|---|---|---|
| Level | 底层原语 | 高层，附着于控件 | 高层，附着于控件 |
| Trigger | Manual (`IsOpen`) | 代码调用或附着于控件 | Hover |
| 点击外部自动关闭 | Optional | Built-in | Built-in |
| 键盘支持 | Manual | Automatic | 不适用 |
| 适用场景 | 自定义覆盖层行为 | 菜单、确认框、选择器 | 悬停提示 |

## 另请参阅 {#see-also}

- [Flyout](/controls/layout/containers/flyout)：附着在控件上的高层弹出内容。
- [ToolTip](/controls/feedback/tooltip)：悬停触发、用于补充说明的弹出提示。
- [ContextMenu](/controls/menus/contextmenu)：右键菜单。
