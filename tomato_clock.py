import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer


def show_popup(message):
    QMessageBox.information(None, "提醒", message)


def main():
    app = QApplication(sys.argv)

    def reminder():
        show_popup("25分钟过去了，请注意休息！")
        QTimer.singleShot(5 * 60 * 1000, focus)  # 5分钟后调用 focus 函数

    def focus():
        show_popup("5分钟过去了，开始专注！")
        QTimer.singleShot(25 * 60 * 1000, reminder)  # 25分钟后调用 reminder 函数

    show_popup("开始计时！")
    while True:
        # 启动第一个提醒
        QTimer.singleShot(25 * 60 * 1000, reminder)  # 25分钟后调用 reminder 函数
        QTimer.singleShot(5 * 60 * 1000, focus)  # 5分钟后调用 focus 函数

    # 启动事件循环
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
