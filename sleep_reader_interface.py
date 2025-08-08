from PyQt5.QtCore import Qt, QUrl, QRunnable, QThread, QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme, IconWidget, TextEdit, 
                            PrimaryPushButton, InfoBar, InfoBarPosition, ProgressRing
                            )
from qfluentwidgets import FluentIcon as FIF 

import sys
import os
from openai import OpenAI
from openai.types.chat.chat_completion import Choice
import re
import json
from typing import *

client = OpenAI(
        api_key="sk-EqnqTtSVD7nWjb8APdNtUW0mBbX0UouPs13C2nh4fbW06Iyk",
        base_url="https://api.moonshot.cn/v1"
    )


# 定义一个用于发送信号的QObject子类
class WorkerSignals(QObject):
    # 定义一个信号，用于通知主线程线程已经启动
    started = pyqtSignal()
    # 定义一个信号，用于通知主线程线程已经完成
    finished = pyqtSignal()
    # 定义一个信号，用于通知主线程线程发生错误
    error = pyqtSignal(tuple)
    # 添加一个信号，用于通知主线程线程信息
    message = pyqtSignal(str, str)
    # 定义一个信号，用于通知主线程线程的进度
    progress = pyqtSignal(int)

class StartReading(QRunnable):
    def __init__(self):
        super().__init__()
        # inital the file path
        self.file_path = os.path.join(os.path.dirname(__file__), 'dataSet', 'dream_library.txt')
        self.signals = WorkerSignals()

    def run(self):
        try:
            # 发出线程启动信号
            self.signals.started.emit()
            self.signals.message.emit("（+.+）", "sleep reader 开始在 dream library 中阅读啦~")
            self.start_reading()
            # 发出线程完成信号
            self.signals.finished.emit()
        except Exception as e:
            print(f"图书管理员开小差啦~: {e}")
            # 确保在异常情况下发出错误信号
            self.signals.error.emit((str(e),))
            self.signals.message.emit('Zzzzzz~', f'图书管理员开小差啦~: {str(e)}')  # 发射错误提示信号

    # 工作函数
    def start_reading(self):
        # 读取并去重url
        urls = self.read_urls_from_file()
        print(f"共有{len(urls)}条URL需要处理")

        # 循环处理每个url
        for i, url in enumerate(urls):
            if not url:
                continue
            # 调用API接口总结内容
            summary = self.read_by_Kimi("分析网页内容："+url)
            if summary:
                # 保存到json文件
                file_name =  re.sub(r'[\\/*?:"<>|]', '', summary["title"])+".json"
                save_file_path = os.path.join(os.path.dirname(__file__), "output",file_name)
                self.save_to_json(summary, save_file_path)
                
            # 发送进度信号，计算当前进度百分比
            progress_percent = ((i + 1) * 100 // len(urls)) if len(urls)-1 > i else 100
            self.signals.progress.emit(int(progress_percent))  # 发送百分比进度

    def read_urls_from_file(self):
        # read urls from file
        with open(self.file_path, 'r') as file:
            urls = [line.strip() if self.is_url(line.strip()) else None for line in file.readlines()]
    
        # remove duplicates
        return list(set(urls))
    
    # search 工具的具体实现，这里我们只需要返回参数即可
    def search_impl(self, arguments: Dict[str, Any]) -> Any:
        """
        在使用 Moonshot AI 提供的 search 工具的场合，只需要原封不动返回 arguments 即可，
        不需要额外的处理逻辑。
    
        但如果你想使用其他模型，并保留联网搜索的功能，那你只需要修改这里的实现（例如调用搜索
        和获取网页内容等），函数签名不变，依然是 work 的。
    
        这最大程度保证了兼容性，允许你在不同的模型间切换，并且不需要对代码有破坏性的修改。
        """
        return arguments
    
    def chat(self, messages) -> Choice:
        completion = client.chat.completions.create(
            model="moonshot-v1-128k",
            messages=messages,
            temperature=0.3,
            tools=[
                {
                    "type": "builtin_function",  # <-- 使用 builtin_function 声明 $web_search 函数，请在每次请求都完整地带上 tools 声明
                    "function": {
                        "name": "$web_search",
                    },
                }
            ]
        )
        return completion.choices[0]
    
    def read_by_Kimi(self, content):
        system_prompt = """
                    搜索URL中的文章、视频或图片中的信息，整理其内容并条理清晰地输出，要求如下：
                    1. 避免出现倾向性，保持客观准确。
                    2. 不要遗漏重要信息。
                    3. 输出的前十个字为标题，后面为总结内容。
                    4. 内容要真实可靠，不要虚假夸大。
                    5. 随时使用网络查找工具获得必要的额外相关信息。
                    6. 尽可能将教程等内容按步骤分解，条例输出。

                    请使用如下 JSON 格式输出你的回复：
                    {
                        "title": "总结标题",
                        "url": "链接地址",
                        "content": "具体内容"
                    }
                    其中content中的具体内容采用Markdown格式。

                    """
        print(f"正在阅读来自 {content} 的资料")

        messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "搜索该URL并结合分析：" + content}
                ]
    
        finish_reason = None
        while finish_reason is None or finish_reason == "tool_calls":
            choice = self.chat(messages)
            finish_reason = choice.finish_reason
            if finish_reason == "tool_calls":  # <-- 判断当前返回内容是否包含 tool_calls
                messages.append(choice.message)  # <-- 我们将 Kimi 大模型返回给我们的 assistant 消息也添加到上下文中，以便于下次请求时 Kimi 大模型能理解我们的诉求
                for tool_call in choice.message.tool_calls:  # <-- tool_calls 可能是多个，因此我们使用循环逐个执行
                    tool_call_name = tool_call.function.name
                    tool_call_arguments = json.loads(tool_call.function.arguments)  # <-- arguments 是序列化后的 JSON Object，我们需要使用 json.loads 反序列化一下
                    if tool_call_name == "$web_search":
                        tool_result = self.search_impl(tool_call_arguments)
                    else:
                        tool_result = f"Error: unable to find tool by name '{tool_call_name}'"
    
                    # 使用函数执行结果构造一个 role=tool 的 message，以此来向模型展示工具调用的结果；
                    # 注意，我们需要在 message 中提供 tool_call_id 和 name 字段，以便 Kimi 大模型
                    # 能正确匹配到对应的 tool_call。
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call_name,
                        "content": json.dumps(tool_result),  # <-- 我们约定使用字符串格式向 Kimi 大模型提交工具调用结果，因此在这里使用 json.dumps 将执行结果序列化成字符串
                    })
    
        print(choice.message.content)  # <-- 在这里，我们才将模型生成的回复返回给用户
        json_data = json.loads(choice.message.content)
        return json_data

    # # 使用Kimi的API接口调用r1模型总结内容
    # def read_by_Kimi(self, content):

    #     client = ai_engine
    #     system_prompt = """
    #                 搜索URL中的文章、视频或图片中的信息，整理其内容并条理清晰地输出，要求如下：
    #                 1. 避免出现倾向性，保持客观准确。
    #                 2. 不要遗漏重要信息。
    #                 3. 输出的前十个字为标题，后面为总结内容。
    #                 4. 内容要真实可靠，不要虚假夸大。
    #                 5. 随时使用网络查找工具获得必要的额外相关信息。
    #                 6. 尽可能将教程等内容按步骤分解，条例输出。

    #                 请使用如下 JSON 格式输出你的回复：
    #                 {
    #                     "title": "总结标题",
    #                     "url": "链接地址",
    #                     "content": "具体内容"
    #                 }
    #                 其中content中的具体内容采用Markdown格式。

    #                 """
    #     print(f"正在阅读来自 {content} 的资料")

    #     message = [
    #                 {"role": "system", "content": system_prompt},
    #                 {"role": "user", "content": content}
    #             ]
        
    #     try:
            
    #         response = client.chat.completions.create(
    #             model="moonshot-v1-128k",
    #             messages=message,
    #             temperature=0.5,
    #             response_format={"type": "json_object"}, # <-- 使用 response_format 参数指定输出格式为 json_object
    #             tools = [
    #                 {
    #                     "type": "builtin_function",  # <-- 我们使用 builtin_function 来表示 Kimi 内置工具，也用于区分普通 function
    #                     "function": {
    #                         "name": "$web_search",
    #                     },
    #                 },
    #             ],
    #             max_tokens=20000,
    #             stream=False,
    #         )
    #         summary = response.choices[0].message.content
    #         print(response.choices[0].model_dump_json(indent=4))
    #         json_data = json.loads(summary)
    #         return json_data
    #     except json.JSONDecodeError as e:
    #         print(f"JSON 解码错误: {e}")
    #         return None
    #     except Exception as e:
    #         print(f"调用API接口出错: {e}")
    #         return None
        
    # 将总结内容存入json文件
    def save_to_json(self, summary, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(summary, file, ensure_ascii=False, indent=4)

    def is_url(self, input_string):
        # URL的正则表达式模式
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://' # 匹配http://或https://等
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # 域名
            r'localhost|' # 本地主机
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # IP地址
            r'(?::\d+)?' # 端口
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(url_pattern, input_string) is not None

# 主界面类
class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        main_layout = QVBoxLayout(self)
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName('sleep_reader')
        self.resize(600,400)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(10)

        #inital the thread pool
        self.thread_pool = QThreadPool()

        # inital the file path
        self.file_path = os.path.join(os.path.dirname(__file__), 'dataSet', 'dream_library.txt')

        # inital the title
        self.title = QWidget()
        self.title_layout = QHBoxLayout(self.title)

        self.label = SubtitleLabel('Sleep Reader')
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(50)

        self.iconWidget = IconWidget(FIF.BOOK_SHELF)
        self.iconWidget.setFixedWidth(20)
        self.iconWidget.setFixedHeight(20)
        
        self.ring = ProgressRing()
        # 设置进度环取值范围和当前值
        self.ring.setRange(0, 100)
        self.ring.setValue(0)
        # 显示进度环内文本
        self.ring.setTextVisible(True)
        # 调整进度环大小
        self.ring.setFixedSize(50, 50)
        # 调整厚度
        self.ring.setStrokeWidth(5)

        self.title_layout.addWidget(self.iconWidget)
        self.title_layout.addWidget(self.label)
        self.title_layout.addWidget(self.ring)
        self.title_layout.addStretch(1)

        main_layout.addWidget(self.title)

        # inital the notes
        self.dream_sheff = TextEdit()
        self.dream_sheff.setFixedWidth(600)
        self.dream_sheff.setContentsMargins(10,10,10,10)
        self.load_note()
        self.dream_sheff.textChanged.connect(lambda: self.save_button.setEnabled(True))
        main_layout.addWidget(self.dream_sheff)

        # inital the buttons
        self.buttons = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons)
        self.save_button = PrimaryPushButton(FIF.SAVE, 'SAVE')
        self.save_button.clicked.connect(self.save_note)
        self.save_button.setEnabled(False)
        self.save_button.setFixedHeight(40)
        self.save_button.setFixedWidth(100)

        self.start_button = PrimaryPushButton(FIF.ROBOT, 'read')
        self.start_button.clicked.connect(self.start_reading)
        self.start_button.setFixedHeight(40)
        self.start_button.setFixedWidth(100)

        self.buttons_layout.addWidget(self.save_button)
        self.buttons_layout.addWidget(self.start_button)
        self.buttons_layout.addStretch(1)
        main_layout.addWidget(self.buttons)
        
    # 启动阅读任务
    def start_reading(self):
        # 创建异步任务，启动线程池
        self.ring.setValue(0)
        worker = StartReading()
        worker.signals.started.connect(self.on_thread_started)
        worker.signals.finished.connect(self.on_thread_finished)
        worker.signals.error.connect(self.on_thread_error)
        worker.signals.message.connect(self.show_message)  # 连接新的信号到槽函数
        worker.signals.progress.connect(self.update_progress)
        self.thread_pool.start(worker)

    def on_thread_started(self):
        print("线程已启动")

    def on_thread_finished(self):
        print("线程已完成")

    def on_thread_error(self, error_info):
        print(f"线程出错: {error_info}")
        InfoBar.error(
            title='错误',
            content=f"诶呀，读书的时候打瞌睡了: {error_info[0]}",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
    
    def show_message(self, title, content):
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self  # 这里的 self 是 QFrame 对象，是有效的 PyQt 组件
        )

    def update_progress(self, value):
        self.ring.setValue(value)

    # 储存url到dream library
    def save_note(self):
        note_text = self.dream_sheff.toPlainText().strip()
        if not note_text:
            InfoBar.warning(
                title='警告',
                content="美梦图书馆书架不能为空！",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            try:
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    file.write(self.dream_sheff.toPlainText())
                print(f"笔记已保存到 {self.file_path}")
            except Exception as e:
                print(f"保存笔记时出错: {e}")

            print("保存任务已启动，线程池正在处理...")
            self.save_button.setEnabled(False)
            InfoBar.success(
                title='成功',
                content="数据暂时安全保存！",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

    def load_note(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                note_text = file.read()
            self.dream_sheff.setPlainText(note_text)
            print(f"睡梦图书馆书架已加载到 {self.file_path}")
        except Exception as e:
            print(f"书架倒啦: {e}")

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Frame()
    w.show()
    app.exec_()