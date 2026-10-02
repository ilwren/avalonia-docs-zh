---
id: routed-events
title: 路由事件
---

import InputEventRoutingDiagram from '/img/concepts/ui-concepts/user-input/pointer-pressed-routing.png';

Avalonia 中多数事件都实现为路由事件。所谓路由事件，是指事件不只在引发它的那个控件上触发，而是在整棵树上传递。

## 什么是路由事件？ {#what-is-a-routed-event}

一个典型的 Avalonia 应用含有许多元素。无论是用代码创建还是在 XAML 中声明，这些元素都处在一棵元素树中，彼此的关系由这棵树表达。事件路由的方向有两种，取决于事件本身的定义；但一般来说，路由从源元素出发，沿元素树一路向上「冒泡」，直到抵达树的根（通常是一个页面或窗口）。若你接触过 HTML DOM，想必对冒泡这个概念不陌生。

### 路由事件要解决的主要场景 {#top-level-scenarios-for-routed-events}

下面简要说明催生路由事件这一概念的那些场景，以及为什么普通的 CLR 事件在这些场景下力有不逮：

**控件组合与封装：**Avalonia 中许多控件都有丰富的内容模型。比如你可以把一张图片放进 [`Button`](/api/avalonia/controls/button) 里，这实际上扩展了按钮的视觉树。但加进去的图片绝不能破坏命中测试的行为——即便用户点的像素严格说来属于那张图片，按钮也依然要对其内容上的 `Click` 作出反应。

**处理程序只需挂一处：**在 Windows Forms 中，若多个元素都可能引发某个事件，你就得把同一个处理程序反复挂上好几次。有了路由事件，只挂一次即可，就像这个例子：

```xml
 <Border Height="50" Width="300">
  <StackPanel Orientation="Horizontal" Button.Click="CommonClickHandler">
    <Button Name="YesButton">Yes</Button>
    <Button Name="NoButton">No</Button>
    <Button Name="CancelButton">Cancel</Button>
  </StackPanel>
</Border>
```

```csharp
private void CommonClickHandler(object sender, RoutedEventArgs e)
{
  var source = e.Source as Control;
  switch (source.Name)
  {
    case "YesButton":
      // do something here ...
      break;
    case "NoButton":
      // do something ...
      break;
    case "CancelButton":
      // do something ...
      break;
  }
  e.Handled=true;
}
```

**类处理：**路由事件允许由类定义一个静态处理程序。这个类处理程序有机会抢在任何实例处理程序之前处理该事件。

**无需反射即可引用事件：**某些代码和标记技术需要有办法标识出某个具体事件。路由事件会创建一个 [`RoutedEvent`](/api/avalonia/interactivity/routedevent) 字段作为标识，从而提供一种稳妥的事件标识方式，既不依赖静态反射，也不依赖运行时反射。

### 路由事件是怎么实现的 {#how-routed-events-are-implemented}

路由事件本质上是一个 CLR 事件，背后由 `RoutedEvent` 类的一个实例支撑，并注册到 Avalonia 的事件系统中。注册时拿到的 `RoutedEvent` 实例，通常会作为注册方（也即路由事件的「所有者」）类中的 `public` `static` `readonly` 字段成员保留下来。它与同名 CLR 事件（有时称作「包装」事件）的连接，是通过重写该 CLR 事件的 `add` 和 `remove` 实现来完成的。通常 `add` 和 `remove` 会保持隐式默认，按各语言自己的事件语法来添加和移除处理程序。这套路由事件的支撑与连接机制，在概念上与 avalonia 属性颇为相似——后者也是一个 CLR 属性，背后由 `AvaloniaProperty` 类支撑，并注册到 Avalonia 属性系统中。

下面的例子展示了一个自定义 `Tap` 路由事件的声明，包括 `RoutedEvent` 标识字段的注册与公开，以及 `Tap` CLR 事件的 `add` 和 `remove` 实现。

