import sys
from openai import OpenAI
import os
import atexit

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLabel, QFrame
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from qfluentwidgets import (SubtitleLabel, setFont, SmoothScrollArea, PrimaryToolButton, ElevatedCardWidget, AvatarWidget,
                            InfoBar, InfoBarPosition, ToolTipFilter, ToolTipPosition,
                            )
from qfluentwidgets import FluentIcon as FIF 
import datetime
from typing import *
import json

# Deepseek API 配置
CHAT_MODE = 'moonshot-v1-128k'

client = OpenAI(
    api_key="sk-EqnqTtSVD7nWjb8APdNtUW0mBbX0UouPs13C2nh4fbW06Iyk",
    base_url="https://api.moonshot.cn/v1",
)

waiting = False


# 定义一个工作线程类
class ApiWorker(QThread):
    api_result = pyqtSignal(str)  # 定义一个信号，用于传递结果
    response_finished = pyqtSignal()  # 定义一个信号，用于通知线程结束

    def __init__(self, chat_mode, input_message, parent=None):
        super().__init__(parent)
        self.chat_mode = chat_mode
        self.system_message = [{"role": "system", "content": 
                                """
                                You will respond in the identity of Eileen, 
                                a cat girl with a lively and generous character, 
                                who likes to think and provide her own thoughts and suggestions to questions. 
                                Occasionally, she uses some German words in the conversation and naturally provides explanations.
                                Usually use english for responses.
                                """}]
        self.input_message = input_message
        self.running = False  # 线程运行标志

    def run(self):
        if not self.running:
            self.running = True
            try:
                # 调用 API
                result = self.call_Deepseek_api(self.chat_mode)
                self.api_result.emit(result)  # 发射信号，传递结果
            except Exception as e:
                self.api_result.emit(str(e))  # 如果出错，传递错误信息
            finally:
                self.response_finished.emit()  # 通知线程结束
                self.running = False
        self.quit()  # 退出线程

    # API 调用函数及联网搜索功能
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
    def call_Deepseek_api(self, chat_mode):
        data = self.system_message + self.input_message# + data_end

        try:
            response = client.chat.completions.create(
                model=chat_mode,
                messages=data,
                stream=True,
                temperature=0.9,
                tools = [
                    {
                        "type": "builtin_function",  # <-- 我们使用 builtin_function 来表示 Kimi 内置工具，也用于区分普通 function
                        "function": {
                            "name": "$web_search",
                        },
                    },
                ]
            )
            for chunk in response:
                if chunk.choices:
                    part = chunk.choices[0].delta.content
                    # print(part)
                    self.api_result.emit(part)  # 发射信号，传递部分
                
                
        except Exception as e:
            return f"诶呀我没听清楚，可以请你再说一遍么？" + str(e)


