from PyQt5.QtCore import Qt, QUrl, QRunnable, QThread, QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme, IconWidget, TextEdit, 
                            PrimaryPushButton, InfoBar, InfoBarPosition, SmoothScrollArea,
                            FlowLayout, ElevatedCardWidget
                            )
from qfluentwidgets import FluentIcon as FIF 

import sys
import os
import json

file_path = os.path.join(os.path.dirname(__file__), "dataSet", "notes.json")

# 加载便签
def load_notes(filename=file_path):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# 保存便签
def save_notes(notes, filename=file_path):
    with open(filename, "w") as file:
        json.dump(notes, file, indent=2)

# 删除便签
def delete_note(note_id, filename=file_path):
    notes = load_notes(filename)
    # 过滤掉指定 ID 的便签
    updated_notes = [note for note in notes if note["id"] != note_id]
    save_notes(updated_notes, filename)

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        main_layout = QVBoxLayout(self)
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName('idea_set')
        self.resize(600,400)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(10)

        # inital the title
        self.title = QWidget()
        self.title_layout = QHBoxLayout(self.title)

        self.label = SubtitleLabel('breaking ideas')
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(50)

        self.iconWidget = IconWidget(FIF.IOT)
        self.iconWidget.setFixedWidth(20)
        self.iconWidget.setFixedHeight(20)
        
        self.title_layout.addWidget(self.iconWidget)
        self.title_layout.addWidget(self.label)
        self.title_layout.addStretch(1)

        main_layout.addWidget(self.title)

        # inital the content
        self.scroll_area = SmoothScrollArea()
        self.content = QWidget()
        self.scroll_area.setWidget(self.content)
        main_layout.addWidget(self.scroll_area)

        # inital the content
        self.content_layout = FlowLayout(self.content, needAni=True)
        self.content_layout.setSpacing(10)

        self.label = SubtitleLabel('hello world')
        self.content_layout.addWidget(self.label)
        
        self.card = IdeaCard('hello world')
        self.content_layout.addWidget(self.card)
        
        
class IdeaCard(ElevatedCardWidget):
    def __init__(self,text, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('idea_card')
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10,10,10,10)
        self.layout.setSpacing(10)

        self.label = SubtitleLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(80)

        self.delete_btn = PrimaryPushButton('delete')
        self.delete_btn.clicked.connect(delete_note)
        self.delete_btn.setFixedWidth(80)
        self.delete_btn.setFixedHeight(30)
        self.delete_btn.setObjectName('delete_btn')

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.delete_btn)
        
        



if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Frame()
    w.show()
    app.exec_()
