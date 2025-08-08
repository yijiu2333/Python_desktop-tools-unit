# coding:utf-8
import sys
import os

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, FluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, InfoBadge,
                            InfoBadgePosition, FluentBackgroundTheme, IconWidget)
from qfluentwidgets import FluentIcon as FIF 

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName('gallery')
        
        main_layout = QVBoxLayout(self)
        self.resize(600,400)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(10)

        # inital the folder path
        self.folder_path = os.path.join(os.path.dirname(__file__), 'images', 'paintings')

        # inital the title
        self.title = QWidget()
        self.title_layout = QHBoxLayout(self.title)

        self.label = SubtitleLabel('画廊')
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(50)

        self.iconWidget = IconWidget(FIF.BOOK_SHELF)
        self.iconWidget.setFixedWidth(20)
        self.iconWidget.setFixedHeight(20)
        
        self.title_layout.addWidget(self.iconWidget)
        self.title_layout.addWidget(self.label)
        self.title_layout.addStretch(1)

        main_layout.addWidget(self.title, 1, Qt.AlignTop)

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Frame()
    w.show()
    app.exec_()