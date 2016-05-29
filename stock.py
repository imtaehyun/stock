import sys
import logging
from datetime import datetime
from ebest.xasession import XASession
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCheckBox
from PyQt5 import uic
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StockWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.server = {
            "address": "hts.ebestsec.co.kr",
            "port": 20001,
            "type": 0
        }

        self.init_ui()

        # Logger 초기화
        logHandler = LogHandler(self.view)
        logHandler.setLevel(logging.DEBUG)
        logger.addHandler(logHandler)

        self.session = XASession()


    def init_ui(self):
        self.view = uic.loadUi('stock.ui', self)

        self.view.check_test_acct.setChecked(True)
        self.view.btn_logout.setEnabled(False)


    def login(self):
        # self.view.ipt_login_id = QLineEdit()
        self.user = {
            "id": self.view.ipt_login_id.text(),
            "pwd": self.view.ipt_login_pwd.text(),
            "certpwd": self.view.ipt_login_certpwd.text(),
            "acctpwd": self.view.ipt_login_acctpwd.text()
        }

        is_login = self.session.login(self.server, self.user)

        if is_login:
            self.view.btn_login.setEnabled(False)
            self.view.btn_logout.setEnabled(True)

    def logout(self):

        self.session.logout()

        self.view.btn_login.setEnabled(True)
        self.view.btn_logout.setEnabled(False)

    def change_acct_type(self, is_test_acct):
        self.view.ipt_login_certpwd.setEnabled(not is_test_acct)
        self.view.ipt_login_acctpwd.setEnabled(not is_test_acct)

        if is_test_acct:
            self.server["address"] = "demo.ebestsec.co.kr"

        else:
            self.server["address"] = "hts.ebestsec.co.kr"


class LogHandler(logging.Handler):
    def __init__(self, view):
        logging.Handler.__init__(self)
        self.view = view

    def emit(self, record):
        now = datetime.now()
        message = "[{level}] {time} - {msg}".format(time=str(now), level=record.levelname, msg=record.msg)
        print(message)
        self.view.log.append(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = StockWindow()
    myWindow.show()
    app.exec_()
