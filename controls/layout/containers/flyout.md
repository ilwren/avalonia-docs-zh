---
id: flyout
title: Flyout
---

import FlyoutShowAttachedScreenshot from '/img/controls/flyout/flyout-show-attached.gif';

flyout 是一种可关闭的容器，能挂到某几类「宿主」控件上——不过 flyout 本身并不是控件。宿主控件获得焦点时它会显示出来，随后可以通过多种方式隐藏。

flyout 既可以装简单内容，也可以装层次丰富的组合界面。

在 _Avalonia_ 应用中，flyout 可以声明为资源，在两个及以上的宿主控件之间共享。

## 示例 {#examples}

flyout 通过宿主的 [`Flyout`](/api/avalonia/controls/flyout) 属性挂到宿主控件上。例如：

<XamlPreview>

```xml
<UserControl xmlns="https://github.com/avaloniaui"
             Padding="20">
  <Button Content="Button with flyout">
    <Button.Flyout >
      <Flyout>This is the button flyout.</Flyout>
    </Button.Flyout>
  </Button>
</UserControl>
```

</XamlPreview>

:::caution
只有 button 和 split button 控件支持 `Flyout` 属性。要把 flyout 挂到其他 _Avalonia_ 内置控件上，请改用 `AttachedFlyout` 属性。
:::

对于没有 `Flyout` 属性的控件，请使用 `AttachedFlyout` 属性。此时 flyout 不会自动显示，得在代码隐藏中自行控制。

```xml
<Border Background="Red" PointerPressed="Border_PointerPressed">
    <FlyoutBase.AttachedFlyout>
        <Flyout>
            <TextBlock Text="Red Rectangle Flyout." />
        </Flyout>
    </FlyoutBase.AttachedFlyout>
</Border>
```

```csharp
public void Border_PointerPressed(object sender, PointerPressedEventArgs args)
{
    var ctl = sender as Control;
    if (ctl != null)
    {
        FlyoutBase.ShowAttachedFlyout(ctl);
    }
}
```

<Image light={FlyoutShowAttachedScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

| 属性          | 说明                                                                          |
| ----------------- | ------------------------------------------------------------------------------------ |
| `Content`         | flyout 内部显示的内容。                                             |
| `ContentTemplate` | 作用于 `Content` 的 `DataTemplate`。当 `Content` 绑定到视图模型对象时很有用。 |
| `Placement`       | flyout 相对于其所挂控件的弹出位置。 |
| `ShowMode`        | 描述 flyout 如何显示和隐藏，可选项见下文。                |

## 显示模式 {#show-mode}

该设置描述 flyout 如何显示和隐藏：

<table><thead><tr><th width="259">Mode</th><th>说明</th></tr></thead><tbody><tr><td><code>Standard</code></td><td>所挂控件获得焦点时 flyout 显示；该控件失去焦点时（用户按 Tab 切走或点击别处）flyout 隐藏。 </td></tr><tr><td><code>Transient</code></td><td></td></tr><tr><td><code>TransientWithDismiss OnPointerMoveAway</code></td><td></td></tr></tbody></table>

## 所有 flyout 通用的方法 {#common-methods-for-all-flyouts}

| 属性                | 说明                                                                             |
| ----------------------- | --------------------------------------------------------------------------------------- |
| `ShowAt(Control)`       | 在指定目标处显示 flyout                                                |
| `ShowAt(Control, bool)` | 在指定目标处显示 flyout，但把它摆在当前指针位置 |
| `Hide`                  | 隐藏 flyout                                                                        |

## 共享 flyout {#sharing-flyouts}

同一个 flyout 可以在应用中的多个元素之间共享。比如从窗口的资源集合中共享一个 flyout：

```xml
<Window.Resources>
    <Flyout x:Key="MySharedFlyout">
        <!-- Flyout content here -->
    </Flyout>
</Window.Resources>

<Button Content="Click me!" Flyout="{StaticResource MySharedFlyout}" />

<Button Content="Now click me!" Flyout="{StaticResource MySharedFlyout}" />
```

## 为 flyout 设置样式 {#styling-flyouts}

flyout 本身虽然不是控件，但可以通过定位 `Flyout` 用来显示内容的那个呈现器来定制整体外观：普通 `Flyout` 对应的是 `FlyoutPresenter`，`MenuFlyout` 对应的则是 `MenuFlyoutPresenter`。由于 flyout 呈现器并不对外暴露，若某些样式类只想作用于特定的 flyout，可以通过 `FlyoutBase` 上的 `FlyoutPresenterClasses` 属性传入

```xml
<Style Selector="FlyoutPresenter.mySpecialClass">
    <Setter Property="Background" Value="Red" />
</Style>

<Flyout FlyoutPresenterClasses="mySpecialClass">
    <!-- Flyout content here -->
</Flyout>
```

## 另请参阅 {#see-also}

- [Flyout API 参考](/api/avalonia/controls/flyout)
- [GitHub 上的 `Flyout.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Flyouts/Flyout.cs)