```csharp
public class SampleControl: Control
{
  public static readonly RoutedEvent<RoutedEventArgs> TapEvent =
    RoutedEvent.Register<SampleControl, RoutedEventArgs>(nameof(Tap), RoutingStrategies.Bubble);

  // Provide CLR accessors for the event
  public event EventHandler<RoutedEventArgs> Tap
  { 
    add => AddHandler(TapEvent, value);
    remove => RemoveHandler(TapEvent, value);
  }
}
```

### 路由事件处理程序与 XAML {#routed-event-handlers-and-xaml}

要在 XAML 中为事件添加处理程序，请在充当事件侦听者的元素上，把事件名写成一个特性。特性的值就是你实现的处理程序方法名，该方法必须存在于代码隐藏文件的那个类中。

```xml
<Button Click="b1SetColor">button</Button>
```

添加标准 CLR 事件处理程序的 XAML 语法，与添加路由事件处理程序完全相同——因为你实际上挂的是 CLR 事件包装器，其底层正是路由事件的实现。

## 路由策略 {#routing-strategies}

路由事件采用以下三种路由策略之一：

* **冒泡：**先调用事件源上的处理程序，随后路由事件逐级传给父元素，直到抵达元素树的根。多数路由事件都采用冒泡策略。冒泡路由事件一般用来上报来自各个控件或界面元素的输入或状态变化。
* **直接：**只有源元素自己有机会调用处理程序作出响应。这与 Windows Forms 对事件的「路由」方式类似。不过与标准 CLR 事件不同的是，直接路由事件支持类处理（类处理在后文会讲到）。
* **隧道：**先调用元素树根部的处理程序，随后路由事件沿路径逐级穿过子元素，朝着作为事件源的那个节点元素（也就是引发该路由事件的元素）前进。隧道路由事件常被用在控件的组合过程中，以便把来自内部组成部件的事件有意地压下去，或者换成针对整个控件的事件。Avalonia 提供的输入事件往往会同时引发隧道事件和冒泡事件。

## 为什么要用路由事件？ {#why-use-routed-events}

作为应用开发者，你未必总需要知道、或在意自己处理的事件其实是个路由事件。路由事件有其特殊行为，但只要你是在引发事件的那个元素上处理它，这些行为基本都察觉不到。

路由事件真正显出威力的，是前面提到的那几种场景：在共同的根上定义通用处理程序、组合出自己的控件，或者定义自定义控件类。

路由事件的侦听者与事件源，并不需要在各自的层次结构中共有某个事件。任何控件都可以充当任何路由事件的侦听者。因此，你可以把整套可用 API 中的全部路由事件视为一种概念上的「接口」，让应用中彼此无关的元素借它交换事件信息。这种把路由事件当「接口」的思路，对输入事件尤其适用。

路由事件还能用来在元素树中传递信息，因为事件数据会一路传给路径上的每个元素。某个元素可以改动事件数据中的内容，这一改动对路径上的下一个元素就是可见的。

除了路由这一面，Avalonia 的某个事件之所以实现为路由事件而非标准 CLR 事件，还有另外两个理由。若你要实现自己的事件，不妨也考虑考虑这两条原则：

* 某些样式和模板功能要求被引用的事件必须是路由事件。这正是前面提到的事件标识场景。
* 路由事件支持类处理机制：类可以指定若干静态方法，让它们抢在任何已注册的实例处理程序之前处理路由事件。这在控件设计中非常有用，因为你的类可以强制施行某些由事件驱动的类行为，不至于被实例上的某个事件处理程序意外压掉。

上述每一点，本文都会单辟一节展开。

## 为路由事件添加并实现事件处理程序 {#adding-and-implementing-an-event-handler-for-a-routed-event}

要在 XAML 中添加事件处理程序，请把事件名作为特性加到元素上，并把特性值设成某个实现了相应委托的事件处理程序的名字，如下例所示。

```xml
<Button Click="b1SetColor">button</Button>
```

