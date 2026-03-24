---
name: huggingface-gradio
description: 使用 Python 构建 Gradio Web UI 和演示。在创建或编辑 Gradio 应用、组件、事件监听器、布局或聊天机器人时使用。
---

# Gradio

Gradio 是一个用于构建交互式 Web UI 和 ML 演示的 Python 库。本技能涵盖了核心 API、模式和示例。

## 指南

特定主题的详细指南(相关时阅读):

- [快速入门](https://www.gradio.app/guides/quickstart)
- [Interface 类](https://www.gradio.app/guides/the-interface-class)
- [Blocks 和事件监听器](https://www.gradio.app/guides/blocks-and-event-listeners)
- [控制布局](https://www.gradio.app/guides/controlling-layout)
- [更多 Blocks 功能](https://www.gradio.app/guides/more-blocks-features)
- [自定义 CSS 和 JS](https://www.gradio.app/guides/custom-CSS-and-JS)
- [流式输出](https://www.gradio.app/guides/streaming-outputs)
- [流式输入](https://www.gradio.app/guides/streaming-inputs)
- [分享您的应用](https://www.gradio.app/guides/sharing-your-app)
- [自定义 HTML 组件](https://www.gradio.app/guides/custom-HTML-components)
- [Python 客户端入门](https://www.gradio.app/guides/getting-started-with-the-python-client)
- [JS 客户端入门](https://www.gradio.app/guides/getting-started-with-the-js-client)

## 核心模式

**Interface**(高级): 用输入/输出组件包装函数。

```python
import gradio as gr

def greet(name):
    return f"Hello {name}!"

gr.Interface(fn=greet, inputs="text", outputs="text").launch()
```

**Blocks**(低级): 灵活的布局和显式事件连接。

```python
import gradio as gr

with gr.Blocks() as demo:
    name = gr.Textbox(label="Name")
    output = gr.Textbox(label="Greeting")
    btn = gr.Button("Greet")
    btn.click(fn=lambda n: f"Hello {n}!", inputs=name, outputs=output)

demo.launch()
```

**ChatInterface**: 聊天机器人 UI 的高级包装器。

```python
import gradio as gr

def respond(message, history):
    return f"You said: {message}"

gr.ChatInterface(fn=respond).launch()
```

## 关键组件签名

### `Textbox(value: str | I18nData | Callable | None = None, type: Literal['text', 'password', 'email'] = "text", lines: int = 1, max_lines: int | None = None, placeholder: str | I18nData | None = None, label: str | I18nData | None = None, info: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, autofocus: bool = False, autoscroll: bool = True, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", text_align: Literal['left', 'right'] | None = None, rtl: bool = False, buttons: list[Literal['copy'] | Button] | None = None, max_length: int | None = None, submit_btn: str | bool | None = False, stop_btn: str | bool | None = False, html_attributes: InputHTMLAttributes | None = None)`
创建一个文本区域,供用户输入字符串或显示字符串输出。

### `Number(value: float | Callable | None = None, label: str | I18nData | None = None, placeholder: str | I18nData | None = None, info: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", buttons: list[Button] | None = None, precision: int | None = None, minimum: float | None = None, maximum: float | None = None, step: float = 1)`
创建一个数字字段,供用户输入数字或显示数字输出。

### `Slider(minimum: float = 0, maximum: float = 100, value: float | Callable | None = None, step: float | None = None, precision: int | None = None, label: str | I18nData | None = None, info: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", randomize: bool = False, buttons: list[Literal['reset']] | None = None)`
创建一个滑块,范围从 {minimum} 到 {maximum},步长为 {step}。

### `Checkbox(value: bool | Callable = False, label: str | I18nData | None = None, info: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", buttons: list[Button] | None = None)`
创建一个可以设置为 `True` 或 `False` 的复选框。

### `Dropdown(choices: Sequence[str | int | float | tuple[str, str | int | float]] | None = None, value: str | int | float | Sequence[str | int | float] | Callable | DefaultValue | None = DefaultValue(), type: Literal['value', 'index'] = "value", multiselect: bool | None = None, allow_custom_value: bool = False, max_choices: int | None = None, filterable: bool = True, label: str | I18nData | None = None, info: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", buttons: list[Button] | None = None)`
创建一个下拉列表,可以从中选择单个条目或多个条目(作为输入组件)或显示(作为输出组件)。

### `Radio(choices: Sequence[str | int | float | tuple[str, str | int | float]] | None = None, value: str | int | float | Callable | None = None, type: Literal['value', 'index'] = "value", label: str | I18nData | None = None, info: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", rtl: bool = False, buttons: list[Button] | None = None)`
创建一组(字符串或数字类型)单选按钮,只能选择其中一个。

### `Image(value: str | PIL.Image.Image | np.ndarray | Callable | None = None, format: str = "webp", height: int | str | None = None, width: int | str | None = None, image_mode: Literal['1', 'L', 'P', 'RGB', 'RGBA', 'CMYK', 'YCbCr', 'LAB', 'HSV', 'I', 'F'] | None = "RGB", sources: list[Literal['upload', 'webcam', 'clipboard']] | Literal['upload', 'webcam', 'clipboard'] | None = None, type: Literal['numpy', 'pil', 'filepath'] = "numpy", label: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, buttons: list[Literal['download', 'share', 'fullscreen'] | Button] | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, streaming: bool = False, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", webcam_options: WebcamOptions | None = None, placeholder: str | None = None, watermark: WatermarkOptions | None = None)`
创建一个图像组件,可用于上传图像(作为输入)或显示图像(作为输出)。

### `Audio(value: str | Path | tuple[int, np.ndarray] | Callable | None = None, sources: list[Literal['upload', 'microphone']] | Literal['upload', 'microphone'] | None = None, type: Literal['numpy', 'filepath'] = "numpy", label: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, streaming: bool = False, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", format: Literal['wav', 'mp3'] | None = None, autoplay: bool = False, editable: bool = True, buttons: list[Literal['download', 'share'] | Button] | None = None, waveform_options: WaveformOptions | dict | None = None, loop: bool = False, recording: bool = False, subtitles: str | Path | list[dict[str, Any]] | None = None, playback_position: float = 0)`
创建一个音频组件,可用于上传/录制音频(作为输入)或显示音频(作为输出)。

### `Video(value: str | Path | Callable | None = None, format: str | None = None, sources: list[Literal['upload', 'webcam']] | Literal['upload', 'webcam'] | None = None, height: int | str | None = None, width: int | str | None = None, label: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", webcam_options: WebcamOptions | None = None, include_audio: bool | None = None, autoplay: bool = False, buttons: list[Literal['download', 'share'] | Button] | None = None, loop: bool = False, streaming: bool = False, watermark: WatermarkOptions | None = None, subtitles: str | Path | list[dict[str, Any]] | None = None, playback_position: float = 0)`
创建一个视频组件,可用于上传/录制视频(作为输入)或显示视频(作为输出)。

### `File(value: str | list[str] | Callable | None = None, file_count: Literal['single', 'multiple', 'directory'] = "single", file_types: list[str] | None = None, type: Literal['filepath', 'binary'] = "filepath", label: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, height: int | str | float | None = None, interactive: bool | None = None, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", allow_reordering: bool = False, buttons: list[Button] | None = None)`
创建一个文件组件,允许上传一个或多个通用文件(用作输入时)或显示通用文件或 URL 供下载(作为输出时)。

### `Chatbot(value: list[MessageDict | Message] | Callable | None = None, label: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, container: bool = True, scale: int | None = None, min_width: int = 160, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, autoscroll: bool = True, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", height: int | str | None = 400, resizable: bool = False, max_height: int | str | None = None, min_height: int | str | None = None, editable: Literal['user', 'all'] | None = None, latex_delimiters: list[dict[str, str | bool]] | None = None, rtl: bool = False, buttons: list[Literal['share', 'copy', 'copy_all'] | Button] | None = None, watermark: str | None = None, avatar_images: tuple[str | Path | None, str | Path | None] | None = None, sanitize_html: bool = True, render_markdown: bool = True, feedback_options: list[str] | tuple[str, ...] | None = ('Like', 'Dislike'), feedback_value: Sequence[str | None] | None = None, line_breaks: bool = True, layout: Literal['panel', 'bubble'] | None = None, placeholder: str | None = None, examples: list[ExampleMessage] | None = None, allow_file_downloads: <class 'inspect._empty'> = True, group_consecutive_messages: bool = True, allow_tags: list[str] | bool = True, reasoning_tags: list[tuple[str, str]] | None = None, like_user_message: bool = False)`
创建一个聊天机器人,显示用户提交的消息和响应。

### `Button(value: str | I18nData | Callable = "Run", every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, variant: Literal['primary', 'secondary', 'stop', 'huggingface'] = "secondary", size: Literal['sm', 'md', 'lg'] = "lg", icon: str | Path | None = None, link: str | None = None, link_target: Literal['_self', '_blank', '_parent', '_top'] = "_self", visible: bool | Literal['hidden'] = True, interactive: bool = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", scale: int | None = None, min_width: int | None = None)`
创建一个可以分配任意 .click() 事件的按钮。

### `Markdown(value: str | I18nData | Callable | None = None, label: str | I18nData | None = None, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool | None = None, rtl: bool = False, latex_delimiters: list[dict[str, str | bool]] | None = None, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", sanitize_html: bool = True, line_breaks: bool = False, header_links: bool = False, height: int | str | None = None, max_height: int | str | None = None, min_height: int | str | None = None, buttons: list[Literal['copy']] | None = None, container: bool = False, padding: bool = False)`
用于渲染任意 Markdown 输出。

### `HTML(value: Any | Callable | None = None, label: str | I18nData | None = None, html_template: str = "${value}", css_template: str = "", js_on_load: str | None = "element.addEventListener('click', function() { trigger('click') });", apply_default_css: bool = True, every: Timer | float | None = None, inputs: Component | Sequence[Component] | set[Component] | None = None, show_label: bool = False, visible: bool | Literal['hidden'] = True, elem_id: str | None = None, elem_classes: list[str] | str | None = None, render: bool = True, key: int | str | tuple[int | str, ...] | None = None, preserved_by_key: list[str] | str | None = "value", min_height: int | None = None, max_height: int | None = None, container: bool = False, padding: bool = False, autoscroll: bool = False, buttons: list[Button] | None = None, props: Any)`
创建一个具有任意 HTML 的组件。


## 自定义 HTML 组件

如果任务需要对现有组件进行大量自定义或创建 Gradio 中不存在的组件,您可以使用 `gr.HTML` 创建。它支持 `html_template`(使用 `${}` JS 表达式和 `{{}}` Handlebars 语法)、用于作用域样式的 `css_template`,以及用于交互性的 `js_on_load` — 其中 `props.value` 更新组件值,`trigger('event_name')` 触发 Gradio 事件。为了可重用性,子类化 `gr.HTML` 并定义 `api_info()` 以支持 API/MCP。参见[完整指南](https://www.gradio.app/guides/custom-HTML-components)。

以下是一个展示如何创建和使用这些类型组件的示例:

```python
import gradio as gr

class StarRating(gr.HTML):
    def __init__(self, label, value=0, **kwargs):
        html_template = """
        <h2>${label} rating:</h2>
        ${Array.from({length: 5}, (_, i) => `<img class='${i < value ? '' : 'faded'}' src='https://upload.wikimedia.org/wikipedia/commons/d/df/Award-star-gold-3d.svg'>`).join('')}
        """
        css_template = """
            img { height: 50px; display: inline-block; cursor: pointer; }
            .faded { filter: grayscale(100%); opacity: 0.3; }
        """
        js_on_load = """
            const imgs = element.querySelectorAll('img');
            imgs.forEach((img, index) => {
                img.addEventListener('click', () => {
                    props.value = index + 1;
                });
            });
        """
        super().__init__(value=value, label=label, html_template=html_template, css_template=css_template, js_on_load=js_on_load, **kwargs)

    def api_info(self):
        return {"type": "integer", "minimum": 0, "maximum": 5}


with gr.Blocks() as demo:
    gr.Markdown("# Restaurant Review")
    food_rating = StarRating(label="Food", value=3)
    service_rating = StarRating(label="Service", value=3)
    ambience_rating = StarRating(label="Ambience", value=3)
    average_btn = gr.Button("Calculate Average Rating")
    rating_output = StarRating(label="Average", value=3)
    def calculate_average(food, service, ambience):
        return round((food + service + ambience) / 3)
    average_btn.click(
        fn=calculate_average,
        inputs=[food_rating, service_rating, ambience_rating],
        outputs=rating_output
    )

demo.launch()
```

## 事件监听器

所有事件监听器共享相同的签名:

```python
component.event_name(
    fn: Callable | None | Literal["decorator"] = "decorator",
    inputs: Component | Sequence[Component] | set[Component] | None = None,
    outputs: Component | Sequence[Component] | set[Component] | None = None,
    api_name: str | None = None,
    api_description: str | None | Literal[False] = None,
    scroll_to_output: bool = False,
    show_progress: Literal["full", "minimal", "hidden"] = "full",
    show_progress_on: Component | Sequence[Component] | None = None,
    queue: bool = True,
    batch: bool = False,
    max_batch_size: int = 4,
    preprocess: bool = True,
    postprocess: bool = True,
    cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
    trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
    js: str | Literal[True] | None = None,
    concurrency_limit: int | None | Literal["default"] = "default",
    concurrency_id: str | None = None,
    api_visibility: Literal["public", "private", "undocumented"] = "public",
    time_limit: int | None = None,
    stream_every: float = 0.5,
    key: int | str | tuple[int | str, ...] | None = None,
    validator: Callable | None = None,
) -> Dependency
```

每个组件支持的事件:

- **AnnotatedImage**: select
- **Audio**: stream, change, clear, play, pause, stop, pause, start_recording, pause_recording, stop_recording, upload, input
- **BarPlot**: select, double_click
- **BrowserState**: change
- **Button**: click
- **Chatbot**: change, select, like, retry, undo, example_select, option_select, clear, copy, edit
- **Checkbox**: change, input, select
- **CheckboxGroup**: change, input, select
- **ClearButton**: click
- **Code**: change, input, focus, blur
- **ColorPicker**: change, input, submit, focus, blur
- **Dataframe**: change, input, select, edit
- **Dataset**: click, select
- **DateTime**: change, submit
- **DeepLinkButton**: click
- **Dialogue**: change, input, submit
- **DownloadButton**: click
- **Dropdown**: change, input, select, focus, blur, key_up
- **DuplicateButton**: click
- **File**: change, select, clear, upload, delete, download
- **FileExplorer**: change, input, select
- **Gallery**: select, upload, change, delete, preview_close, preview_open
- **HTML**: change, input, click, double_click, submit, stop, edit, clear, play, pause, end, start_recording, pause_recording, stop_recording, focus, blur, upload, release, select, stream, like, example_select, option_select, load, key_up, apply, delete, tick, undo, retry, expand, collapse, download, copy
- **HighlightedText**: change, select
- **Image**: clear, change, stream, select, upload, input
- **ImageEditor**: clear, change, input, select, upload, apply
- **ImageSlider**: clear, change, stream, select, upload, input
- **JSON**: change
- **Label**: change, select
- **LinePlot**: select, double_click
- **LoginButton**: click
- **Markdown**: change, copy
- **Model3D**: change, upload, edit, clear
- **MultimodalTextbox**: change, input, select, submit, focus, blur, stop
- **Navbar**: change
- **Number**: change, input, submit, focus, blur
- **ParamViewer**: change, upload
- **Plot**: change
- **Radio**: select, change, input
- **ScatterPlot**: select, double_click
- **SimpleImage**: clear, change, upload
- **Slider**: change, input, release
- **State**: change
- **Textbox**: change, input, select, submit, focus, blur, stop, copy
- **Timer**: tick
- **UploadButton**: click, upload
- **Video**: change, clear, start_recording, stop_recording, stop, play, pause, end, upload, input

## 其他参考

- [端到端示例](examples.md) — 完整的工作应用
