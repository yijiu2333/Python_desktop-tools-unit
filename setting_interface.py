# Copyright (C) 2025  <Yijiu Zhao>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# coding:utf-8

from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (SubtitleLabel, setFont, IconWidget, SmoothScrollArea,
                            SettingCardGroup, OptionsSettingCard, )
from qfluentwidgets import FluentIcon as FIF 

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName('setting-interface')
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)

        # 标题栏
        self.hBoxLayout_title = QHBoxLayout()
        self.vBoxLayout.addLayout(self.hBoxLayout_title)
        
        self.initTitle(self.hBoxLayout_title)

        # 内容
        self.hBoxLayout_content = QHBoxLayout()
        self.vBoxLayout.addLayout(self.hBoxLayout_content)

        self.initContent(self.hBoxLayout_content)


    

        # init title
    def initTitle(self, layout: QHBoxLayout):
        self.iconWidget = IconWidget(FIF.SETTING)
        self.iconWidget.setFixedWidth(20)
        self.iconWidget.setFixedHeight(20)
        layout.addWidget(self.iconWidget, 0, Qt.AlignLeft)

        self.label = SubtitleLabel('设置及配置', self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(50)
        layout.addWidget(self.label, 1, Qt.AlignLeft)


        # 内容初始化
    def initContent(self, layout: QHBoxLayout):
        # 滚动区域
        self.scrollArea = SmoothScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QFrame.NoFrame)

        self.scrollArea.resize(400, 1400)

        self.scrollArea.setScrollAnimation(Qt.Vertical, 400, QEasingCurve.OutQuint)
        self.scrollArea.setScrollAnimation(Qt.Horizontal, 400, QEasingCurve.OutQuint)

        self.scrollArea.enableTransparentBackground()
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setContentsMargins(10, 10, 10, 10)

        #self.scrollArea.setFixedHeight(350)
        #self.scrollArea.setFixedWidth(400)

        self.layout.addWidget(self.scrollArea, 1, Qt.AlignCenter)

        # 设置卡片组
        self.settingCardGroup = SettingCardGroup()
        self.scrollArea.setWidget(self.settingCardGroup)

        # 设置卡片组内容
        card = OptionsSettingCard(
            qconfig.themeMode,
            FIF.BRUSH,
            "应用主题",
            "调整你的应用外观",
            texts=["浅色", "深色", "跟随系统设置"]
        )