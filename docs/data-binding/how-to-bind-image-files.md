---
id: how-to-bind-image-files
title: 如何绑定图片文件
description: 把来自文件路径、资源或流的图片源绑定到 Avalonia 控件上显示。
doc-type: how-to
---


<GitHubSampleLink title="Loading Images" link="https://github.com/AvaloniaUI/AvaloniaUI.QuickGuides/tree/main/LoadingImages"/>


在 Avalonia UI 中，绑定图片文件为应用展示动态图像内容打开了方便之门。本文概览如何绑定来自不同来源的图片文件。

## 绑定来自不同来源的图片文件 {#binding-to-image-files-from-different-sources}

假设你有若干来自不同来源的图片（比如本地资源或网络 URL）想在视图中展示，可以这样做：

首先在 `ViewModel` 中定义若干属性来表示这些图片源。属性类型可以是 `Bitmap`，也可以是 `Task<Bitmap>`（如果加载图片涉及异步操作）。加载工作由 `ImageHelper` 类完成。

```csharp
public class MainWindowViewModel : ViewModelBase
{
    public Bitmap? ImageFromBinding { get; } = ImageHelper.LoadFromResource(new Uri("avares://LoadingImages/Assets/abstract.jpg"));
    public Task<Bitmap?> ImageFromWebsite { get; } = ImageHelper.LoadFromWeb(new Uri("https://upload.wikimedia.org/wikipedia/commons/4/41/NewtonsPrincipia.jpg"));
}
```

你还需要一个辅助类 `ImageHelper`，提供从资源和网络 URL 加载图片的方法。实现如下：

```csharp
using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using Avalonia;
using Avalonia.Media.Imaging;
using Avalonia.Platform;

namespace ImageExample.Helpers
{
    public static class ImageHelper
    {
        public static Bitmap LoadFromResource(Uri resourceUri)
        {
            return new Bitmap(AssetLoader.Open(resourceUri));
        }

        public static async Task<Bitmap?> LoadFromWeb(Uri url)
        {
            using var httpClient = new HttpClient();
            try
            {
                var response = await httpClient.GetAsync(url);
                response.EnsureSuccessStatusCode();
                var data = await response.Content.ReadAsByteArrayAsync();
                return new Bitmap(new MemoryStream(data));
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine($"An error occurred while downloading image '{url}' : {ex.Message}");
                return null;
            }
        }
    }
}
```

`LoadFromResource` 方法接收一个资源 URI，用 Avalonia 提供的 `AssetLoader` 类加载图片；`LoadFromWeb` 方法则用 `HttpClient` 类从网络 URL 加载图片。

随后在视图中把这些图片源绑定到 `Image` 控件上：

```xml
<Grid ColumnDefinitions="*,*,*" RenderOptions.BitmapInterpolationMode="HighQuality">
    <Image Grid.Column="0" Source="avares://LoadingImages/Assets/abstract.jpg" MaxWidth="300" />
    <Image Grid.Column="1" Source="{Binding ImageFromBinding}" MaxWidth="300" />
    <Image Grid.Column="2" Source="{Binding ImageFromWebsite^}" MaxWidth="300" />
</Grid>
```

`Image` 控件的 `Source` 属性可以接受多种图片源，包括文件路径、URL 和资源。请注意，对于异步图片源，必须在绑定表达式后面加上 `^` 字符，以告知 Avalonia 这是一个异步绑定。

请确认本地图片路径准确无误、文件可访问；如果图片属于应用资源，还要确认它已正确包含进项目。绑定网络图片时，则要确认 URL 可达。

## 另请参阅 {#see-also}

- [如何绑定到任务结果](/docs/data-binding/how-to-bind-to-a-task-result)：用 `^` 运算符异步加载数据。
- [数据绑定语法](/docs/data-binding/data-binding-syntax)：绑定路径、模式与转换器。









