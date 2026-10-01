---
id: native-aot
title: Native AOT
description: Publish XPF applications as native executables using ahead-of-time compilation, including trimming requirements and XAML type preservation.
doc-type: how-to
---

Native AOT (Ahead-of-Time) compilation is supported in XPF. Unlike WPF, XPF does not use COM marshalling, which allows it to be compatible with AOT compilation. Large applications using third-party control libraries can be successfully compiled with Native AOT.

## 项目配置 {#project-configuration}

Add `PublishAot` to your `.csproj`.

```xml
<PropertyGroup>
    <PublishAot>true</PublishAot>
</PropertyGroup>
```

## 发布 {#publishing}

在命令行运行 `dotnet publish` 即可发布应用：

```
dotnet publish -r <runtime> -c Release
```

举例来说，`dotnet publish -r osx-arm64 -c Release` 会为 Apple Silicon 设备发布应用。

更多信息请参阅 .NET 官方文档站上的 [Native AOT 部署](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/?tabs=windows%2Cnet8#publish-native-aot-using-the-cli)和 [dotnet publish](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-publish)。

## Trimming by the Native AOT linker

To use AOT with XPF, trimming and linking must be conservative.

By default, the XPF SDK ships with an `rd.xml` root descriptor that force-includes XPF runtime libraries, including all built-in WPF assemblies and any user-executable assemblies on which `Xpf.Sdk` is set.

However, if your application references third-party WPF libraries, they must have equivalent trimming configurations. Otherwise, the Native AOT linker may remove types that are only referenced from XAML, which it cannot detect as being in use.

If you are experiencing runtime errors due to missing types, check if you are using any third-party libraries that do not ship with a root descriptor. Add a root descriptor for these to your `.csproj` file.

```xml title=".csproj"
<ItemGroup>
    <ProjectReference Include="..\YourAssembly\YourAssembly.csproj" />
    <TrimmerRootAssembly Include="YourAssembly" />
</ItemGroup>
```

相关说明请参阅 .NET 官方文档站上的[裁剪](https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/prepare-libraries-for-trimming#csproj-file)。

## 另请参阅 {#see-also}

- [Native AOT (Avalonia)](/docs/deployment/native-aot): AOT setup for standard Avalonia applications
- [Windows Deployment](/xpf/deployment/windows)
- [macOS Deployment](/xpf/deployment/macos)
- [Linux Deployment](/xpf/deployment/linux)
- [Performance Optimization](/xpf/configuration/performance)
