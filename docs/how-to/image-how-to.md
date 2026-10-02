---
id: image-how-to
title: "操作指南：显示与处理图片"
description: 在 Avalonia 中从各种来源加载图片、处理纵横比，以及操作位图。
doc-type: how-to
---

本指南介绍 Image 控件的各种用法：从不同来源加载图片、处理纵横比、动态图片，以及位图操作。

## 从资产加载图片 {#loading-images-from-assets}

把图片作为嵌入资源放进项目，再用 `avares://` URI 方案引用它们：

```xml
<Image Source="avares://MyApp/Assets/logo.png" Width="200" />
```

确认 `.csproj` 中把该文件设成了 `AvaloniaResource`：

```xml
<ItemGroup>
    <AvaloniaResource Include="Assets\**" />
</ItemGroup>
```

## 从文件路径加载图片 {#loading-images-from-a-file-path}

绑定到一个从磁盘读入的 `Bitmap`：

```csharp
[ObservableProperty]
private Bitmap? _photo;

[RelayCommand]
private async Task LoadPhoto()
{
    var topLevel = TopLevel.GetTopLevel(App.Current?.ApplicationLifetime
        is IClassicDesktopStyleApplicationLifetime desktop ? desktop.MainWindow : null);
    if (topLevel is null) return;

    var files = await topLevel.StorageProvider.OpenFilePickerAsync(
        new FilePickerOpenOptions
        {
            Title = "Select an image",
            FileTypeFilter = new[] { FilePickerFileTypes.ImageAll }
        });

    if (files.Count > 0)
    {
        await using var stream = await files[0].OpenReadAsync();
        Photo = new Bitmap(stream);
    }
}
```

```xml
<Image Source="{Binding Photo}" MaxWidth="400" />
```

## 从 URL 加载图片 {#loading-images-from-a-url}

使用 `AsyncImageLoader`，或者在视图模型中加载位图：

```csharp
[RelayCommand]
private async Task LoadFromUrl(string url)
{
    using var client = new HttpClient();
    var bytes = await client.GetByteArrayAsync(url);
    using var stream = new MemoryStream(bytes);
    Photo = new Bitmap(stream);
}
```

## Stretch Modes

[`Stretch`](/api/avalonia/media/stretch) 属性控制图片如何填满自己的边界：

```xml
<!-- Preserves aspect ratio, fits within bounds -->
<Image Source="{Binding Photo}" Stretch="Uniform" />

<!-- Fills the entire area, may crop -->
<Image Source="{Binding Photo}" Stretch="UniformToFill" />

<!-- Stretches to fill, ignores aspect ratio -->
<Image Source="{Binding Photo}" Stretch="Fill" />

<!-- No scaling, displays at original size -->
<Image Source="{Binding Photo}" Stretch="None" />
```

| 拉伸方式 | 说明 |
|---|---|
| `Uniform` | 等比缩放至完整装入（默认）。 |
| `UniformToFill` | 等比缩放至填满，必要时裁掉溢出部分。 |
| `Fill` | 拉伸至恰好填满，不管纵横比。 |
| `None` | 按原始像素尺寸显示。 |

## Circular Image (Avatar)

用 `Clip` 把图片裁成圆形：

```xml
<Border CornerRadius="50" ClipToBounds="True"
        Width="100" Height="100">
    <Image Source="{Binding Avatar}" Stretch="UniformToFill" />
</Border>
```

## 带回退的图片 {#image-with-fallback}

没有图片可用时显示一个占位内容：

```xml
<Panel Width="200" Height="200">
    <!-- Fallback shown when Source is null -->
    <Border Background="#F3F4F6" IsVisible="{Binding Photo, Converter={x:Static ObjectConverters.IsNull}}">
        <TextBlock Text="No Image" HorizontalAlignment="Center" VerticalAlignment="Center"
                   Foreground="Gray" />
    </Border>
    <Image Source="{Binding Photo}" Stretch="Uniform" />
</Panel>
```

## Image Interpolation

控制图片被缩放时的渲染质量：

```xml
<!-- Sharp pixels for pixel art -->
<Image Source="{Binding PixelArt}"
       RenderOptions.BitmapInterpolationMode="None" />

<!-- Smooth scaling for photos -->
<Image Source="{Binding Photo}"
       RenderOptions.BitmapInterpolationMode="HighQuality" />
```

| 模式 | 说明 |
|---|---|
| `None` | 最近邻，像素锐利。 |
| `LowQuality` | 双线性过滤。 |
| `MediumQuality` | 双线性，并略作改进。 |
| `HighQuality` | 双三次或高质量重采样。 |
| `Default` | 平台默认值。 |

## DrawingImage (Vector Graphics)

分辨率无关的矢量图请用 `DrawingImage`：

```xml
<Image Width="48" Height="48">
    <Image.Source>
        <DrawingImage>
            <GeometryDrawing Brush="Red"
                             Geometry="M12,21.35L10.55,20.03C5.4,15.36 2,12.27 2,8.5
                                       C2,5.41 4.42,3 7.5,3C9.24,3 10.91,3.81 12,5.08
                                       C13.09,3.81 14.76,3 16.5,3C19.58,3 22,5.41 22,8.5
                                       C22,12.27 18.6,15.36 13.45,20.03L12,21.35Z" />
        </DrawingImage>
    </Image.Source>
</Image>
```

## PathIcon

简单的单色图标请用 `PathIcon`，而不是 `Image`：

```xml
<PathIcon Data="{StaticResource home_regular}" Width="24" Height="24"
          Foreground="{DynamicResource SystemAccentColor}" />
```

PathIcon 会从父级样式继承 `Foreground`，因此很容易纳入主题。

## RenderTargetBitmap (Screenshots)

把一个控件截取成位图：

```csharp
var renderTarget = new RenderTargetBitmap(new PixelSize(800, 600));
renderTarget.Render(myControl);
renderTarget.Save("screenshot.png");
```

目标控件必须已附加到可见窗口上。若想不显示窗口就完成渲染，请使用启用了 Skia 渲染器的[无头平台](/docs/testing/setting-up-the-headless-platform#visual-regression-testing)。

## Key Properties

| 属性 | 类型 | 说明 |
|---|---|---|
| `Source` | `IImage` | 要显示的图像（`Bitmap`、`DrawingImage` 之类）。 |
| `Stretch` | `Stretch` | 图片如何填满自己的边界。 |
| `StretchDirection` | `StretchDirection` | `Both`, `UpOnly`, `DownOnly`. |

## See Also

- [Image 控件参考](/controls/media/image)：属性表。
- [PathIcon 控件参考](/controls/media/pathicon)：矢量图标控件。
- [DrawingImage 控件参考](/controls/media/drawingimage)：矢量图像源。
- [如何绑定图片文件](/docs/data-binding/how-to-bind-image-files)：在数据模板中绑定图片。
- [图像插值](/docs/graphics-animation/image-interpolation)：位图的渲染质量。
- [资产](/docs/fundamentals/including-assets)：资产加载与 URI 方案。
