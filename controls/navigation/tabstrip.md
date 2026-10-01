---
id: tabstrip
title: TabStrip
description: 一条只有选项卡标题、不自带内容切换的选项卡栏，让你完全掌控选中内容的呈现方式。
doc-type: reference
---

显示一条选项卡标题栏。你可以把这个控件当作横向菜单来用。

[`TabStrip`](/api/avalonia/controls/primitives/tabstrip) 由 [`TabStripItem`](/api/avalonia/controls/primitives/tabstripitem) 子项组成。`TabStripItem` 按出现顺序显示，可以通过两种方式创建：1. 直接给出一组 `TabStripItem`；2. 由 `ItemsSource` 生成。

与 [`TabControl`](/api/avalonia/controls/tabcontrol) 不同，`TabStrip` 不负责呈现选中项的内容。`TabStrip` 要求你响应 `SelectionChanged` 事件或 `SelectedItem` 属性变化，再用另一个控件（比如 `ContentControl`）把目标内容显示出来。这让你完全掌控显示的内容，也让自定义视图缓存之类的玩法成为可能。

## 示例：`TabStrip` 搭配 `TabStripItem` {#example-tabstrip-with-tabstripitem}

<XamlPreview>

```xml
<TabStrip xmlns="https://github.com/avaloniaui" Margin="5">
  <TabStripItem>Tab 1</TabStripItem>
  <TabStripItem>Tab 2</TabStripItem>
</TabStrip>
```

</XamlPreview>

## 示例：`TabStrip` 搭配 `ItemsSource` {#example-tabstrip-with-itemssource}

```xml
<TabStrip ItemsSource="{Binding MyTabs}" SelectedItem="{Binding MySelectedItem}">
    <TabStrip.ItemTemplate>
        <DataTemplate x:DataType="vm:MyViewModel">
            <TextBlock Text="{Binding Header}"/>
        </DataTemplate>
    </TabStrip.ItemTemplate>
</TabStrip>
```

## 响应选中项变化 {#responding-to-selection-changes}

由于 `TabStrip` 不显示选中项的内容，你需要给它配一个独立的控件，比如 `ContentControl`。把 `SelectedIndex`（或 `SelectedItem`）绑定到视图模型，再根据变化切换显示的内容。

```xml
<DockPanel>
    <TabStrip DockPanel.Dock="Top"
              SelectedIndex="{Binding SelectedIndex}">
        <TabStripItem>Home</TabStripItem>
        <TabStripItem>Settings</TabStripItem>
    </TabStrip>
    <ContentControl Content="{Binding CurrentPage}" />
</DockPanel>
```

```csharp
public class MainViewModel : ViewModelBase
{
    private int _selectedIndex;
    private object? _currentPage;

    public int SelectedIndex
    {
        get => _selectedIndex;
        set
        {
            if (_selectedIndex != value)
            {
                _selectedIndex = value;
                OnPropertyChanged();
                UpdateCurrentPage();
            }
        }
    }

    public object? CurrentPage
    {
        get => _currentPage;
        set
        {
            _currentPage = value;
            OnPropertyChanged();
        }
    }

    private void UpdateCurrentPage()
    {
        CurrentPage = SelectedIndex switch
        {
            0 => new HomeViewModel(),
            1 => new SettingsViewModel(),
            _ => null
        };
    }
}
```

## `TabStrip` 与 `TabControl` 的取舍 {#when-to-use-tabstrip-vs-tabcontrol}

当你需要自定义内容切换逻辑（比如视图缓存或延迟加载）时，用 `TabStrip`。因为 `TabStrip` 不管内容显示，视图何时创建、是否缓存、何时释放，全由你说了算。

当你想要开箱即用的内容显示时，用 `TabControl`。`TabControl` 会把选项卡标题和内容区一并管好，你不必自己写任何内容切换逻辑。

## 另请参阅 {#see-also}

- [TabControl](/controls/navigation/tabcontrol)
- [TabStrip API 参考](/api/avalonia/controls/primitives/tabstrip)
- [GitHub 上的 `TabStrip.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Primitives/TabStrip.cs)
