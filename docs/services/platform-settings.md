---
id: platform-settings
title: Platform Settings
description: 通过 PlatformSettings 服务访问平台专属设置，比如轻点判定范围、双击时限、系统颜色和热键配置。
doc-type: reference
---

`PlatformSettings` 服务让你能访问平台专属的设置和信息。其中一些设置会在用户改动系统偏好时于运行期间发生变化，你的应用可以据此动态响应。

在任意 `Visual` 上调用 `GetPlatformSettings` 扩展方法即可取得 `PlatformSettings`。关于如何访问平台服务，更多细节请看 [TopLevel](/docs/fundamentals/top-level) 页。

```csharp title="Getting PlatformSettings"
var platformSettings = myControl.GetPlatformSettings();
```

## 方法 {#methods}

### `GetTapSize(PointerType type)`

返回以指针按下位置为中心的一块矩形的大小：指针抬起必须落在这块矩形内，才算作一次轻点手势。该值以设备无关像素为单位。

```csharp
Size GetTapSize(PointerType type);
```

### `GetDoubleTapSize(PointerType type)`

返回以指针按下位置为中心的一块矩形的大小：指针抬起必须落在这块矩形内，才算作一次双击手势。该值以设备无关像素为单位。

```csharp
Size GetDoubleTapSize(PointerType type);
```

### `GetDoubleTapTime(PointerType type)`

返回双击手势中第一次与第二次轻点之间允许的最长间隔。

```csharp
TimeSpan GetDoubleTapTime(PointerType type);
```

### `GetColorValues()`

返回当前的系统颜色值，包括是否启用了深色模式，以及用户选择的强调色。

```csharp
PlatformColorValues GetColorValues();
```

:::tip
内置的 `FluentTheme` 本就支持跟随强调色自动切换，不过你也可以用这个方法，依据系统颜色设置实现自定义逻辑。
:::

## 属性 {#properties}

### `HoldWaitDuration`

获取从指针按下到 `Holding` 事件触发之间的时长。

```csharp
TimeSpan HoldWaitDuration { get; }
```

### `HotkeyConfiguration`

获取 Avalonia 应用在当前平台上的热键配置。该属性返回一个 `PlatformHotkeyConfiguration` 对象，其中包含复制、粘贴、剪切、全选和撤销等常用操作的按键手势。

```csharp
PlatformHotkeyConfiguration HotkeyConfiguration { get; }
```

:::tip
当应用需要以适配平台的方式处理「复制」「粘贴」「剪切」这类人所共知的手势时，`HotkeyConfiguration` 尤其好使。
:::

下面的示例演示如何判断某个按键事件是否命中了当前平台的「复制」手势：

```csharp title="Handling platform-specific hotkeys"
protected override void OnKeyDown(KeyEventArgs e)
{
    var hotkeys = this.GetPlatformSettings()?.HotkeyConfiguration;
    if (hotkeys is not null && hotkeys.Copy.Any(g => g.Matches(e)))
    {
        // Handle Copy hotkey.
    }
}
```

## 事件 {#events}

### `ColorValuesChanged`

系统颜色值变化时触发，包括深色模式和强调色的改动。订阅该事件，就能实时更新应用的外观。

```csharp
event EventHandler<PlatformColorValues>? ColorValuesChanged;
```

下面的示例订阅颜色变化，并把新的主题变体记录到日志：

```csharp title="Responding to system color changes"
var platformSettings = myControl.GetPlatformSettings();
if (platformSettings is not null)
{
    platformSettings.ColorValuesChanged += (sender, values) =>
    {
        Debug.WriteLine($"Theme variant: {values.ThemeVariant}");
    };
}
```

## 另请参阅 {#see-also}

- [TopLevel](/docs/fundamentals/top-level)：从控件访问平台服务。
- [指针事件](/docs/input-interaction/pointer)：处理指针输入与手势。
- [手势](/docs/input-interaction/gestures)：处理轻点等手势事件。

