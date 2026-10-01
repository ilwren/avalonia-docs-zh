---
id: the-mvvm-pattern
title: MVVM 模式
description: 用 Model-View-ViewModel 模式配合数据绑定，把界面和逻辑分开。
doc-type: explanation
video:
  src: https://youtu.be/nD4d51p6ryg
  title: 详解 Avalonia MVVM —— 界面为什么会自动更新
---

import MvvmPatternDiagram from '/img/concepts/architecture/mvvm/mvvm-architecture.png';
import MvvmDataBindingDiagram from '/img/concepts/architecture/mvvm/mvvm.png';

MVVM（Model-View-ViewModel）模式把应用的用户界面和逻辑分开。它不再把显示代码和行为逻辑搅在同一个文件里，而是拆成三个彼此独立的部分，通过数据绑定互相通信。

<Image light={MvvmPatternDiagram} alt="Diagram showing the three components of the MVVM pattern: Model, View, and View Model." position="center" maxWidth={400} cornerRadius="true"/>

- **View（视图）**：用户所见内容的结构、布局与外观。在 Avalonia 中，视图用 AXAML 文件定义，代码隐藏尽量少写。视图通过绑定从视图模型取得数据。
- **ViewModel（视图模型）**：视图与模型之间的中介。它对外暴露供视图绑定的数据和命令，处理用户交互逻辑，并在数据变化时引发 `PropertyChanged` 事件通知视图。
- **Model（模型）**：应用的领域层，包含数据访问、业务逻辑与校验，比如仓储、数据传输对象和服务客户端。

视图知道视图模型，视图模型知道模型，反过来则不成立：模型不知道视图模型的存在，视图模型也不知道视图的存在。正是这条单向的依赖链，让每一层都可以独立测试、独立替换。

## 为什么要用 MVVM？ {#why-use-mvvm}

应用一旦变大，把界面定义和应用逻辑统统堆在代码隐藏文件里就会出问题：控件之间的交互纠缠不清，逻辑和界面平台耦合在一起，单元测试也无从下手。

MVVM 的解法是把应用逻辑挪进 POCO（Plain Old CLR Object）中，这些类不依赖 Avalonia，也不依赖任何界面框架。好处有：

- **可测试性**：视图模型可以像普通类一样做单元测试，不必启动界面。
- **关注点分离**：界面布局和应用逻辑各自演进。重新设计视图时不必碰视图模型。
- **与 XAML 天生契合**：Avalonia 的数据绑定系统负责把视图和视图模型连起来，MVVM 用在这里顺理成章。

## 什么时候该用 MVVM {#when-to-use-mvvm}

相比[代码隐藏](/docs/fundamentals/code-behind)的写法，MVVM 带来了额外的复杂度。对小而简单的应用来说，代码隐藏也许更好理解、更好维护。

有两种策略可供权衡：

1. 先用代码隐藏，等应用维护不动了再改造成 MVVM。
2. 如果预计应用会不断扩张，一开始就上 MVVM。

## Avalonia 中的 MVVM {#mvvm-in-avalonia}

### 视图与视图模型 {#views-and-view-models}

视图由一个 AXAML 文件及其代码隐藏实现，视图模型则是一个普通的 C#（或 F#）类。每个视图都有一个与之对应的视图模型，该视图的全部逻辑都放在里面。

视图由 Avalonia 的[内置控件](/controls)、[用户控件](/docs/fundamentals/ui-composition)，以及（可选的）你自己设计的[自定义控件](/docs/custom-controls)组合而成。

### 数据绑定 {#data-binding}

数据绑定是连接视图与视图模型的关键技术。可以把这层关系想象成两层结构，中间由绑定串起来：

<Image light={MvvmDataBindingDiagram} alt="Diagram showing data bindings connecting a view layer to a view model layer." position="center" maxWidth={400} cornerRadius="true"/>

有些绑定是双向的。比如文本输入框就是双向绑定：视图模型的变化会更新控件，用户的输入也会回流到视图模型。另一些绑定则是单向的，比如按钮的命令绑定只从视图流向视图模型。

由于视图模型既不引用视图、也不引用任何 Avalonia 类型，它可以像普通代码一样做单元测试。

### 模型层 {#the-model-layer}

模型代表界面之外的一切：数据存储、网络服务、业务规则。MVVM 并不规定模型层该怎么组织，但有一条原则很重要 —— 分离。请用依赖注入把模型服务提供给视图模型，而不要把它们硬绑在一起。

## 另请参阅 {#see-also}

- [Code-behind](/docs/fundamentals/code-behind)
- [界面组合](/docs/fundamentals/ui-composition)
- [数据绑定入门](/docs/data-binding/introduction-to-data-binding)
