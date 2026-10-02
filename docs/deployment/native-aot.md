---
id: native-aot
title: Native AOT
description: 用提前编译（AOT）把 Avalonia 应用发布为原生可执行程序。
doc-type: how-to
---

Native AOT（提前编译）让你能把 Avalonia 应用发布成自包含的可执行程序，并获得原生级的性能表现。本指南讲的是 Native AOT 部署中与 Avalonia 相关的注意事项和配置方法。

## 它能给 Avalonia 应用带来什么 {#benefits-for-avalonia-applications}

对 Avalonia 应用而言，Native AOT 编译有这些好处：

- 启动更快，这对桌面应用尤其受用
- 内存占用更低，适合资源吃紧的环境
- 自包含部署，目标机上无需安装 .NET 运行时
- 攻击面更小（没有 JIT 编译），安全性更好
- 配合裁剪使用时，分发体积更小

## 为 Avalonia 配置 Native AOT {#setting-up-native-aot-for-avalonia}

### 项目配置 {#project-configuration}

把下面的内容加进你的 `.csproj` 文件。

```xml
<PropertyGroup>
    <!-- Only needed for the main executable project -->
    <PublishAot>true</PublishAot>

    <!-- Add to all projects/libraries in use, to ensure AOT compatibility -->
    <IsAotCompatible>true</IsAotCompatible>

    <!-- Necessary before Avalonia 12.0, was used for accessiblity APIs -->
    <BuiltInComInteropSupport>false</BuiltInComInteropSupport>
</PropertyGroup>
```

相关说明请参阅 .NET 官方文档站上的 [Native AOT 部署](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/)。

## 与 Avalonia 相关的注意事项 {#avalonia-specific-considerations}

### XAML 加载 {#xaml-loading}
使用 Native AOT 时，XAML 会在构建期编译进应用。请确保你：
- 在 XAML 文件中使用 `x:CompileBindings="True"`
- 不要在运行时动态加载 XAML
- 尽可能用静态资源引用，而不是动态资源

### 资产与资源 {#assets-and-resources}
- 把所有资产都作为嵌入资源打包
- 资产使用 `AvaloniaResource` 生成操作
- 不要从外部来源动态加载资产

### 视图模型与依赖注入 {#view-models-and-dependency-injection}
- 在启动时注册你的视图模型
- 采用编译期的 DI 配置
- 不要用基于反射的服务定位

## 发布 Avalonia 的 Native AOT 应用 {#publishing-avalonia-native-aot-applications}

在命令行运行 `dotnet publish` 即可发布应用：

```
dotnet publish -r <runtime> -c Release
```

举例来说，`dotnet publish -r osx-arm64 -c Release` 会为 Apple Silicon 设备发布应用。

更多信息请参阅 .NET 官方文档站上的 [Native AOT 部署](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/?tabs=windows%2Cnet8#publish-native-aot-using-the-cli)和 [dotnet publish](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-publish)。

:::tip
之后你可以用苹果的 [lipo 工具](https://developer.apple.com/documentation/apple-silicon/building-a-universal-macos-binary)把 Intel 和 Apple Silicon 两份二进制合二为一，从而发布通用二进制（Universal binary）。
:::

## 解决反射相关的错误 {#resolving-reflection-related-errors}

在你的 `.csproj` 文件中添加裁剪器根描述符。

```xml title=".csproj"
<ItemGroup>
    <ProjectReference Include="..\YourAssembly\YourAssembly.csproj" />
    <TrimmerRootAssembly Include="YourAssembly" />
</ItemGroup>
```

相关说明请参阅 .NET 官方文档站上的[裁剪](https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/prepare-libraries-for-trimming#csproj-file)。

## 已知限制 {#known-limitations}

在 Avalonia 中使用 Native AOT 时，请留意这些限制：
- 动态创建控件必须在裁剪器设置中作相应配置
- 部分第三方 Avalonia 控件可能不兼容 AOT
- 平台专属功能需要显式配置
- 设计时工具中的实时预览可能受限

## 平台支持 {#platform-support}

平台支持情况请参阅[平台/架构限制](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/#platformarchitecture-restrictions)。

## Avalonia XPF

若你使用 [Avalonia XPF](/xpf)，它同样支持 Native AOT。XPF 下的配置和用法请参阅 [XPF：Native AOT](/xpf/deployment/native-aot)。

## 另请参阅 {#see-also}

- [Native AOT 部署](https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/?tabs=windows%2Cnet9plus#platformarchitecture-restrictions)：微软关于 Native AOT 的文档。
- [使用 Native AOT 的 Avalonia 示例应用](https://github.com/AvaloniaUI/Avalonia.Samples)：示例项目。
