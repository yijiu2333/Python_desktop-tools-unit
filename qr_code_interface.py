# coding:utf-8
import sys
import os

from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (SubtitleLabel, setFont, FlowLayout, PlainTextEdit, 
                            CardWidget, PrimaryPushButton, IconWidget, SmoothScrollArea, PushButton, InfoBar, InfoBarPosition)
from qfluentwidgets import FluentIcon as FIF 

import components.qr_code_creater as qr_code_creater
import components.menu_image_label as menu_image_label

# init global variables
filename = 'default'

class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName('qr-code-generator-frame')

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout_title = QHBoxLayout()
        self.hBoxLayout_title.setContentsMargins(15, 0, 0, 0)

        self.scrollArea = SmoothScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        
        self.scrollArea.resize(1500, 500)

        self.view = QWidget()

        self.scrollArea.setWidget(self.view)
        self.scrollArea.enableTransparentBackground()
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)


        self.flowLayout_content = FlowLayout(self.view, needAni=True)# enable animation

        # 自定义动画参数
        self.flowLayout_content.setAnimation(250, QEasingCurve.OutQuad)

        self.vBoxLayout.addLayout(self.hBoxLayout_title)
        self.vBoxLayout.addWidget(self.scrollArea, 1)

        self.setWindowTitle('QR Code Generator')

        self.initTitle(self.hBoxLayout_title)
        self.initFlowLayout(self.flowLayout_content)


    # init title
    def initTitle(self, layout: QHBoxLayout):
        self.text = '二维码生成器'
        self.label = SubtitleLabel(self.text, self)

        # self.icon_path = os.path.join(os.path.dirname(__file__), 'images', 'icon', 'example_qr.png')
        self.iconWidget = IconWidget(FIF.QRCODE)
        self.iconWidget.setFixedWidth(20)
        self.iconWidget.setFixedHeight(20)
        layout.addWidget(self.iconWidget, 0, Qt.AlignLeft)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedHeight(50)
        layout.addWidget(self.label, 1, Qt.AlignLeft)

    # init FlowLayout input
    def initFlowLayout(self, layout: FlowLayout):
        
        self.imagecard = QRCard()
        self.imagecard.setFixedWidth(500)
        self.imagecard.setFixedHeight(500)
        
        self.textcard = ContentCard(self.imagecard)
        self.textcard.setFixedWidth(500)
        self.textcard.setFixedHeight(500)

        layout.addWidget(self.textcard)
        layout.addWidget(self.imagecard)


