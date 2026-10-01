---
id: view-locator
title: 视图定位器
description: 用实现了 IDataTemplate 的 ViewLocator，为视图模型自动解析对应的视图。
doc-type: explanation
---

在 MVVM 应用中，视图模型只管应用逻辑，对界面一无所知。*视图定位器* 架起了这座桥：它为给定的视图模型自动找到正确的视图。当 Avalonia 在某个内容区域遇到一个视图模型对象时，就由视图定位器决定该创建并显示哪个视图。

:::info
ViewLocator 并非必需。用 XAML 中定义的 [DataTemplates](/docs/data-templates/data-template-collection) 也能达到同样效果。Avalonia 默认项目模板之所以带上 ViewLocator，只是为了方便 MVVM 应用。
:::

## 运作原理 {#how-it-works}

ViewLocator 实现了 [`IDataTemplate`](/api/avalonia/controls/templates/idatatemplate) 接口，也就是说它参与 Avalonia 标准的数据模板解析流程。当 [`ContentControl`](/api/avalonia/controls/contentcontrol) 之类的呈现器需要显示一个非控件对象时，就会去搜寻匹配的 `IDataTemplate`；注册过的 ViewLocator 会匹配上视图模型对象，并构建出相应的视图。

`IDataTemplate` 接口有两个成员：

- `Match(object data)` —— 若该模板能处理给定对象，则返回 `true`。
- `Build(object data)` —— 创建并返回用于显示的控件。

## 默认实现 {#default-implementation}

Avalonia 项目模板自带的 ViewLocator 走的是命名约定：把完全限定类型名中的 `"ViewModel"` 换成 `"View"`，再用反射解析出视图类型。

例如，`MyApp.ViewModels.MainViewModel` 会解析为 `MyApp.Views.MainView`。

```csharp
public class ViewLocator : IDataTemplate
{
    public Control Build(object data)
    {
        var name = data.GetType().FullName!.Replace("ViewModel", "View");
        var type = Type.GetType(name);

        if (type != null)
        {
            return (Control)Activator.CreateInstance(type)!;
        }

        return new TextBlock { Text = "Not Found: " + name };
    }

    public bool Match(object data)
    {
        return data is ViewModelBase;
    }
}
```

对任何继承自 `ViewModelBase` 的对象，`Match` 都返回 `true`。`Build` 用 `Activator.CreateInstance` 构造视图；若找不到对应的视图类型，则返回一个表示出错的 `TextBlock`。

:::tip
基于反射的做法上手方便，但它不兼容 Native AOT，也没有任何编译期安全保障。用于生产的应用，不妨考虑下面介绍的几种替代方案。
:::

## 注册视图定位器 {#registering-the-view-locator}

在 `App.axaml` 中注册你的 ViewLocator，让它在整个应用范围内可用：

```xml
<Application xmlns="https://github.com/avaloniaui"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             x:Class="MyApp.App"
             xmlns:local="using:MyApp"
             RequestedThemeVariant="Default">
    <Application.DataTemplates>
        <local:ViewLocator />
    </Application.DataTemplates>

    <Application.Styles>
        <FluentTheme />
    </Application.Styles>
</Application>
```

由于 `ViewLocator` 实现了 `IDataTemplate`，它就和你定义的其他数据模板一样，待在 `DataTemplates` 集合里。

## 使用视图定位器 {#using-the-view-locator}

注册之后，凡是视图模型作为内容出现的地方，视图定位器都会自动解析出视图。最常见的写法是用一个 `ContentControl` 绑定到视图模型属性：

```xml
<ContentControl Content="{Binding CurrentPage}" />
```

当 `CurrentPage` 被设为某个 `SettingsViewModel` 实例时，视图定位器会创建一个 `SettingsView` 并把它显示在 `ContentControl` 内部。把 `CurrentPage` 换成另一个视图模型，显示的视图也会随之自动切换。

也可以把视图模型直接设为窗口的 `DataContext`：

```csharp
DataContext = new MainViewModel(); // ViewLocator resolves MainView
```

## 其他做法 {#alternative-approaches}

默认那个基于反射的 ViewLocator 做原型够用，但有几处短板：无法在编译期确认视图是否存在、不支持 AOT，也没法给视图注入依赖。下面几种做法可以弥补这些不足。

