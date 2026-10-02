---
id: docker
title: Docker 容器
description: 如何在 Docker 容器中运行 Avalonia 应用：装好所需的 Linux 依赖，并备好虚拟显示器。
doc-type: how-to
---

要在 Docker 容器里运行 Avalonia 应用，需要安装 Avalonia 依赖的原生 Linux 库，并为渲染后端提供一个显示服务器（或虚拟帧缓冲）。

## 所需的包 {#required-packages}

Avalonia 在 Linux 上直接对接 X11，因此容器镜像里必须包含若干原生库，而默认的 .NET 运行时镜像并不自带这些库。

在 Dockerfile 中安装这些软件包（基于 Debian/Ubuntu 的镜像）：

```bash
apt-get update && apt-get install -y \
    libx11-6 \
    libice6 \
    libsm6 \
    libfontconfig1 \
    xvfb
```

| NuGet 包 | 用途 |
|---|---|
| `libx11-6` | X11 客户端库，Avalonia 通过它连接 X 显示服务器。 |
| `libice6` | 客户端间交换协议（ICE），X 会话必需。 |
| `libsm6` | X 会话管理协议。 |
| `libfontconfig1` | 字体发现与配置，文本渲染必需。 |
| `xvfb` | X 虚拟帧缓冲。没有接实体显示器时，用它提供一块虚拟显示区。 |

## 用 Xvfb 搭一块虚拟显示器 {#setting-up-a-virtual-display-with-xvfb}

Docker 容器没有实体显示器，而 Avalonia 渲染需要 X11 显示，因此必须运行 Xvfb 来创建虚拟帧缓冲。

在 Dockerfile 中设置 `DISPLAY` 环境变量：

```dockerfile
ENV DISPLAY=:99
```

然后在应用启动之前先把 Xvfb 跑起来。最简单的办法是写个入口脚本：

```bash title="entrypoint.sh"
#!/bin/bash
Xvfb :99 -screen 0 1920x1080x24 &

# Wait for Xvfb to be ready
sleep 1

exec "$@"
```

或者在应用代码里，于初始化 Avalonia 界面之前启动 Xvfb：

```csharp
var display = Environment.GetEnvironmentVariable("DISPLAY") ?? ":99";
var xvfb = Process.Start("Xvfb", new[] { display, "-screen", "0", "1920x1080x24" });

// Wait for the display to become available
var timeout = TimeSpan.FromSeconds(5);
var sw = Stopwatch.StartNew();
while (sw.Elapsed < timeout)
{
    // Try connecting to the display
    try
    {
        // If your app starts without error, the display is ready.
        break;
    }
    catch
    {
        Thread.Sleep(100);
    }
}
```

## 安装字体 {#installing-fonts}

精简版 Docker 镜像不含字体，没有字体时文字会渲染成一个个空白方块。请至少装一个字体族：

```dockerfile
RUN apt-get install -y fonts-noto fonts-ubuntu \
    && fc-cache -fv
```

## 完整的 Dockerfile 示例 {#complete-dockerfile-example}

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src
COPY ["MyApp/MyApp.csproj", "MyApp/"]
RUN dotnet restore "MyApp/MyApp.csproj"
COPY . .
WORKDIR /src/MyApp
RUN dotnet publish "MyApp.csproj" -c Release -o /app/publish \
    --runtime linux-x64 --self-contained true

FROM mcr.microsoft.com/dotnet/runtime:9.0 AS final

# Install Avalonia dependencies and Xvfb
RUN apt-get update && apt-get install -y \
    libx11-6 \
    libice6 \
    libsm6 \
    libfontconfig1 \
    xvfb \
    fonts-noto \
    && fc-cache -fv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:99

WORKDIR /app
COPY --from=build /app/publish .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["./MyApp"]
```

在 Dockerfile 旁边创建入口脚本：

```bash title="entrypoint.sh"
#!/bin/bash
Xvfb :99 -screen 0 1920x1080x24 &
sleep 1
exec "$@"
```

构建并运行：

```bash
docker build -t myapp .
docker run myapp
```

## 改用无头平台 {#using-the-headless-platform-instead}

如果你的容器根本不需要产出可见输出（比如跑自动化测试或生成图片），不妨改用[无头测试平台](/docs/testing/setting-up-the-headless-platform)。无头平台把窗口和渲染后端换成了纯内存实现，既不需要 X11 也不需要 Xvfb。

```csharp
public static AppBuilder BuildAvaloniaApp() => AppBuilder.Configure<App>()
    .UseSkia()
    .UseHeadless(new AvaloniaHeadlessPlatformOptions
    {
        UseHeadlessDrawing = false // set to true if you don't need pixel output
    });
```

这样容器镜像也更小，因为完全用不上 X11 相关软件包。

## 排查问题 {#troubleshooting}

### `libX11.so.6: cannot open shared object file`

缺少 `libx11-6` 包。请把它加进 Dockerfile：

```dockerfile
RUN apt-get update && apt-get install -y libx11-6
```

### 文字空白或完全不显示 {#blank-or-missing-text}

容器里没装字体。装一个字体包并重建字体缓存：

```dockerfile
RUN apt-get install -y fonts-noto && fc-cache -fv
```

### `Cannot open display`

Xvfb 没在运行，或者 `DISPLAY` 变量与 Xvfb 的显示编号对不上。请确认 Xvfb 在应用之前启动，且 `DISPLAY` 设成了同一个值（比如 `:99`）。

## 另请参阅 {#see-also}

- [部署到桌面 Linux](/docs/deployment/linux)：关于 `.deb` 打包
- [部署到嵌入式 Linux](/docs/deployment/embedded-linux)：关于 DRM/KMS 场景
- [桌面 Linux 平台集成](/docs/platform-specific-guides/linux)：关于 X11 依赖与 WSL 2
- [无头测试平台](/docs/testing/setting-up-the-headless-platform)：在完全没有显示服务器的环境下运行