`b1SetColor` 是你实现的那个处理程序的名字，其中装着处理 `Click` 事件的代码。`b1SetColor` 的签名必须与 `RoutedEventHandler<RoutedEventArgs>` 委托一致——那正是 `Click` 事件的事件处理程序委托。所有路由事件处理程序委托的第一个参数都指明处理程序被添加到了哪个元素上，第二个参数则是该事件的数据。

```csharp
void b1SetColor(object sender, RoutedEventArgs args)
{
  //logic to handle the Click event
}
```

`RoutedEventHandler<RoutedEventArgs>` 是最基本的路由事件处理程序委托。对于专为某些控件或场景设计的路由事件，其处理程序所用的委托往往也更专门，以便传递专门的事件数据。比如在常见的输入场景里，你可能要处理 `PointerPressed` 路由事件，此时处理程序应当实现 `RoutedEventHandler<PointerPressedEventArgs>` 委托。用上这个更专门的委托，你就能在处理程序中处理 `PointerPressedEventArgs` 并读取 `PointerEventArgs.Pointer` 属性，后者含有引发本次按下的那个指针的信息。

在用代码创建的应用中，为路由事件添加处理程序很直接。路由事件处理程序总是可以通过辅助方法 `AddHandler` 添加（`add` 现有的支撑实现调用的也正是这个方法）。不过 Avalonia 现有的路由事件一般都带有 `add` 和 `remove` 的支撑逻辑，因而可以用各语言自己的事件语法来添加处理程序，这比辅助方法直观得多。下面是辅助方法的用法示例：

```csharp
void MakeButton()
{
    Button b2 = new Button();
    b2.AddHandler(Button.ClickEvent, Onb2Click);
}

void Onb2Click(object sender, RoutedEventArgs e)
{
    //logic to handle the Click event     
}
```

下一个例子展示 C# 的运算符写法：

```csharp
void MakeButton2()
{
  Button b2 = new Button();
  b2.Click += Onb2Click2;
}

void Onb2Click2(object sender, RoutedEventArgs e)
{
  //logic to handle the Click event     
}
```

**「已处理」这个概念**

所有路由事件都共用同一个事件数据基类 `RoutedEventArgs`。`RoutedEventArgs` 定义了取布尔值的 `Handled` 属性。`Handled` 属性的用处在于：路径上的任何事件处理程序都可以把 `Handled` 设为 `true`，从而把这个路由事件标记为_已处理_。在路径上某个元素的处理程序处理过之后，这份共享的事件数据会继续上报给路径上的每一个侦听者。

`Handled` 的取值会影响路由事件在后续路径上如何被上报和处理。若某个路由事件的事件数据中 `Handled` 为 `true`，那么其他元素上侦听该路由事件的处理程序，针对这一次事件实例通常就不会再被调用了。无论处理程序是在 XAML 中挂的，还是用 `+=` 这类语言专属语法添加的，情况都一样。在大多数常见场景下，把 `Handled` 设为 `true`、将事件标记为已处理，就会「截停」隧道或冒泡路由；对于在路径某处被类处理程序处理掉的事件，也是如此。

不过还有一种「handledEventsToo」机制：即便事件数据中 `Handled` 已为 `true`，侦听者仍可运行自己的处理程序作出响应。换句话说，把事件数据标记为已处理，并不能真正截停事件路径。这一机制只能在代码中使用：

* 在代码中，不要用适用于一般 CLR 事件的语言专属事件语法，而要调用 Avalonia 的 `AddHandler<TEventArgs>(RoutedEvent<TEventArgs>, EventHandler<TEventArgs> handler, RoutingStrategies, bool)` 方法来添加处理程序，并把 `handledEventsToo` 的值指定为 `true`。

除了 `Handled` 状态在路由事件中带来的行为之外，`Handled` 这一概念还会影响你该如何设计应用、如何编写事件处理代码。你可以把 `Handled` 理解成路由事件对外公开的一套简单约定。具体怎么用这套约定由你说了算，但 `Handled` 取值在概念设计上的本意是这样的：

