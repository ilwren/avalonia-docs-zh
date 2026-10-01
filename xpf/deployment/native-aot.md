---
id: native-aot
title: Native AOT
description: 用预先编译（AOT）把 XPF 应用发布为本机可执行文件，内含裁剪要求与 XAML 类型保留的注意事项。
doc-type: how-to
---

XPF 支持 Native AOT（预先编译）。与 WPF 不同，XPF 不使用 COM 封送，因此能与 AOT 编译相容。即便是用了第三方控件库的大型应用，也能成功地用 Native AOT 编出来。

## 项目配置 {#project-configuration}

在你的 `.csproj` 中加上 `PublishAot`。

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

## Native AOT 链接器的裁剪 {#trimming-by-the-native-aot-linker}

要在 XPF 上用 AOT，裁剪和链接都得保守些。

XPF SDK 默认自带一份 `rd.xml` 根描述符，会强制保留 XPF 运行时库，其中包括所有内置的 WPF 程序集，以及设置了 `Xpf.Sdk` 的用户可执行程序集。

不过，若你的应用引用了第三方 WPF 库，它们也得有相应的裁剪配置；否则 Native AOT 链接器会把那些只在 XAML 中被引用的类型剪掉——它看不出这些类型其实在用。

若运行时因缺少类型而报错，先看看你是不是用了某些不带根描述符的第三方库。给它们在 `.csproj` 文件中补上根描述符即可。

```xml title=".csproj"
<ItemGroup>
    <ProjectReference Include="..\YourAssembly\YourAssembly.csproj" />
    <TrimmerRootAssembly Include="YourAssembly" />
</ItemGroup>
```

相关说明请参阅 .NET 官方文档站上的[裁剪](https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/prepare-libraries-for-trimming#csproj-file)。

## 另请参阅 {#see-also}

- [Native AOT（Avalonia）](/docs/deployment/native-aot)：标准 Avalonia 应用的 AOT 配置
- [Windows Deployment](/xpf/deployment/windows)
- [macOS Deployment](/xpf/deployment/macos)
- [Linux Deployment](/xpf/deployment/linux)
- [Performance Optimization](/xpf/configuration/performance)
