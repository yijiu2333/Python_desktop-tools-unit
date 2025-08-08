# coding:utf-8
import sys
import os
from PIL import Image

from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy
from qfluentwidgets import (SubtitleLabel, setFont, SmoothScrollArea,
                            IconWidget, FlowLayout)
from qfluentwidgets import FluentIcon as FIF 

from tqdm import tqdm

import components.menu_image_label as menu_image_label

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

        main_layout.addWidget(self.title)

        # inital the gallery scroll area
        self.scroll_area = SmoothScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # self.scroll_area.setMinimumHeight(500)

        # inital the gallery items
        self.galley = QWidget()
        self.gallery_layout = FlowLayout(self.galley, needAni = True)
        # set the animation duration and easing curve
        self.gallery_layout.setAnimation(250, QEasingCurve.OutQuart)
        
        self.gallery_layout.setContentsMargins(30,30,30,30)
        self.gallery_layout.setVerticalSpacing(20)
        self.gallery_layout.setHorizontalSpacing(10)
        
        self.scroll_area.setWidget(self.galley)
        main_layout.addWidget(self.scroll_area)

        # add the gallery items
        self.addGalleryItems()

        # initial the gallery items click event

    def addGalleryItems(self):
        for file in tqdm(os.listdir(self.folder_path)):
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
                image_path = os.path.join(self.folder_path, file)
                img = Image.open(image_path)
                width, height = img.size 
                image = menu_image_label.MenuImageLabel(image_path)
                image.clicked.connect(lambda p = image_path: self.click_image(p))
                image.setFixedHeight(200)
                image.setFixedWidth(200 * width // height)
                self.gallery_layout.addWidget(image)
    
    def click_image(self, path):
        image = menu_image_label.MenuImageLabel(path)
        image.setParent(self)
        
        img = Image.open(path)
        width, height = img.size 

        image.setFixedHeight(600)
        image.setFixedWidth(600 * width // height)

        w, h = (self.width() - image.width()) // 2, (self.height() - image.height()) // 2
        image.move(w, h)
        image.show()
        
        image.clicked.connect(lambda: image.close())


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    w = Frame()
    w.show()
    app.exec_()        