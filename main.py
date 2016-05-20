import sys

from kiwoom import Kiwoom
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QAxContainer import QAxWidget


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.kiwoom = Kiwoom()
        self.kiwoom.login()

    def initUI(self):
        self.setWindowTitle("키움증권 테스트")
        self.setGeometry(300, 300, 300, 150)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
