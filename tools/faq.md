---
id: faq
title: FAQ
doc-type: troubleshooting
---

## General

#### 用 Avalonia 需要许可证吗？ {#do-i-need-a-license-to-use-avalonia}

不需要。**Avalonia 本身始终以 MIT 许可证完全开源。**你可以永久免费地用 Avalonia 开发并发布商业应用。Community 许可证只针对专业工具链（Visual Studio 扩展、Dev Tools、Parcel），与框架本身无关。

#### 要是这些我都不想要呢？ {#what-if-i-dont-want-any-of-this}

完全没问题。所有旧版工具依旧开源，都能在 GitHub 上找到：
- 现有的 Visual Studio 扩展
- Dev Tools
- TreeDataGrid

你可以继续照原样使用它们，也可以 fork 出来自行维护。

#### 我还能继续用旧版工具吗？ {#can-i-continue-using-the-legacy-tools}

可以。旧版的 FOSS Visual Studio 扩展仍可在 [github.com/AvaloniaUI/AvaloniaVS](https://github.com/AvaloniaUI/AvaloniaVS) 克隆并构建，旧版 Dev Tools 的源码依然在，最初的 TreeDataGrid 也还在。它们都是 MIT 许可证，任何人都可以使用、fork 或接手维护。

#### 我的 Community 许可证什么时候到期？ {#when-does-my-community-license-expire}

只要你仍符合资格，Community 许可证就不会到期。但若情况有变（比如你的组织规模超出了资格门槛），就必须升级到付费许可证。

#### Visual Studio 的宽限期过后会怎样？ {#what-happens-after-the-visual-studio-grace-period}

2026 年 4 月 13 日之后，若你既没注册 Community 许可证也没购买付费许可证，你可以：
- 继续使用旧版的 FOSS Visual Studio 扩展
- 改用 Visual Studio Code 或 JetBrains Rider（相应扩展依旧免费）
- 若符合资格，注册一个 Community 许可证
- 购买付费许可证

#### 我还有别的问题，上哪儿问？ {#i-have-another-question-where-can-i-ask}

欢迎到[社区中心](https://github.com/AvaloniaCommunity)和 [Avalonia 支持](https://support.avaloniaui.net/)留下你的问题或反馈。

## 开发者工具 {#developer-tools}

#### 可以把多个实例连到开发者工具上吗？ {#is-it-possible-to-connect-multiple-instances-to-the-developer-tools}

可以。只要有一个开发者工具实例在运行并已激活，你就能把一个乃至多个应用连上去。
每来一个新连接都会开一个新的开发者工具窗口，彼此独立工作。

#### 它支持 Browser/Android/iOS 吗？ {#does-it-work-with-browserandroidios}

移动端和浏览器应用都支持。
更多细节请见[挂接浏览器或移动端应用](/tools/developer-tools/attaching-applications)。

#### NativeAOT 应用能用开发者工具和 DiagnosticsPackage 吗？ {#can-i-use-developer-tools-and-diagnosticspackage-with-nativeaot-app}

可以。DiagnosticsPackage 对裁剪十分友好。虽说它确实用到了反射，但该工具在 AOT 下经过了测试。

#### `AvaloniaUI.DiagnosticsSupport` 取代 `Avalonia.Diagnostics` 包了吗？还是两个都得装？ {#does-avaloniauidiagnosticssupport-replace-avaloniadiagnostics-package-or-do-i-need-both}

你只需要 `AvaloniaUI.DiagnosticsSupport`。
`Avalonia.Diagnostics` 是旧版开发者工具用的老包，可以放心从项目里移除。
若出于某种原因确有必要，两个包也能同时引用，不过最好给各自的工具配不同的手势。

#### 没有许可证的人也能构建引用了 `AvaloniaUI.DiagnosticsSupport` 的项目吗？ {#can-everybody-build-project-referencing-avaloniauidiagnosticssupport-even-without-a-license}

可以。`AvaloniaUI.DiagnosticsSupport` 是个集成包，充当 `Developer Tools` 与用户应用之间的桥梁。它本身不需要任何许可证，公开项目里也可以引用。

但真要打开 `Developer Tools`，就得有许可证和 Avalonia 门户账号了。

#### 有必要在 Release/生产构建中排除 `AvaloniaUI.DiagnosticsSupport` 包吗？ {#is-it-necessary-to-exclude-avaloniauidiagnosticssupport-package-from-releaseproduction-build}

该工具对 Release 版本的内部测试也挺有用，并非只能随 Debug 构建一起引入。

与旧版 Avalonia DevTools 不同，这个包不带那些可能把 Release 编译搞砸的笨重依赖。

不过出于安全和包体积的考虑，仍建议在生产构建中排除它。

做法是使用 `Condition="'$(Configuration)' == 'Debug'"'`：
```xml
<PackageReference Include="AvaloniaUI.DiagnosticsSupport" Version="" Condition="'$(Configuration)' == 'Debug'" />
```

再配合 `this.AttachDeveloperTools()` 或 `.WithDeveloperTools()` 的 `#if DEBUG` 一起用。

#### 有没有 arm64 和 x86 版本的工具，或者有这个计划吗？ {#are-arm64-and-x86-builds-of-the-tool-available-or-planned}

目前 Windows 和 Linux 只提供 **x64** 版本。
macOS 版是同时含 **x64** 和 **arm64** 两种架构的通用包。

## TreeDataGrid

### Data Updates

#### 我改了模型属性，TreeDataGrid 却不更新 {#treedatagrid-doesnt-update-when-i-change-model-properties}

**问题**：你改了数据对象上的属性，表格却没有反映出来。

**解决办法**：你的数据模型必须实现 `INotifyPropertyChanged`。TreeDataGrid 要靠属性变更通知来刷新界面。

```csharp
// ❌ Wrong - No property change notifications
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
}

// ✅ Correct - Implements INotifyPropertyChanged
public class Person : INotifyPropertyChanged
{
    private string _name;
    private int _age;

    public string Name
    {
        get => _name;
        set
        {
            if (_name != value)
            {
                _name = value;
                OnPropertyChanged();
            }
        }
    }

    public int Age
    {
        get => _age;
        set
        {
            if (_age != value)
            {
                _age = value;
                OnPropertyChanged();
            }
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
```

#### 往集合里添加项，新项却不出现 {#new-items-dont-appear-when-i-add-them-to-the-collection}

**问题**：你往 `List<T>` 或数组中添加了项，表格却不显示新项。

**解决办法**：改用 `ObservableCollection<T>`，它会自动把集合变化通知给表格。

```csharp
// ❌ Wrong - List doesn't notify of changes
private List<Person> _people = new List<Person>();

// ✅ Correct - ObservableCollection notifies of changes
private ObservableCollection<Person> _people = new ObservableCollection<Person>();
```

### Cell Editing

#### 点击单元格却进不了编辑状态 {#cell-editing-doesnt-work-when-i-click-on-cells}

**问题**：点击单元格没有进入编辑。

**解决办法**：确认你在列定义中同时提供了 getter 和 setter：

```csharp
// ❌ Wrong - No setter, column is read-only
new TextColumn<Person, string>("Name", x => x.Name)

// ✅ Correct - Has both getter and setter
new TextColumn<Person, string>(
    "Name",
    x => x.Name,
    (row, value) => row.Name = value)
```

可能还需要指定编辑手势：

```csharp
new TextColumn<Person, string>(
    "Name",
    x => x.Name,
    (row, value) => row.Name = value,
    options: new TextColumnOptions<Person>
    {
        BeginEditGestures = BeginEditGestures.Tap
    })
```

## WebView

#### 支持离屏渲染吗？能借此避开 airspace 问题吗？ {#is-offscreen-rendering-supported-to-avoid-airspace-issue}

部分支持。在 Linux 上，WPE 后端始终离屏渲染并合成进 Avalonia 的视觉树，因此那里不存在 airspace 问题。在 Windows 以及 Linux 的 WebKitGTK 后端上，可通过[环境选项](/controls/web/webview-environment)中的 `ExperimentalOffscreen` 启用离屏渲染，但尚属实验性。macOS 暂不支持。

#### Linux 上支持 NativeWebView 吗？ {#is-nativewebview-supported-on-linux}

支持。`NativeWebView` 会自动挑选后端：

- **WebKitGTK** 是保底选项，只要没装 WPE 就用它。Ubuntu 就属此列，它并未打包 WPE WebKit。
- **[WPE WebKit](https://wpewebkit.org)** 在其库存在时优先采用。它用 SHM（软件渲染）离屏绘制，因而不依赖原生窗口嵌入，X11 和 Wayland 会话下都能用。

无论走哪条路都不需要额外配置。各后端所需的运行时库请见 [Linux 前置条件](/docs/app-development/embedding-web-content#linux)；只有当你想在已装 WPE 的机器上改用 WebKitGTK 时，才需要 [`LinuxWpeWebViewEnvironmentRequestedEventArgs.PreferWebKitGtkInstead`](/controls/web/webview-environment#linux-wpe-webkit)。

#### WebAuthenticationBroker 能用于 Google Auth 或 Microsoft.Identity Auth 吗？ {#can-i-use-webauthenticationbroker-for-google-auth-or-microsoftidentity-auth}

两家认证提供方都支持。你可以：
- 手动构造请求和重定向用的 `Uri`
- 与 `Google.Apis.Auth` 和 `Microsoft.Identity.Client` NuGet 包集成

集成示例可在我们的[示例仓库](https://github.com/AvaloniaUI/Accelerate.Samples/tree/main/WebAuthenticationBrokerSample)中找到。

#### 为什么要选 WebAuthenticationBroker 而不是别的方案？ {#why-use-webauthenticationbroker-over-other-options}

`Microsoft.Identity.Client` 和 `Google.Apis.Auth` 虽然自带 Web-UI 对话框，但只限于特定平台和提供方。WebAuthenticationBroker 的长处在于：
- 实现与提供方无关
- 桌面平台开箱即用，对框架没有特别要求
- 完整支持 macOS，不受 mac-catalyst 的种种限制

#### NativeWebView 支持通过 getUserMedia() API 访问摄像头/麦克风/屏幕共享吗？ {#does-nativewebview-support-cameramicrophonescreenshare-access-via-getusermedia-api}

支持，`getUserMedia()` API 在各平台均可用。与桌面浏览器类似，用户会收到摄像头、麦克风或屏幕共享的权限提示。macOS 支持是在 `11.2.4` 版本中加入的。

有些平台还要求开发者在应用包上配置权限。若主应用需要某项权限，Web 视图多半也需要。例如在 macOS/iOS 的打包应用中就必须有 [NSCameraUsageDescription](https://developer.apple.com/documentation/bundleresources/information-property-list/nscamerausagedescription?language=objc)。

## 另请参阅 {#see-also}

- [安装开发者工具](/tools/developer-tools/installation)
- [Avalonia 工具概述](/tools/)
