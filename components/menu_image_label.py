# coding:utf-8
import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (ImageLabel, 
                            InfoBar, InfoBarPosition, RoundMenu, Action)
from qfluentwidgets import FluentIcon as FIF 

class MenuImageLabel(ImageLabel):

    # 新增带路径参数的信号
    clicked_with_path = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.img_path = None

    def contextMenuEvent(self, event):
        """自定义右键菜单"""
        menu = RoundMenu()
        menu.addAction(Action(FIF.COPY, "复制图片",  shortcut="Ctrl+C", triggered=lambda: self.copy_image()))
        menu.exec_(event.globalPos())

    def mousePressEvent(self, event: QMouseEvent):
            
        if event.button() == Qt.RightButton:
            self.contextMenuEvent(event)

        super().mousePressEvent(event)

    def copy_image(self):
        """复制图片到剪贴板"""
        clipboard = QApplication.clipboard()
        current_pixmap = self.pixmap()  # 获取当前图片
        if current_pixmap:
            clipboard.setPixmap(current_pixmap)  # 复制到剪贴板
            
            InfoBar.success(
                title='Success',
                content="图片复制成功！",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
    
