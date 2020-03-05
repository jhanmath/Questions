# -*- coding: utf-8 -*-
import sys
import os

# from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QApplication
from mainwindow import * # 这个是main   主窗口

if __name__ == '__main__':
    # Many browsers for security reason disable the loading of local files, but you can enable that capability with:
    sys.argv.append("--disable-web-security")
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./icon.svg"))
    main_ui = MainWindow()
    main_ui.show()
    sys.exit(app.exec_())
