---
id: debugging-how-to
title: "操作指南：排查 Avalonia 常见问题"
description: 调试 Avalonia 应用中的绑定、布局、样式与渲染问题。
doc-type: how-to
---

本指南介绍排查 Avalonia 应用中绑定、布局、样式和渲染问题的若干手段。

## 调试数据绑定 {#debugging-data-bindings}

### 开启绑定错误日志 {#enable-binding-error-logging}

Avalonia 会把绑定错误记入跟踪输出。在 `Program.cs` 中配置日志：

```csharp
public static AppBuilder BuildAvaloniaApp()
    => AppBuilder.Configure<App>()
        .UsePlatformDetect()
        .LogToTrace(LogEventLevel.Warning);
```

绑定错误会以这样的警告形式出现：
```text
[Binding] Error in binding to 'MyProperty' on 'MyControl': Could not find a matching property accessor...
```

### 常见的绑定失误 {#common-binding-mistakes}

| 现象 | 可能的原因 |
|---|---|
| 控件什么都不显示 | 属性名拼错、没设置 `DataContext`，或者 `DataContext` 类型不对。 |
| 输出里出现「Binding error」 | `DataContext` 上根本没有这个属性。检查一下大小写和拼写。 |
| 单向能用，双向不行 | 属性缺少 setter，或者属性没有引发 `PropertyChanged`。 |
| 集合不更新 | 用了 `List<T>` 而不是 `ObservableCollection<T>`。 |
| 自定义控件无视绑定过来的值 | 在控件构造函数里设置了 `DataContext = this`。这会盖掉继承来的 `DataContext`，父级设置的绑定也就失效了。去掉这个赋值，改为在控件模板内部使用 `TemplateBinding`。 |

### 确认 DataContext {#verify-the-datacontext}

查看控件在运行时拿到的是什么 `DataContext`：

```csharp
// In code-behind for debugging
protected override void OnLoaded(RoutedEventArgs e)
{
    base.OnLoaded(e);
    System.Diagnostics.Debug.WriteLine($"DataContext: {DataContext?.GetType().Name}");
}
```

### 用编译绑定在构建期抓出错误 {#use-compiled-bindings-to-catch-errors-at-build-time}

```xml
<UserControl xmlns:vm="using:MyApp.ViewModels"
             x:DataType="vm:MainViewModel">
    <!-- Binding errors become compile errors -->
    <TextBlock Text="{Binding Name}" />
</UserControl>
```

## 调试布局问题 {#debugging-layout-issues}

### 把布局显形 {#make-layout-visible}

临时加上彩色背景，看看空间是怎么分配的：

```xml
<Grid ColumnDefinitions="200,*">
    <Border Grid.Column="0" Background="#10FF0000">
        <!-- Sidebar content -->
    </Border>
    <Border Grid.Column="1" Background="#100000FF">
        <!-- Main content -->
    </Border>
</Grid>
```

### 检查尺寸为零的元素 {#check-for-zero-size-elements}

宽或高为零的控件是看不见的。常见原因有：

- Canvas 的子元素缺少 `Width`/`Height`。
- `StackPanel` 的朝向与你想要的拉伸方向相垂直。
- `Image` 没有 `Source`，或者 URI 有误。

### Use DevTools

运行时（调试版本）按 **F12** 打开 Avalonia DevTools：

- **Visual Tree** 标签页：查看渲染出的树，以及每个控件的边界。
- **Properties** 标签页：查看属性的实际取值，尺寸也包括在内。
- **Styles** 标签页：看看套用了哪些样式，以及它们的优先级。

## Debugging Styles

### 样式不生效 {#style-not-applying}

| 现象 | 该查什么 |
|---|---|
| 样式毫无效果 | 确认选择器确实匹配得上。打开 DevTools > Styles 查看匹配到的样式。 |
| 局部值盖过了样式 | 局部值（内联写法）的优先级高于样式。把内联的值去掉即可。 |
| 文件里的样式没被加载 | 确认 `.axaml` 文件已通过 `App.axaml` 中的 `StyleInclude` 引入。 |

### 验证样式选择器 {#verify-a-style-selector}

在 DevTools 里试一试你的选择器。若匹配不上，常见问题有：

- 缺少样式类（忘了给控件加 `Classes="myClass"`）。
- 选择器里的控件类型写错了。
- 模板部件缺少 `/template/`。

## Debugging Rendering

### 控件看不见 {#control-not-visible}

按以下顺序排查：

1. **IsVisible** 为 `True`。
2. **Opacity** 大于 0。
3. 控件的 **Width** 和 **Height** 都不为零（或者它所在的面板给了它尺寸）。
4. 控件没有被设了 `ClipToBounds="True"` 的父级**裁掉**。
5. 控件位于**视口**之内（没被滚出可见范围）。

### 渲染瑕疵 {#rendering-artifacts}

- **文字或图标发糊**：图片查 `RenderOptions.BitmapInterpolationMode`，文字查 `TextOptions.TextHintingMode`，并确认 `UseLayoutRounding="True"`。
- **画面闪烁**：可能存在布局死循环。检查是否有绑定在布局过程中又触发了布局。

## Debugging Performance

### 揪出布局抖动 {#identify-layout-thrashing}

界面卡顿有个常见原因：布局过程跑得太频繁。DevTools 的性能标签页会显示布局次数。

### 检查虚拟化 {#check-virtualization}

面对长列表，请确认你用的是支持虚拟化的面板：

```xml
<ListBox ItemsSource="{Binding LargeList}" />
<!-- ListBox virtualizes by default -->
```

像 `ItemsControl` 里套 `StackPanel` 这样不作虚拟化的面板，会把所有项目一次性全建出来：

```xml
<!-- BAD: no virtualization -->
<ItemsControl ItemsSource="{Binding LargeList}" />

<!-- GOOD: use ListBox or configure VirtualizingStackPanel -->
<ListBox ItemsSource="{Binding LargeList}" />
```

## 趁手的调试工具 {#useful-debugging-tools}

| 工具 | 用途 |
|---|---|
| **DevTools (F12)** | 在运行时查看视觉树、属性、样式和事件。 |
| **Compiled Bindings** | 把绑定错误从运行时提前到编译期暴露出来。 |
| **LogToTrace** | 在调试输出中查看绑定错误和其他警告。 |
| **条件断点** | 在视图模型的 setter 中、属性变化时中断。 |

## 另请参阅 {#see-also}

- [绑定调试](/docs/data-binding/binding-debugging)：详细的绑定诊断手段。
- [编译绑定](/docs/data-binding/compiled-bindings)：在构建期抓出绑定错误。
- [性能](/docs/app-development/performance)：性能优化建议。
