# Copyright (C) 2025  <Yijiu Zhao>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# coding:utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (ImageLabel, 
                            InfoBar, InfoBarPosition, RoundMenu, Action)
from qfluentwidgets import FluentIcon as FIF 

class MenuImageLabel(ImageLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def contextMenuEvent(self, event):
        """自定义右键菜单"""
        menu = RoundMenu(self)
        menu.addAction(Action(FIF.COPY, "复制图片",  shortcut="Ctrl+C", triggered=lambda: self.copy_image()))
        menu.exec_(event.globalPos())

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
