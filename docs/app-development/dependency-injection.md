---
id: dependency-injection
title: 实现依赖注入
description: 用 Microsoft.Extensions.DependencyInjection 在 Avalonia 应用中搭建依赖注入。
doc-type: how-to
---

[依赖注入（DI）](https://en.wikipedia.org/wiki/Dependency_injection)能让代码更干净、更模块化、更好测试。做法是把功能拆成一个个独立的服务，按需创建并传递。

本指南介绍如何在 Avalonia 中结合 [Model-View-ViewModel（MVVM）模式](/docs/fundamentals/the-mvvm-pattern)使用依赖注入。

## 前置条件 {#prerequisites}

- 一个 Avalonia 项目
- .NET 8.0 SDK 或更高版本（推荐 .NET 10）

## 第 0 步：背景与初始代码 {#step-0-context-and-initial-code}

假设你的应用里有 `MainViewModel`、`BusinessService` 和 `Repository`。`MainViewModel` 依赖 `IBusinessService`，而 `BusinessService` 依赖 `IRepository`。

<Tabs>

<TabItem value="mainviewmodel" label="MainViewModel">

```csharp
public partial class MainViewModel
{
    private readonly IBusinessService _businessService;

    public MainViewModel(IBusinessService businessService)
    {
        _businessService = businessService;
    }
}
```

</TabItem>

<TabItem value="businessservice" label="BusinessService">

```csharp
public class BusinessService : IBusinessService
{
    private readonly IRepository _repository;

    public BusinessService(IRepository repository)
    {
        _repository = repository;
    }
}
```

</TabItem>

<TabItem value="repository" label="Repository">

```csharp
public class Repository : IRepository
{
}
```

</TabItem>

</Tabs>

传统做法是直接实例化 `Repository`，把它传给 `BusinessService`，再传给 `MainViewModel`，就像这样：

```csharp
var window = new MainWindow
{
    DataContext = new MainViewModel(new BusinessService(new Repository()))
}
```

对于那些简单、不常用、也基本不变的构造函数，这种写法很常见。但随着复杂度上升，它就不太撑得住了，原因在于：

- 构造函数的依赖越多，你要实例化并传入的东西就越多。在构造函数里就地创建依赖（比如 `new MainViewModel(new MyService())`）会把代码牢牢绑死在某个具体的依赖实例上。
- 如果 `MainViewModel` 的构造函数自己创建依赖，它就还会跟依赖的创建过程耦合在一起。
- 如果 `MainViewModel` 在很多地方都被实例化，那么一旦依赖发生变化，_每一处_ `MainViewModel` 的实例化代码都得改。

依赖注入把对象及其依赖的创建过程抽象出去，从而解决了这个问题。于是服务得以良好封装，并被自动注入到任何注册使用它们的服务中。

## 第 1 步：安装 DI 的 NuGet 包 {#step-1-install-the-nuget-package-for-di}

可选的 DI 容器有很多（比如 [DryIoC](https://github.com/dadhi/DryIoc)、[Autofac](https://github.com/autofac/Autofac)、[Pure.DI](https://github.com/DevTeam/Pure.DI)），但本指南聚焦于 `Microsoft.Extensions.DependencyInjection`——一个轻量、可扩展的 DI 容器。它以约定优先的方式为 .NET 应用（Avalonia 应用自然也包括在内）引入依赖注入。

在项目目录下执行下面的命令，即可安装 DI 包。

```shell
dotnet add package Microsoft.Extensions.DependencyInjection
```

## Step 2: Add `ServiceCollectionExtensions`

下面这段代码为 `IServiceCollection` 写了一个扩展方法，把各个服务注册到服务集合中，供注入使用。

```csharp
public static class ServiceCollectionExtensions
{
    public static void AddCommonServices(this IServiceCollection collection)
    {
        collection.AddSingleton<IRepository, Repository>();
        collection.AddTransient<BusinessService>();
        collection.AddTransient<MainViewModel>();
    }
}
```

## Step 3: Modify `App.axaml.cs`

修改 `App.axaml.cs` 以使用 DI 容器，这样上一步注册的视图模型就能由容器解析出来。解析完成的视图模型随后可以赋给 `MainWindow`/`MainView` 的数据上下文。

```csharp
public class App : Application
{
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        // Register all the services needed for the application to run
        var collection = new ServiceCollection();
        collection.AddCommonServices();

        // Creates a ServiceProvider containing services from the provided IServiceCollection
        var services = collection.BuildServiceProvider();

        var vm = services.GetRequiredService<MainViewModel>();
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.MainWindow = new MainWindow
            {
                DataContext = vm
            };
        }
        else if (ApplicationLifetime is ISingleViewApplicationLifetime singleViewPlatform)
        {
            singleViewPlatform.MainView = new MainView
            {
                DataContext = vm
            };
        }

        base.OnFrameworkInitializationCompleted();
    }
}
```

## 第 4 步：验证结果 {#step-4-verify-the-result}

运行应用。如果 DI 容器配置无误，你会看到 `MainWindow`（或 `MainView`）出现，其 `DataContext` 已被设为一个完整解析出来的 `MainViewModel` 实例，依赖也全部注入到位。

## 另请参阅 {#see-also}

- [数据绑定](/docs/data-binding/introduction-to-data-binding)：把视图模型绑定到视图。
- [MVVM 架构](/docs/fundamentals/the-mvvm-pattern)：在 Avalonia 中运用 MVVM 模式。
