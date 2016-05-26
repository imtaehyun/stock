#-*- coding: utf-8 -*-
import sys

from kiwoom import Kiwoom
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextBrowser, QListWidget, QTableView, QTableWidget
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel, QVariant, Qt
from PyQt5 import uic

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.kiwoom = Kiwoom(self.view)
        # self.kiwoom.login()

    def initUI(self):
        self.view = uic.loadUi('StockWindow.ui', self)

    # @pyqtSlot()
    # def login_clicked(self):
    #     self.kiwoom.login()

    @pyqtSlot()
    def get_info(self):
        self.kiwoom.get_login_info()

    @pyqtSlot()
    def get_stock_list(self):
        stock_list = self.kiwoom.get_jongmok_code()
        for stock in stock_list:
            self.view.listStock.addItem(stock['code'])

    @pyqtSlot()
    def jongmok_selected(self):
        self.view.tableView = QTableWidget
        self.view.tableView
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
