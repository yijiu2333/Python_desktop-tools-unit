from PyQt5.QtCore import Qt, QUrl, QRunnable, QThread, QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme, IconWidget, TextEdit, 
                            PrimaryPushButton, InfoBar, InfoBarPosition
                            )
from qfluentwidgets import FluentIcon as FIF 

import sys
import os

class SveNote(QRunnable):
    def __init__(self, text, file_path):
        super().__init__()
        self.text = text
        self.file_path = file_path

    def run(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write(self.text)
            print(f"笔记已保存到 {self.file_path}")
        except Exception as e:
            print(f"保存笔记时出错: {e}")

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        main_layout = QVBoxLayout(self)
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName('note_pad')
        self.resize(600,400)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(10)

        # inital the file path
        self.file_path = os.path.join(os.path.dirname(__file__), 'dataSet', '备忘录.txt')

        #inital the thread pool
        self.thread_pool = QThreadPool()

        # inital the title
        self.title = QWidget()
        self.title_layout = QHBoxLayout(self.title)

        self.label = SubtitleLabel('备忘录')
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(50)

        self.iconWidget = IconWidget(FIF.BOOK_SHELF)
        self.iconWidget.setFixedWidth(20)
        self.iconWidget.setFixedHeight(20)
        
        self.title_layout.addWidget(self.iconWidget)
        self.title_layout.addWidget(self.label)
        self.title_layout.addStretch(1)

        main_layout.addWidget(self.title)

        # inital the notes
        self.note_book = TextEdit()
        self.note_book.setFixedWidth(600)
        self.note_book.setContentsMargins(10,10,10,10)
        self.load_note()
        self.note_book.textChanged.connect(lambda: self.save_button.setEnabled(True))
        main_layout.addWidget(self.note_book)

        # inital the save button
        self.save_button = PrimaryPushButton(FIF.SAVE, 'SAVE')
        self.save_button.clicked.connect(self.save_note)
        self.save_button.setEnabled(False)
        self.save_button.setFixedHeight(40)
        self.save_button.setFixedWidth(100)
        main_layout.addWidget(self.save_button)

    def showEvent(self, event):
        super().showEvent(event)
        self.move_scrollbar_to_bottom()  # 页面显示时自动滚动到底部
        
    def move_scrollbar_to_bottom(self):
        scrollbar = self.note_book.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def save_note(self):
        note_text = self.note_book.toPlainText().strip()
        if not note_text:
            print("笔记内容为空，无法保存。")
            return

        # 创建异步任务
        worker = SveNote(note_text, self.file_path)
        self.thread_pool.start(worker)

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
            self.note_book.setPlainText(note_text)
            print(f"笔记已加载到 {self.file_path}")
        except Exception as e:
            print(f"加载笔记时出错: {e}")

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Frame()
    w.show()
    app.exec_()