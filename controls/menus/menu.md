---
id: menu
title: 菜单
---

import MenuTopDockScreenshot from '/img/controls/menu/menu-top-dock.gif';
import MenuIconScreenshot from '/img/controls/menu/menu-icon.gif';

菜单控件可以为应用添加菜单结构。通常你会把菜单放在 DockPanel 控件的顶边，这样它就绘制在窗口顶部。

:::info
DockPanel 的参考信息请见 [DockPanel](/controls/layout/panels/dockpanel)。
:::

## 菜单项 {#menu-items}

菜单元素内部通常嵌套一组 `<MenuItem>` 元素。第一层菜单项构成菜单的横向部分，再往下的层级则是下拉菜单。

菜单项的文字由 `Header` 属性设置。如有需要，菜单项的内容区里还可以放子项。

加入 `<Separator>` 元素即可添加菜单分隔线；也可以添加一个 header 设为减号的菜单项，像这样：

```xml
<MenuItem Header="-" />
```

## 常用属性 {#useful-properties}

下面这些属性你多半会经常用到：

<table>
  <thead>
    <tr>
      <th width="147.33333333333331">Element</th>
      <th width="190">Property</th>
      <th>说明</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>Menu</code></td>
      <td><code>DockPanel.Dock</code></td>
      <td>把菜单摆在 DockPanel 的顶边。</td>
    </tr>
    <tr>
      <td><code>MenuItem</code></td>
      <td><code>Header</code></td>
      <td>菜单项的文字。</td>
    </tr>
    <tr>
      <td><code>MenuItem</code></td>
      <td><code>InputGesture</code></td>
      <td>菜单项上显示的快捷键。设置该属性并不会让菜单项真的去处理这个输入手势，它只负责把手势文字显示出来。</td>
    </tr>
    <tr>
      <td><code>MenuItem</code></td>
      <td><code>Command</code></td>
      <td>菜单项被点击、或用键盘选中时所执行的命令。</td>
    </tr>
    <tr>
      <td><code>MenuItem</code></td>
      <td><code>MenuItem.Icon</code></td>
      <td>放置一个图标，显示在菜单项旁边。</td>
    </tr>
    <tr>
      <td><code>Separator</code></td>
      <td></td>
      <td>菜单分隔线。</td>
    </tr>
    <tr>
      <td></td>
      <td><code>ItemsPanel</code></td>
      <td>承载各项的容器面板，默认是 `StackPanel`。自定义 `ItemsPanel` 的方法见[自定义面板](/docs/how-to/itemscontrol-how-to#custom-panel)。</td>
    </tr>
    <tr>
      <td></td>
      <td><code>Styles</code></td>
      <td>应用到 ItemControl 任意子元素上的样式。</td>
    </tr>
  </tbody>
</table>

## Example

本例创建一个停靠在窗口顶边的菜单。

<Image light={MenuTopDockScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

```xml
<Window ...>
    <DockPanel>
    <Menu DockPanel.Dock="Top">
      <MenuItem Header="_File">
        <MenuItem Header="_Open..."/>
        <Separator/>
        <MenuItem Header="_Exit"/>
      </MenuItem>
      <MenuItem Header="_Edit">
        <MenuItem Header="Copy"/>
        <MenuItem Header="Paste"/>
      </MenuItem>
    </Menu>
    <TextBlock/>
  </DockPanel>
</Window>
```

## 访问键 {#accelerator-keys}

在 header 中某个字符前加下划线，即可把它定为访问键。例如：

```xml
 <MenuItem Header="_File">
```

有了它，用户可以快速访问某个菜单项。它有时也被称作热键、快捷字母或助记符。字母、数字和带重音的字符都可以作访问键。

用户先按 Alt 键，再按访问键即可（两者也可以一起按）。上面例子中的第二组菜单操作序列演示了这一点。

你会看到，一按下 Alt 键，菜单上凡是定义了访问键的字符都会显示下划线；再按下相应的访问键，对应的子菜单就展开了。

一旦用 Alt 键开启了键盘交互，用户还可以用方向键在菜单间穿行，并用回车键选中菜单项。

## 菜单命令 {#menu-commands}

要让菜单项发起操作，可以把它的 command 属性绑定到一个 `ICommand` 对象上。菜单项被点击或用键盘选中时，该命令就会执行。例如：

```xml
<Menu>
    <MenuItem Header="_File">
        <MenuItem Header="_Open..." Command="{Binding OpenCommand}"/>
    </MenuItem>
</Menu>
```

:::info
绑定命令的具体做法请见[添加交互](/docs/input-interaction/adding-interactivity)。
:::

## 可勾选与单选式菜单项 {#toggle-and-radio-menu-items}

在 `MenuItem` 上设置 `ToggleType` 属性，即可做出可勾选或单选式的菜单项：

```xml
<MenuItem Header="_View">
    <MenuItem Header="Show Toolbar" ToggleType="CheckBox" IsChecked="{Binding ShowToolbar}" />
    <MenuItem Header="Show Status Bar" ToggleType="CheckBox" IsChecked="{Binding ShowStatusBar}" />
    <Separator />
    <MenuItem Header="Light" ToggleType="Radio" GroupName="Theme"
              IsChecked="{Binding IsLightTheme}" />
    <MenuItem Header="Dark" ToggleType="Radio" GroupName="Theme"
              IsChecked="{Binding IsDarkTheme}" />
</MenuItem>
```

| ToggleType | 行为 |
|---|---|
| `None` | 标准菜单项（默认）。 |
| `CheckBox` | 独立切换 `IsChecked`。 |
| `Radio` | 同一个 `GroupName` 内同一时刻只能勾选一项。 |

## 菜单图标 {#menu-icons}

把图片或路径图标放进 `<MenuItem.Icon>` 附加属性，就能显示菜单图标。

<Image light={MenuIconScreenshot} alt="" position="center" maxWidth={400} cornerRadius="true"/>

```xml
<MenuItem Header="_Edit">
  <MenuItem Header="Copy">
     <MenuItem.Icon>
        <PathIcon Data="{StaticResource copy_regular}"/>
     </MenuItem.Icon>
  </MenuItem>
  <MenuItem Header="Paste">
     <MenuItem.Icon>
        <PathIcon Data="{StaticResource clipboard_paste_regular}"/>
     </MenuItem.Icon>
  </MenuItem>
</MenuItem>
```

:::info
为菜单添加图标的详细做法，请见[添加图标](/docs/graphics-animation/adding-icons)。
:::

## 另请参阅 {#see-also}

- [Menu API 参考](/api/avalonia/controls/menu)
- [GitHub 上的 `Menu.cs` 源码](https://github.com/AvaloniaUI/Avalonia/blob/master/src/Avalonia.Controls/Menu.cs)