* 若某个路由事件已被标记为已处理，那么路径上的其他元素就不必再处理它了。
* 若某个路由事件尚未被标记为已处理，那么说明路径上更早的那些侦听者要么没注册处理程序，要么注册了但选择不去改动事件数据、不把 `Handled` 设为 `true`。（当然，也可能当前这个侦听者本就是路径的起点。）此时当前侦听者上的处理程序有三条路可走：
  * 什么也不做；事件保持未处理状态，继续路由到下一个侦听者。
  * 执行代码作出响应，但认为所做的动作还不足以把事件标记为已处理。事件继续路由到下一个侦听者。
  * 执行代码作出响应，并认为动作足够实质，于是在传给处理程序的事件数据中把事件标记为已处理。事件仍会路由到下一个侦听者，但其事件数据中带着 `Handled=true`，因此只有 `handledEventsToo` 的侦听者才有机会继续调用处理程序。

前面提到的路由行为更坐实了这套概念设计：若路径上先前的某个处理程序已经把 `Handled` 设成了 `true`，想再挂上照样会被调用的处理程序就麻烦些（尽管在代码或样式中仍然做得到）。

在实际应用中，人们常常就在引发事件的那个对象上处理冒泡路由事件，压根不去管事件的路由特性。即便如此，把路由事件在事件数据中标记为已处理仍是个好习惯——万一元素树上游还有元素也为同一个路由事件挂了处理程序，这样可以避免意料之外的副作用。

## 类处理程序 {#class-handlers}

若你定义的类以某种方式派生自 `AvaloniaObject`，你还可以为类中声明或继承来的路由事件成员定义并挂上类处理程序。每当路由事件在路径上抵达该类的某个元素实例时，类处理程序总会先于挂在该实例上的实例处理程序被调用。

Avalonia 的一些控件对某些路由事件带有内建的类处理。表面看上去那个路由事件好像压根没被引发，实际上它是被类处理掉了；而且只要用对办法，你的实例处理程序照样有机会处理它。此外，许多基类和控件都公开了虚方法，可用来覆盖类处理行为。

要在你自己的控件中挂上类处理程序，请在静态构造函数里调用 `AddClassHandler` 方法：

```csharp
static MyControl()
{
    MyEvent.AddClassHandler<MyControl>((x, e) => x.OnMyEvent(e));
}

protected virtual void OnMyEvent(MyEventArgs e)
{
    // Handle event here.
}
```

## Avalonia 中的附加事件 {#attached-events-in-avalonia}

XAML 语言还定义了一类特殊事件，叫作_附加事件_。附加事件让你能把某个事件的处理程序添加到任意元素上。处理该事件的元素既不必定义、也不必继承这个附加事件；无论是可能引发事件的对象，还是最终处理它的实例，都不必把该事件定义成自己的类成员、或以别的方式「拥有」它。

Avalonia 的输入系统大量使用附加事件。不过这些附加事件几乎都经由基元素转发出来，于是这些输入事件就以基元素类成员的形式，表现为与之等价的非附加路由事件。比如底层的 `Tapped` 事件，你可以直接在任意 `InputElement` 上处理，而不必在 XAML 或代码里跟附加事件语法较劲。

## XAML 中的限定事件名 {#qualified-event-names-in-xaml}