### 模式匹配 {#pattern-matching}

用 C# 的模式匹配做显式类型映射，取代反射。这种做法兼容 AOT，也有编译期安全保障：

```csharp
public class ViewLocator : IDataTemplate
{
    public Control Build(object data)
    {
        return data switch
        {
            MainViewModel => new MainView(),
            SettingsViewModel => new SettingsView(),
            ProfileViewModel => new ProfileView(),
            _ => new TextBlock { Text = $"No view for {data.GetType().Name}" }
        };
    }

    public bool Match(object data) => data is ViewModelBase;
}
```

每加一个视图模型，就得往 `switch` 表达式里添一行。这是有意为之的取舍：用少量手工维护，换来编译期检查和 AOT 兼容。

### XAML 数据模板 {#xaml-data-templates}

你也可以完全不用 ViewLocator，直接在 XAML 中把「视图—视图模型」映射写成标准的数据模板：

```xml
<Application.DataTemplates>
    <DataTemplate DataType="{x:Type vm:MainViewModel}">
        <views:MainView />
    </DataTemplate>
    <DataTemplate DataType="{x:Type vm:SettingsViewModel}">
        <views:SettingsView />
    </DataTemplate>
</Application.DataTemplates>
```

这种做法用的是 Avalonia 内置的模板解析机制，一行自定义代码都不用写。模板匹配与搜索顺序的细节，请见[数据模板集合](/docs/data-templates/data-template-collection)。

### 依赖注入 {#dependency-injection}

当视图需要通过构造函数注入服务时，把模式匹配和 DI 容器结合起来：

```csharp
public class ViewLocator : IDataTemplate
{
    private readonly IServiceProvider _services;

    public ViewLocator(IServiceProvider services)
    {
        _services = services;
    }

    public Control Build(object data)
    {
        return data switch
        {
            MainViewModel => _services.GetRequiredService<MainView>(),
            SettingsViewModel => _services.GetRequiredService<SettingsView>(),
            _ => new TextBlock { Text = $"No view for {data.GetType().Name}" }
        };
    }

    public bool Match(object data) => data is ViewModelBase;
}
```

由于这个 ViewLocator 需要构造函数参数，请在代码中注册它，而不要写在 XAML 里：

```csharp
public override void OnFrameworkInitializationCompleted()
{
    var services = BuildServiceProvider();
    DataTemplates.Add(new ViewLocator(services));

    base.OnFrameworkInitializationCompleted();
}
```

服务提供程序的搭建方法，请见[依赖注入](/docs/app-development/dependency-injection)。

### 源生成器 {#source-generators}

对于手工维护映射已不现实的大型应用，可以用源生成器在编译期生成 ViewLocator 代码。这样既没有运行时开销，也完全兼容 AOT。

提供此类能力的社区包：

- **[StaticViewLocator](https://github.com/wieslawsoltes/StaticViewLocator)**：一个 NuGet 包，能自动发现并注册「视图—视图模型」配对。

想自己写源生成器，可参考 [Microsoft 的源生成器文档](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/source-generators-overview)。

## 该选哪种办法 {#choosing-an-approach}

| 办法 | 兼容 AOT | 编译期安全 | Supports DI | 维护成本 |
|---|---|---|---|---|
| 反射（默认） | No | No | No | None |
| 模式匹配 | Yes | Yes | Optional | 每个视图模型加一行 |
| XAML 数据模板 | Yes | Yes | No | 每个视图模型加一个模板 |
| 依赖注入 + 模式匹配 | Yes | Yes | Yes | 每个视图模型加一行 |
| 源生成器 | Yes | Yes | Varies | 无（自动生成） |

## 另请参阅 {#see-also}

- [数据模板入门](/docs/data-templates/introduction-to-data-templates)：Avalonia 如何挑选并套用数据模板。
- [数据模板集合](/docs/data-templates/data-template-collection)：按类型定义多个模板。
- [在代码中创建数据模板](/docs/data-templates/creating-data-templates-in-code)：实现 `IDataTemplate` 与使用 `FuncDataTemplate<T>`。
- [依赖注入](/docs/app-development/dependency-injection)：为应用配置服务注册。
