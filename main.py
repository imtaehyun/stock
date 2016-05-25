#-*- coding: utf-8 -*-
import sys

from kiwoom import Kiwoom
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTextBrowser, QListWidget
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import pyqtSlot, QAbstractTableModel, QVariant, Qt
from PyQt5 import uic

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.kiwoom = Kiwoom(self.view)
        self.kiwoom.login()

    def initUI(self):
        self.view = uic.loadUi('StockWindow.ui', self)

        self.tabledata = [['1', '1'],['2','2']]
        header = ['date', 'time']
        tm = MyTableModel(self.tabledata, header, self)
        self.view.tableView.setModel(tm)

    @pyqtSlot()
    def login_clicked(self):
        self.kiwoom.login()

    @pyqtSlot()
    def get_info(self):
        login_info = self.kiwoom.get_login_info()
        self.view.logBrowser.append(str(login_info));

    @pyqtSlot()
    def get_stock_list(self):
        stock_list = self.kiwoom.get_jongmok_code()
        for stock in stock_list:
            self.view.listStock.addItem(stock['code'])

    @pyqtSlot()
    def jongmok_selected(self, item):

        pass

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
