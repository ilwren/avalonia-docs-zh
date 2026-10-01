---
id: embed-native-views
title: 嵌入 Android 原生视图
description: 了解如何借助 NativeControlHost 和 AndroidViewControlHandle，把 WebView、Button 等 Android 原生视图嵌入 Avalonia 应用。
doc-type: how-to
---

通过继承 [`NativeControlHost`](/api/avalonia/controls/nativecontrolhost)，你可以把 Android 原生视图嵌进 Avalonia 的视觉树：把每个 Android `View` 包进一个 [`AndroidViewControlHandle`](/api/avalonia/android/androidviewcontrolhandle)，再从 `CreateNativeControlCore` 返回即可。当你需要 Avalonia 没有对应物的平台专属控件（比如 `WebView`、`MapView` 或媒体播放器）时，这招就派上用场了。

## 运作原理 {#how-it-works}

`NativeControlHost` 会在 Avalonia 布局中占出一块地方，并把这块区域的渲染交给原生平台。在 Android 上，你需要：

1. 在 `NativeControlHost` 的子类中重写 `CreateNativeControlCore`。
2. 借助 `parent` 句柄中的父级 context，创建你所需的 Android 原生 `View`。
3. 把该 `View` 包进 `AndroidViewControlHandle` 并返回。

Avalonia 会摆放并裁剪这个原生视图，使其与宿主控件的边界吻合。

## 获取父级 context {#getting-the-parent-context}

传给 `CreateNativeControlCore` 的 `parent` 参数是一个 `IPlatformHandle`。在 Android 上，你可以把它转成 `AndroidViewControlHandle` 以取得 `View.Context`；若转换失败，就退而使用全局的 application context：

```csharp
var parentContext = (parent as AndroidViewControlHandle)?.View.Context
    ?? global::Android.App.Application.Context;
```

## 示例：嵌入 WebView 和 Button {#example-embedding-a-webview-and-a-button}

下面的示例演示了一个实现 `INativeDemoControl` 接口的类，它会根据参数创建两种 Android 原生控件之一。

:::tip
本示例取自 Avalonia 仓库中的 [ControlCatalog.Android 示例](https://github.com/AvaloniaUI/Avalonia/blob/master/samples/ControlCatalog.Android/EmbedSample.Android.cs)。
:::

首先，定义共享代码用来请求原生控件的接口：

```csharp
public interface INativeDemoControl
{
    IPlatformHandle CreateControl(
        bool isSecond,
        IPlatformHandle parent,
        Func<IPlatformHandle> createDefault);
}
```

然后在 Android 项目里实现它：

```csharp
public class EmbedSampleAndroid : INativeDemoControl
{
    public IPlatformHandle CreateControl(
        bool isSecond,
        IPlatformHandle parent,
        Func<IPlatformHandle> createDefault)
    {
        var parentContext = (parent as AndroidViewControlHandle)?.View.Context
            ?? global::Android.App.Application.Context;

        if (isSecond)
        {
            var webView = new global::Android.Webkit.WebView(parentContext);
            webView.LoadUrl("https://www.android.com/");
            return new AndroidViewControlHandle(webView);
        }

        var button = new global::Android.Widget.Button(parentContext)
        {
            Text = "Hello world"
        };

        var clickCount = 0;
        button.Click += (sender, args) =>
        {
            clickCount++;
            button.Text = $"Click count {clickCount}";
        };

        return new AndroidViewControlHandle(button);
    }
}
```

当 `isSecond` 为 `true` 时，该方法会创建一个 Android `WebView`、加载某个 URL，并把它包进 `AndroidViewControlHandle` 返回；当 `isSecond` 为 `false` 时，则创建一个带点击计数的原生 `Button` 并返回。

## 限制 {#limitations}

原生视图位于 Avalonia 渲染表面之上。请记住以下限制：

- **不能透明**：原生视图无法使用透明背景来透出其后方的 Avalonia 内容。
- **不受变换影响**：Avalonia 的渲染变换（旋转、缩放）对原生视图不起作用。
- **Z 序限制**：原生视图始终渲染在 Avalonia 内容之上，你无法把 Avalonia 控件叠在原生视图上面。
- **裁剪**：原生视图会被裁剪到宿主边界之内，但不支持复杂的裁剪几何。

## 另请参阅 {#see-also}

- [原生平台互操作](/docs/app-development/native-interop)
- [用 Avalonia 开发 Android 应用](/docs/platform-specific-guides/android)
- [在 Android 上部署](/docs/deployment/android)