class Frame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Eileen 聊天机器人")
        self.resize(1200, 800)
        # self.setGeometry(100, 100, 800, 600)
        self.setObjectName("catgirl")

        # 设置主题
        self.setStyleSheet("background-color: #F8F0BD;")
        
        self.icon_path = os.path.join(os.path.dirname(__file__), 'images','catcat.jpg')
        self.setWindowIcon(QIcon(self.icon_path))

        self.supertext_card = AssistantCard('')
        # 主窗口布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 10, 50, 10)

        self.text = '~Eileen~'
        self.label = SubtitleLabel(self.text, self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(50)
        main_layout.addWidget(self.label, 0, Qt.AlignTop)

        # 对话框（使用 QScrollArea）
        self.chat_area = SmoothScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_area.setWidget(self.chat_content)
        self.chat_area.enableTransparentBackground()
        self.chat_layout.addStretch(1)
        #self.chat_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        # self.chat_area.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(self.chat_area)

        # 用户输入框和发送按钮
        self.card = InputCard(lambda: self.send_message(CHAT_MODE),self)
        self.input_field = self.card.input_field
        self.card.setBorderRadius(40)
        main_layout.addWidget(self.card, 0, Qt.AlignBottom)

        # 注册函数 `save_data` 在程序退出时执行
        atexit.register(self.save_data)    
        
        # 系统设定
        # self.sys_cnfig = self.system_message("""
        #                                      You will respond in the identity of Eileen, 
        #                                      a cat girl with a lively and generous character, 
        #                                      who likes to think and provide her own thoughts and suggestions to questions. 
        #                                      Occasionally, she uses some German words in the conversation and naturally provides explanations.
        #                                      Usually use english for responses.
        #                                      """)
        # self.send_message("扮演名叫铜钱的英短,猫男语气，简短问候")

        self.memery_path = os.path.join(os.path.dirname(__file__), 'dataSet', 'AI_memery','memery.json')
        self.add_memery = False  # 是否添加新的记忆数据
        self.messages = []
        self.init_messages()  # 读取数据并初始化对话内容

        self.auto_scroll = True  # 自动滚动到底部
    
    def init_messages(self):
        # 读取数据
        try:
            with open(self.memery_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}  # 如果文件不存在或格式错误，初始化为空字典
        data_list = list(data.values())
        if data_list:
            self.messages = data_list[-1]  # 取最后一条对话记录作为初始对话内容
            self.messages = self.messages[-19:]  # 取最近 19 条对话记录作为初始对话内容



    def update_history(self, response):
        self.add_memery = True
        self.messages.append({"role": "assistant", "content": response})
        if len(self.messages) > 19:
            print("超过19条对话记录，删除最早的记录")
            self.messages = self.messages[-19:]

    # 保持数据
    def save_data(self):
        if self.add_memery:
            timestamp = datetime.datetime.now().strftime("%Y%m%d")

            # 读取现有的 JSON 数据
            try:
                with open(self.memery_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}  # 如果文件不存在或格式错误，初始化为空字典

            # 更新或追加数据
            if timestamp in data:
                flag = 0
                for i in range(len(data[timestamp]) - 1, -1, -1):  # 修正循环范围
                    if data[timestamp][i]['content'][0:20] == self.messages[0]['content'][0:20]:
                        data[timestamp].extend(self.messages[len(data[timestamp]) - i:])
                        flag = 1
                        break
                if flag == 0:
                    data[timestamp].extend(self.messages)  # 追加新消息
            else:
                data[timestamp] = self.messages  # 新增日期数据

            # 写回 JSON 文件
            with open(self.memery_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"对话数据已保存到 " + self.memery_path)

    
    # def system_message(self, message):
    #     return [{"role": "system", "content": message}]

    def send_message(self, chat_mode):
        global waiting

        user_input = self.input_field.toPlainText().strip()
        if not user_input or waiting:
            return

        waiting = True  # 标记为等待状态
        self.update_chat_window(user_input, is_ai=False)

        # 记录用户对话内容
        self.messages += [{"role": "user", "content": user_input}]
        self.input_field.clear()

        # 启动工作线程
        worker = ApiWorker(chat_mode, self.messages)
        worker.api_result.connect(self.handle_api_result)
        worker.response_finished.connect(self.finish_response)
        worker.start()  # 启动线程
        
        # 在ai回复前创建好回复卡片，并插入到聊天内容区域
        self.supertext_card = AssistantCardContent('')
        # 添加 card 到聊天内容布局
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.supertext_card, 0, Qt.AlignTop)
        
        # 自动滚动到底部
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())
        
        #worker.wait()  # 等待线程结束
        #waiting = False  # 标记为非等待状态

    def handle_api_result(self, part):
        global waiting

        if part.strip():  # 只处理非空部分
            # 更新显示 AI 回复
            self.supertext_card.card.label.appendText(part)

        # 自动滚动到底部
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())

        # 检测到鼠标滚轮移动则停止
        

        waiting = False  # 标记为非等待状态
    
    def finish_response(self):
        self.update_history(self.supertext_card.card.label._text)  # 记录对话内容
        self.save_data()  # 保存对话数据

    def update_chat_window(self, text, is_ai=True):
        # 创建一个 card 来显示 AI 或用户回复
        if is_ai:
            text_card = AssistantCardContent(text)
        else:
            text_card = UserCardContent(text)
            #self.messages.append(text)  # 记录对话内容
            #self.messages.append(self.supertext_card.card.label._text)  # 记录对话内容

        # 添加 card 到聊天内容布局
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, text_card, 0, Qt.AlignTop)

        # 自动滚动到底部
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())
        

# 重写 TextEdit 类，实现回车键事件
class MyTextEdit(QTextEdit):
    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.callback = callback

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            global waiting
            if not waiting:
                self.handleReturnPressed()
        else:
            super().keyPressEvent(event)

    def handleReturnPressed(self):
        if self.callback is not None:
            self.callback()

class InputCard(ElevatedCardWidget):

    def __init__(self, send_message, parent=None):
        super().__init__(parent)

        # 用户输入框和发送按钮
        input_layout = QHBoxLayout(self)
        input_layout.setContentsMargins(40, 15, 15, 15)
        input_layout.setSpacing(20)
    
        self.input_field = MyTextEdit(send_message)
        self.input_field.setFixedHeight(50)
        self.input_field.setPlaceholderText("Type your message...")
        # self.input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 设置输入框大小策略
        self.input_field.setStyleSheet("QTextEdit {"
                        "background-color: #FFFFFF;"
                        "border-radius: 25px;"    # 设置圆角半径
                        "font-family: 'Comic Sans MS','汉仪奶酪体', sans-serif;"  # 设置字体类型
                        "font-size: 20px;" 
                        "color: #DF667C;"    # 设置字体大小
                        "}")
        
        self.send_button = PrimaryToolButton(FIF.SEND)
        self.send_button.setFixedHeight(50)
        self.send_button.setFixedWidth(50)
        self.send_button.setStyleSheet("QToolButton {background-color: #8E66DF; border-radius: 25px; border: none;}")
        self.send_button.clicked.connect(send_message)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)

