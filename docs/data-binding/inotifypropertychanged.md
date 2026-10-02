---
id: inotifypropertychanged
title: 如何使用 INotifyPropertyChanged
description: 实现 INotifyPropertyChanged，在视图模型属性变化时通知界面。
doc-type: how-to
---

## 引言 {#introduction}
`INotifyPropertyChanged` 接口是 MVVM（Model-View-ViewModel）设计模式中的关键一环，有了它才谈得上可扩展、好维护的应用。它负责在属性发生变化时发出通知，视图据此自动更新，应用各组件之间的沟通也因此顺畅起来。

## 什么是 INotifyPropertyChanged？ {#what-is-inotifypropertychanged}

`INotifyPropertyChanged` 是 .NET 提供的一个接口，类实现它之后就能对外宣告「某个属性的值变了」。这在数据绑定场景中尤其有用 —— 绑定的数据一变，界面就能自动刷新。

`INotifyPropertyChanged` 接口只有一个事件成员 `PropertyChanged`。当属性值发生变化时，对象引发 `PropertyChanged` 事件，告知所有绑定到它的元素。

## 为什么 INotifyPropertyChanged 对 MVVM 这么重要？ {#why-is-inotifypropertychanged-important-in-mvvm}
在 MVVM 模式中，ViewModel 封装了视图的交互逻辑，也封装了来自 Model 的数据。视图绑定到 ViewModel 的属性上，而 ViewModel 又把 Model 对象中的数据暴露出来。

要让 MVVM 模式真正跑起来，底层数据一变，视图就得跟着更新 —— 这正是 `INotifyPropertyChanged` 的用武之地。在 ViewModel 中实现这个接口，就能把 Model 的变化通知给视图，界面随之自动刷新。

## Implementing INotifyPropertyChanged
下面是实现 `INotifyPropertyChanged` 的一个例子：

```csharp
public class MyViewModel : INotifyPropertyChanged
{
    private string _name;

    public string Name
    {
        get { return _name; }
        set
        {
            _name = value;
            OnPropertyChanged(nameof(Name));
        }
    }

    public event PropertyChangedEventHandler PropertyChanged;

    protected virtual void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
```

在这段代码中，每当 `Name` 属性被赋上新值，`OnPropertyChanged` 方法就会被调用，进而引发 `PropertyChanged` 事件。所有绑定到该属性的界面元素都会随之更新，显示出新值。

## 用 MVVM Toolkit 简化 INotifyPropertyChanged {#using-mvvm-toolkit-to-simplify-inotifypropertychanged}
实现 `INotifyPropertyChanged` 本身不算复杂，但 ViewModel 里属性一多就相当啰嗦。好在 .NET Community Toolkit 的 MVVM 库借助源生成器，用 `ObservableObject` 基类加 `[ObservableProperty]` 特性，提供了实现 `INotifyPropertyChanged` 的更高效写法。

下面是用 `ObservableObject` 达成同样效果的写法：

```csharp
using CommunityToolkit.Mvvm.ComponentModel;

public partial class MyViewModel : ObservableObject
{
    [ObservableProperty]
    private string _name;
}
```

这段代码中，`ObservableObject` 类实现了 `INotifyPropertyChanged`，而 `[ObservableProperty]` 特性用来标明 `_name` 是一个可观察属性。源生成器会在幕后生成必要的样板代码，包括该属性的 getter 和 setter，并在属性变化时自动调用 `OnPropertyChanged` 方法。这样实现起来更清爽，也更不容易出错。

MVVM Toolkit 提供了一整套工具，帮你简化 .NET 应用中 MVVM 模式的落地，`INotifyPropertyChanged` 的使用只是其中之一。借助源生成器，代码在保持同样功能的前提下更高效、也更易读。

## 另请参阅 {#see-also}

- [MVVM 模式](/docs/fundamentals/the-mvvm-pattern)：MVVM 架构模式入门。
- [数据校验](/docs/data-binding/binding-validation)：用 INotifyDataErrorInfo 在数据绑定中做校验。
- [数据绑定入门](/docs/data-binding/introduction-to-data-binding)：数据绑定总览。