还有一种写法形似 _类型名_._事件名_ 的附加事件语法，严格说来却并非附加事件用法：当你为子元素引发的路由事件挂处理程序时就是这样。你把处理程序挂到共同的父元素上以借用事件路由，哪怕这个父元素压根没有那个路由事件成员。再看看[本页前面](#top-level-scenarios-for-routed-events)那个例子。

```xml
<Border Height="50" Width="300">
  <StackPanel Orientation="Horizontal" Button.Click="CommonClickHandler">
    <Button Name="YesButton">Yes</Button>
    <Button Name="NoButton">No</Button>
    <Button Name="CancelButton">Cancel</Button>
  </StackPanel>
</Border>
```

这里添加处理程序的父元素侦听者是一个 `StackPanel`，但它挂上的却是由 `Button` 类声明并引发的路由事件的处理程序。事件由 `Button` 所「拥有」，但路由事件系统允许把任何路由事件的处理程序，挂到任何本可以挂公共语言运行时（CLR）事件侦听者的控件实例上。这类限定事件特性名的默认 xmlns 命名空间通常就是 Avalonia 的默认 xmlns 命名空间，不过你也可以为自定义路由事件指定带前缀的命名空间。

## 输入事件 {#input-events}

在 Avalonia 平台中，路由事件最常见的用武之地就是输入事件。输入事件往往成对出现：一个是冒泡事件，另一个是隧道事件。偶尔也有输入事件只有冒泡版本，或者只有直接路由版本。

Avalonia 中成对出现的输入事件，其实现方式是：用户的一次输入动作（比如按下鼠标键）会依次引发这一对中的两个路由事件。先引发隧道事件并走完它的路径，再引发冒泡事件并走完它的路径。两个事件实实在在共用同一份事件数据实例，因为引发冒泡事件的那个实现类在调用 `RaiseEvent` 方法时，会接住隧道事件的事件数据并在新引发的事件中复用它。为隧道事件挂了处理程序的侦听者，最先有机会把路由事件标记为已处理（先是类处理程序，然后才是实例处理程序）。若隧道路径上某个元素把事件标记为已处理，这份「已处理」的事件数据会继续送给冒泡事件，于是为对应冒泡输入事件挂的普通处理程序就不会被调用了。从外部看，就好像那个被处理掉的冒泡事件压根没有被引发过。这种处理行为对控件组合很有用：你可能希望所有基于命中测试或基于焦点的输入事件，都由最终那个控件来上报，而不是由它的各个组成部件上报。最终的控件元素在组合结构中更靠近根部，因而有机会先对隧道事件作类处理，并在支撑控件类的代码里，用一个更贴合该控件的事件把那个路由事件「换掉」。

为了说明输入事件是怎么处理的，来看下面这个输入事件的例子。在下面的树状图中，`leaf element #2` 是 `PointerPressed` 事件的来源：

<Image light={InputEventRoutingDiagram} alt="Event routing diagram" position="center" maxWidth={400} cornerRadius="true"/>

事件的处理顺序如下：

1. 根元素上的 `PointerPressed`（隧道）。
2. 中间元素 #1 上的 `PointerPressed`（隧道）。
3. 源元素 #2 上的 `PointerPressed`（隧道）。
4. 源元素 #2 上的 `PointerPressed`（冒泡）。
5. 中间元素 #1 上的 `PointerPressed`（冒泡）。
6. 根元素上的 `PointerPressed`（冒泡）。

路由事件处理程序委托提供了两个对象引用：引发事件的对象，以及处理程序被调用时所在的对象。处理程序被调用时所在的对象由 `sender` 参数给出，而最初引发事件的对象则由事件数据中的 `Source` 属性给出。路由事件当然也可能由同一个对象引发并处理，此时 `sender` 与 `Source` 完全相同（上面处理顺序清单中的第 3、4 步就是这种情况）。

由于有隧道和冒泡，父元素收到输入事件时，其 `Source` 往往是它的某个子元素。当你需要弄清源元素究竟是谁时，访问 `Source` 属性即可。

通常，输入事件一旦被标记为 `Handled`，后续处理程序就不会再被调用了。一般来说，只要某个处理程序已经按你的应用逻辑把这个输入事件的含义处理妥当，就该立刻把它标记为已处理。

这条关于 `Handled` 状态的通则有个例外：那些注册时就声明要刻意无视事件数据 `Handled` 状态的输入事件处理程序，在两条路径上都照样会被调用。

某些类会选择对特定输入事件作类处理，通常意在重新定义某个由用户驱动的输入事件在该控件内的含义，并引发一个新事件。

## 另请参阅 {#see-also}

- [加入交互](/docs/input-interaction/adding-interactivity)：事件与命令概览。
- [指针事件](/docs/input-interaction/pointer)：指针设备事件与指针捕获。
- [手势](/docs/input-interaction/gestures)：构建在指针事件之上的更高层手势事件。
