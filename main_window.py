# Copyright (C) 2025  <Yijiu Zhao>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# coding:utf-8
import sys
import os

from PyQt5.QtCore import Qt, QEventLoop, QTimer, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (NavigationItemPosition, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF 

import frame # type: ignore # import the frame module
import qr_code_interface # type: ignore # import the qr_code_interface module
import note_pad_interface # type: ignore # import the note_pad_interface module
import ai_catgirl_interface # type: ignore # import the ai_catgirl_interface module


class Window(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = frame.Frame('Home Interface', self)
        # self.homepage.setObjectName("homepage")
        self.catgirlInterface = ai_catgirl_interface.Frame(self)
        self.notepadInterface = note_pad_interface.Frame(self)
        self.settingInterface = frame.Frame('Setting Interface', self)
        self.qrcodeInterface = qr_code_interface.Frame(self)

        self.initSplashScreen()

        self.initNavigation()
        self.initWindow()

    # splash screen
    def initSplashScreen(self):
        # Initialize the window size
        self.resize(1200, 800)
    
        # set window size and position
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        
        # Center the window on the screen
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    
        # Load splash screen image icon
        self.splashScreen_image = os.path.join(os.path.dirname(__file__), 'images','icon','splash_icon.png')
        self.image = QIcon(self.splashScreen_image)
        self.setWindowIcon(self.image)
    
        # Create and display the splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(1020, 1020))
    
        # Show the main window
        self.show()
    
        # Create sub-interface
        self.createSubInterface()
    
        # Close the splash screen
        self.splashScreen.finish()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)
        loop.exec()


    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.addSubInterface(self.catgirlInterface, FIF.HELP, 'Catgirl Eileen')
        self.addSubInterface(self.notepadInterface, FIF.BOOK_SHELF, 'Note pad')
        self.addSubInterface(self.qrcodeInterface, FIF.QRCODE, 'QR code')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # NOTE: enable acrylic effect, user can  go back to the previous interface by clicking the top left corner
        self.navigationInterface.setAcrylicEnabled(True)
    
    def initWindow(self):
        self.setWindowTitle('宇心老婆天下第一可爱！')

        # set window icon (for both window and appleos)
        self.icon_path = os.path.join(os.path.dirname(__file__), 'images','icon','home_icon.jpg')
        self.setWindowIcon(QIcon(self.icon_path))
        self.resize(1200, 800)

        # set window size and position
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.setContentsMargins(0, 0, 0, 0)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()