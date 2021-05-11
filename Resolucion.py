import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
import os

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
qapp = QApplication(sys.argv)
print(qapp.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling))