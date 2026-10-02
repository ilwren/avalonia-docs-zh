# 术语表与文风约定

## 文风

- **称呼读者用「你」**，不用「您」「我们」。原文是第二人称祈使语气，中文保持一致。
- **不要逐字硬译。** 英文爱用的 "you can simply…"、"it is worth noting that…"
  在中文里是废话，直接删掉。宁可句子短，不要句子齐整。
- **破折号、从句尽量拆成短句。** 英文一句 40 词，中文拆成两三句往往更清楚。
- **被动语态改主动。** "The value is set by the binding" → 「绑定会设置该值」。
- **避免「的」字连用**，避免「进行」「实现」「使得」这类翻译腔动词。
- 中英文之间**加半角空格**：`按 F12 键`、`Avalonia 应用`。
- 标点用**全角**（`，。：；（）`），但代码、版本号、路径内部保持原样。

## 保留原文的专有名词

框架 / 产品名、语言名、IDE 名、包名一律保留：

> Avalonia、Avalonia XPF、Avalonia Plus、.NET、C#、F#、XAML、AXAML、MVVM、WPF、UWP、
> WinUI、Xamarin、MAUI、Skia、Impeller、NuGet、Visual Studio、Visual Studio Code、
> JetBrains Rider、GitHub、WebAssembly、Android、iOS、macOS、Linux、Windows、X11、
> Wayland、Parcel、TreeDataGrid、RichTextEditor、MediaPlayer、PdfViewer、NativeWebView

所有**类型名、成员名、属性名、命名空间、文件名**保持英文 —— 它们是代码里要照着敲的东西，
翻译了反而没法用。分段器会自动把它们屏蔽成占位符。

## 常用译名

| 英文 | 中文 | 备注 |
| --- | --- | --- |
| control | 控件 | |
| custom control | 自定义控件 | |
| user control | 用户控件 | |
| templated control | 模板化控件 | |
| attribute | 特性 | 指 XML/XAML 特性，与 property 区分 |
| property | 属性 | |
| attached property | 附加属性 | |
| styled property | 样式化属性 | |
| dependency property | 依赖属性 | |
| binding | 绑定 | |
| compiled binding | 编译绑定 | |
| data context | 数据上下文 | |
| data template | 数据模板 | |
| control theme | 控件主题 | |
| style class | 样式类 | |
| pseudoclass | 伪类 | |
| selector | 选择器 | |
| layout | 布局 | |
| panel | 面板 | |
| measure / arrange | 测量 / 排列 | 布局两阶段 |
| visual tree | 视觉树 | |
| logical tree | 逻辑树 | |
| code-behind | 代码隐藏 | 首次出现可写「代码隐藏（code-behind）」 |
| markup | 标记 | |
| routed event | 路由事件 | |
| bubbling / tunneling | 冒泡 / 隧道 | |
| event handler | 事件处理程序 | |
| brush | 画刷 | |
| stroke / fill | 描边 / 填充 | |
| easing | 缓动 | |
| transition | 过渡动画 | |
| render transform | 渲染变换 | |
| hit testing | 命中测试 | |
| pointer | 指针 | 不译作「鼠标」，触摸同样适用 |
| focus | 焦点 | |
| automation peer | 自动化对等体 | 无障碍 |
| accessibility | 无障碍访问 | |
| previewer | 预览器 | |
| template (project) | 模板 | |
| scaffold | 骨架 / 脚手架 | |
| overload | 重载 | |
| coerce | 强制值回调 | AvaloniaProperty 语境 |
| inherited from | 继承自 | |
| no summary available | 暂无摘要 | API 参考占位文案 |
| breaking change | 破坏性变更 | |
| deprecated | 已弃用 | |
| troubleshooting | 疑难排查 | |
| getting started | 快速上手 | |
| see also | 另请参阅 | |

## API 参考的固定句式

自动生成的 API 文档句式高度统一，译名必须一致，否则记忆库会裂开：

| 英文 | 中文 |
| --- | --- |
| Gets or sets … | 获取或设置…… |
| Gets a value indicating whether … | 获取一个值，指示…… |
| Occurs when … | 当……时发生 |
| Raised when … | 当……时引发 |
| Defines the X property. | 定义 X 属性。 |
| Identifies the X Avalonia property. | 标识 X Avalonia 属性。 |
| Initializes a new instance of the X class. | 初始化 X 类的新实例。 |
| Inherited from X. | 继承自 X。 |