# 重写 QLabel 类，实现追加文本功能
class MyLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self._text = text
        self.setText(self._text)  # 初始化显示内容

    def appendText(self, addtext):
        self._text += addtext  # 追加文本
        self.setText(self._text)  # 更新 QLabel 的显示内容


class AssistantCardContent(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout(self))
        self.empty_label = QLabel()
        self.empty_label.setFixedWidth(90)
        self.card = AssistantCard(text)
        self.card.setBorderRadius(25)
        self.layout().addWidget(self.card)
        self.layout().addWidget(self.empty_label)
        

class AssistantCard(ElevatedCardWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        global waiting

        output_layout = QHBoxLayout(self)
        output_layout.setContentsMargins(15, 15, 15, 15)
        
        output_layout.setSpacing(20)

        # 创建 AI 的头像
        avatar_widget = QWidget()
        avatar_widget.setFixedWidth(60)
        avatar_layout = QVBoxLayout(avatar_widget)
        avatar_path = os.path.join(os.path.dirname(__file__), 'images',  'catcat.jpg')
        avatar = AvatarWidget(avatar_path)
        avatar.setRadius(24)
        avatar.setFixedHeight(50)
        avatar.setFixedWidth(50)

        # 文本复制按钮
        copy_button = PrimaryToolButton(FIF.COPY)

        copy_button.setToolTip('copy ✨')
        copy_button.setToolTipDuration(3000)
        # 给按钮安装工具提示过滤器
        copy_button.installEventFilter(ToolTipFilter(copy_button, showDelay=500, position=ToolTipPosition.TOP))

        copy_button.setStyleSheet("QToolButton {background-color: #8E66DF; border-radius: 15px; border: none;}")

        copy_button.setFixedHeight(30)
        copy_button.setFixedWidth(30)
        copy_button.clicked.connect(self.copy_text)

        avatar_layout.addWidget(avatar, 0, Qt.AlignTop)
        avatar_layout.addStretch(1)
        avatar_layout.addWidget(copy_button, 0, Qt.AlignBottom)
        
        output_layout.addWidget(avatar_widget)


        # 创建一个 QLabel 来显示 AI 回复
        self.label = MyLabel(text)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("QLabel {font-size: 24px; font-family: 'Comic Sans MS','汉仪奶酪体', sans-serif; color: #5B5686;}")
        setFont(self.label, 20)
        # label.setStyleSheet("QLabel {font-size: 24px; font-family: Arial;")
        output_layout.addWidget(self.label)

    def copy_text(self):
        """复制文本到剪贴板"""
        clipboard = QApplication.clipboard()

        self_text = self.label.text()  # 获取当前文本内容

        if self_text:  # 确保文本不为空
            clipboard.setText(self_text)  # 复制到剪贴板

            InfoBar.success(
                title='Success',
                content="文本复制成功！",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )

class UserCardContent(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout(self))
        self.empty_label = QLabel()
        self.empty_label.setFixedWidth(90)
        self.card = UserCard(text)
        self.card.setBorderRadius(25)
        self.layout().addWidget(self.empty_label)
        self.layout().addWidget(self.card)


class UserCard(ElevatedCardWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        output_layout = QHBoxLayout(self)
        output_layout.setContentsMargins(15, 15, 15, 15)
        
        output_layout.setSpacing(20)

        # 创建一个 QLabel 来显示 AI 回复及用户对话
        label = QLabel(text)
        label.setAlignment(Qt.AlignRight)
        label.setWordWrap(True)
        label.setStyleSheet("QLabel {font-size: 24px; font-family: 'Comic Sans MS','汉仪奶酪体', sans-serif; color: #DF667C;}")
        setFont(label, 20)
        # label.setStyleSheet("QLabel {font-size: 24px; font-family: Arial;")
        output_layout.addWidget(label)

        # 创建 User 的头像
        avatar_widget = QWidget()
        avatar_widget.setFixedWidth(60)
        avatar_layout = QVBoxLayout(avatar_widget)
        avatar_path = os.path.join(os.path.dirname(__file__), 'images',  'user.jpg')
        avatar = AvatarWidget(avatar_path)
        avatar.setRadius(24)
        avatar.setFixedHeight(50)
        avatar.setFixedWidth(50)
        avatar_layout.addWidget(avatar, 0, Qt.AlignTop)
        avatar_layout.addStretch(1)
        output_layout.addWidget(avatar_widget)  


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Frame()
    w.show()
    app.exec_()