import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QAxContainer import QAxWidget


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.CommConnect()
        self.kiwoom.OnEventConnect[int].connect(self.onEventConnect)


    def initUI(self):
        self.setWindowTitle("키움증권 테스트")
        self.setGeometry(300, 300, 300, 150)


    def onEventConnect(self, errCode):
        if errCode == 0:
            self.statusBar().showMessage("Connected")
        else:
            self.statusBar().showMessage("Not Connected")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
