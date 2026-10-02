---
id: imageloader
title: ImageLoader
description: 把 Markdown.ImageLoader 设为一个 MarkdownImageLoader，即可定制 Markdown 控件加载和解析图片的方式。
doc-type: reference
tags:
  - avalonia pro
  - avalonia enterprise
---

`Markdown` 控件通过 `MarkdownImageLoader` 来解析图片 URL。在控件上设置 `Markdown.ImageLoader`，其文档中的每张图片就都会用上它。

:::info
该控件需要 [Avalonia Pro](https://avaloniaui.net/pricing) 或更高版本。
:::

## 默认表现 {#default-behavior}

默认没有设置任何加载器，所以在你提供一个之前，图片不会被加载。基类 `MarkdownImageLoader` 能解析 `http://`、`https://` 和 `file://` 三种方案，成功时返回 `IImage`，失败时返回 `null`。大多数常见场景下，直接把加载器赋上去即可，一行代码都不用写：

```xml
<Markdown Text="![Logo](https://example.com/logo.png)">
  <Markdown.ImageLoader>
    <MarkdownImageLoader />
  </Markdown.ImageLoader>
</Markdown>
```

若需要基类未覆盖的协议方案、图片格式、鉴权方式或缓存策略，就派生一个自己的加载器。

## 示例：加载 SVG 图片 {#example-loading-svg-images}

### 所需的包 {#required-packages}

要跑通下面这个自定义图片加载器的例子，你需要安装以下 NuGet 包：

```bash
 dotnet add package Avalonia.Svg.Skia
```

### Implementation

下面是一个支持 SVG 图片的自定义图片加载器示例：

```csharp
using Avalonia.Controls;
using Avalonia.Media.Imaging;
using Avalonia.Svg.Skia;
using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

public class CustomImageLoader : MarkdownImageLoader
{
    public override async Task<IImage?> LoadImageAsync(string url)
    {
        IImage? image = null;

        if (Uri.TryCreate(url, UriKind.Absolute, out var uri))
        {
            Stream? stream = null;

            if (uri.Scheme == "http" || uri.Scheme == "https")
            {
                stream = await DownloadImage(uri);
            }
            else if (uri.Scheme == "file" && File.Exists(uri.LocalPath))
            {
                stream = File.OpenRead(uri.LocalPath);
            }

            if (stream is null)
            {
                return null;
            }

            using (stream)
            {
                if (IsSvgFile(stream))
                {
                    var svg = new SvgImage
                    {
                        Source = SvgSource.LoadFromStream(stream)
                    };

                    image = svg;
                }
                else
                {
                    image = new Bitmap(stream);
                }
            }
        }

        return image;
    }

    private static async Task<Stream> DownloadImage(Uri url)
    {
        using var client = new HttpClient();
        using var response = await client.GetAsync(url).ConfigureAwait(false);
        using var stream = await response.Content.ReadAsStreamAsync().ConfigureAwait(false);
        var memoryStream = new MemoryStream();
        await stream.CopyToAsync(memoryStream).ConfigureAwait(false);
        memoryStream.Position = 0;
        return memoryStream;
    }

    private static bool IsSvgFile(Stream stream)
    {
        if (stream == null || stream.Length == 0)
            return false;
        try
        {
            const int bufferSize = 512;
            byte[] buffer = new byte[Math.Min(bufferSize, stream.Length)];
            int bytesRead = stream.Read(buffer, 0, buffer.Length);
            string header = Encoding.UTF8.GetString(buffer, 0, bytesRead);
            return header.Contains("<svg", StringComparison.OrdinalIgnoreCase);
        }
        catch
        {
            return false;
        }
        finally
        {
            stream.Position = 0;
        }
    }
}
```

## 用法 {#usage}

`Markdown.ImageLoader` 是附加属性，直接设置在控件上即可。

### XAML

```xml
<Window xmlns="https://github.com/avaloniaui"
        xmlns:local="using:MarkdownSample">
  <Markdown Text="![SVG Image](https://example.com/image.svg)">
    <Markdown.ImageLoader>
      <local:CustomImageLoader />
    </Markdown.ImageLoader>
  </Markdown>
</Window>
```

若要让多个控件共用一个加载器，请把它声明为资源，再让各控件都指向它：

```xml
<Window.Resources>
  <local:CustomImageLoader x:Key="ImageLoader" />
</Window.Resources>

<StackPanel>
  <Markdown Markdown.ImageLoader="{StaticResource ImageLoader}" Text="{Binding First}" />
  <Markdown Markdown.ImageLoader="{StaticResource ImageLoader}" Text="{Binding Second}" />
</StackPanel>
```

### Code

```csharp
var loader = new CustomImageLoader();

// Every image in this control's document uses it
markdown.ImageLoader = loader;

// Or through the static accessor, which takes any StyledElement
Markdown.SetImageLoader(markdown, loader);
```

若想让某张图片与众不同，可以在那个元素上设置 `MarkdownImage.ImageLoader`。写在单张图片上的取值会盖过控件给出的取值。

图片加载会一直推迟到 URL（由 Markdown 源码自动设置）和加载器两者都就位；之后再赋上加载器，文档中已有的图片也会重新解析。这样一来，文档模型就与图片解析解耦了。

## 适用场景 {#when-to-use}

只要默认的图片解析方式满足不了需求，你就该实现一个自定义的 `MarkdownImageLoader`。比如你可能需要渲染 SVG 图片、从需要鉴权的远程服务器加载图片，或是加一层缓存策略以免反复下载。自定义加载器让你完全掌控图片 URI 如何解析，以及 `Markdown` 控件能显示哪些图片类型。

## 另请参阅 {#see-also}

- [Markdown 控件](/controls/data-display/text-display/markdown)
- [CodeHighlighter](/controls/data-display/text-display/markdown/codehighlighter)