# 二维码自定义卡片
class QRCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setObjectName('qr-code-generator-card')
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout_title = QHBoxLayout()
        self.hBoxLayout_image = QHBoxLayout()
        self.hBoxLayout_button = QHBoxLayout()

        self.vBoxLayout.setContentsMargins(10, 10, 10, 10)

        self.hBoxLayout_title.setContentsMargins(35, 0, 0, 0)
        self.hBoxLayout_image.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout_button.setContentsMargins(0, 0, 40, 0)

        self.vBoxLayout.addLayout(self.hBoxLayout_title)
        self.vBoxLayout.addLayout(self.hBoxLayout_image)
        self.vBoxLayout.addLayout(self.hBoxLayout_button)
        
        self.title = SubtitleLabel('二维码生成区域', self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedHeight(50)

        self.hBoxLayout_title.addWidget(self.title, 1, Qt.AlignLeft)
        
        # show QR code
        self.qr_code = SmoothScrollArea()
        self.qr_code.setWidgetResizable(True)
        self.qr_code.setFrameShape(QFrame.NoFrame)
        
        self.qr_code.resize(400, 350)

        # 自定义平滑滚动动画
        self.qr_code.setScrollAnimation(Qt.Vertical, 350, QEasingCurve.OutQuint)
        self.qr_code.setScrollAnimation(Qt.Horizontal, 400, QEasingCurve.OutQuint)

        self.qr_code.enableTransparentBackground()
        self.qr_code.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.qr_code.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.qr_code.setContentsMargins(0, 0, 0, 0)

        self.qr_code.setFixedHeight(350)
        self.qr_code.setFixedWidth(400)

        self.hBoxLayout_image.addWidget(self.qr_code, 1, Qt.AlignCenter)

        self.button = PushButton(FIF.COPY, '复制二维码')
        self.hBoxLayout_button.addWidget(self.button, 0, Qt.AlignRight)

    def showQRCode(self):
        global filename
        # 移除当前的内部容器
        self.old_container = self.qr_code.takeWidget()
        if self.old_container:
            self.old_container.deleteLater()  # 删除旧的容器

        self.qr_code_image_path = os.path.join(os.path.dirname(__file__), 'images', 'QR', filename)
        print(self.qr_code_image_path)
        self.qr_code_view = menu_image_label.MenuImageLabel(self.qr_code_image_path)
        self.qr_code_view.setFixedHeight(350)
        self.qr_code_view.setFixedWidth(400)
        self.qr_code_view.setBorderRadius(8, 8, 8, 8)
        self.qr_code.setWidget(self.qr_code_view)

        # 发送系统提醒
        InfoBar.success(
            title='Success',
            content="新的二维码已生成！",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

        # 复制二维码
        self.button.clicked.connect(lambda: self.copyQRCode())

    def copyQRCode(self):
        """复制图片到剪贴板"""
        clipboard = QApplication.clipboard()  # 获取系统剪贴板
        current_pixmap = self.qr_code_view.pixmap()  # 获取当前图片
        if current_pixmap:
            clipboard.setPixmap(current_pixmap)  # 复制到剪贴板

        InfoBar.success(
            title='Success',
            content="二维码复制成功！",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,
            parent=self
        )

# 输入框的自定义卡片
class ContentCard(CardWidget):
    def __init__(self, qrcard: QRCard, parent=None):
        super().__init__(parent)

        self.qrcard = qrcard
        self.setObjectName('qr-code-generator-card')
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout_title = QHBoxLayout()
        self.hBoxLayout_text = QHBoxLayout()
        self.hBoxLayout_button = QHBoxLayout()

        self.hBoxLayout_title.setContentsMargins(35, 0, 0, 0)
        self.hBoxLayout_text.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout_button.setContentsMargins(0, 0, 40, 0)

        self.vBoxLayout.addLayout(self.hBoxLayout_title)
        self.vBoxLayout.addLayout(self.hBoxLayout_text)
        self.vBoxLayout.addLayout(self.hBoxLayout_button)
        
        self.title = SubtitleLabel('请在下方输入你要生成二维码的文字：', self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedHeight(50)
        
        self.hBoxLayout_title.addWidget(self.title, 1, Qt.AlignLeft)

        self.text = 'Enter the text you want to generate QR Code for:'
        self.textEdit = PlaceholderTextEdit(self.text)
        # self.textEdit.setPlainText()
        # self.textEdit.setReadOnly(True)
        self.textEdit.setFixedHeight(350)
        self.textEdit.setFixedWidth(400)
        self.hBoxLayout_text.addWidget(self.textEdit, 1, Qt.AlignCenter)

        self.button = PrimaryPushButton(FIF.UPDATE, '生成二维码')

        # 按钮点击事件
        if self.textEdit.toPlainText():
            self.button.clicked.connect(lambda: self.generateQRCode(self.textEdit.toPlainText(),self.qrcard))

        self.hBoxLayout_button.addWidget(self.button, 0, Qt.AlignRight)

    def generateQRCode(self, textdata, qrcard):
        global filename
        self.data = textdata
        self.qrcard = qrcard

        if self.data != 'Enter the text you want to generate QR Code for:':
            filename = textdata.replace(' ', '_') + '.png'
            qr_code_creater.create_qr_code(self.data, filename)

            self.qrcard.showQRCode()
        else:
            InfoBar.warning(
            title='警告',
            content="请输入文字内容！",
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=self
        )
        

# 自定义文本框,实现占位符功能
class PlaceholderTextEdit(PlainTextEdit):
    def __init__(self, placeholder_text, parent=None):  
        super().__init__(parent)
        self.placeholder_text = placeholder_text
        self.is_placeholder = True  # 标记是否显示占位符
        self.setPlaceholderText()

    def setPlaceholderText(self):
        """设置占位符文本"""
        self.setPlainText(self.placeholder_text)
        self.is_placeholder = True
        self.setStyleSheet("color: gray;")  # 设置占位符颜色为灰色

    def clearPlaceholderText(self):
        """清空占位符文本"""
        self.clear()
        self.setPlainText('')
        self.is_placeholder = False
        self.setStyleSheet("")  # 恢复默认样式

    def focusInEvent(self, event):
        """当控件获得焦点时"""
        if self.is_placeholder:
            self.clearPlaceholderText()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """当控件失去焦点时"""
        if self.toPlainText() == "" and self.is_placeholder is False:
            self.setPlaceholderText()
        super().focusOutEvent(event)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Frame()
    w.show()
    app.exec_()