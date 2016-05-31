import sys
import logging
from config import StockConfig
from datetime import datetime
from ebest.xasession import XASession
from ebest.xaquery import XAQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCheckBox
from PyQt5 import uic

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class StockWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = uic.loadUi('stock.ui', self)  # ui load
        self.stockConfig = StockConfig()  # config init

        self.initialize()

        # Logger 초기화
        logHandler = LogHandler(self.view)
        logHandler.setLevel(logging.DEBUG)
        logger.addHandler(logHandler)

        self.session = XASession()

    def initialize(self):
        config = self.stockConfig.load()

        self.view.ipt_login_id.setText(config["user"]["id"])
        self.view.ipt_login_pwd.setText(config["user"]["pwd"])
        self.view.ipt_login_certpwd.setText(config["user"]["certpwd"])
        self.view.ipt_login_acctpwd.setText(config["user"]["acctpwd"])

        self.user = config["user"]
        self.server = config["server"]

        self.view.check_test_acct.setChecked(self.server["host"] == "demo.ebestsec.co.kr")

    def login(self):
        try :
            self.user = {
                "id": self.view.ipt_login_id.text(),
                "pwd": self.view.ipt_login_pwd.text(),
                "certpwd": self.view.ipt_login_certpwd.text(),
                "acctpwd": self.view.ipt_login_acctpwd.text()
            }

            is_login = self.session.login(self.server, self.user)

            if is_login:
                # config파일 생성
                self.stockConfig.save(user=self.user, server=self.server)

                # input들 모두 read only 처리

                # 로그인/로그아웃버튼 처리
                self.view.btn_login.setEnabled(False)
                self.view.btn_logout.setEnabled(True)

                query = XAQuery()
        except Exception as e:
            print(e)

    def logout(self):

        self.session.logout()

        # 로그인/로그아웃버튼 처리
        self.view.btn_login.setEnabled(True)
        self.view.btn_logout.setEnabled(False)

    def change_acct_type(self, is_test_acct):
        self.view.ipt_login_certpwd.setEnabled(not is_test_acct)
        self.view.ipt_login_acctpwd.setEnabled(not is_test_acct)

        if is_test_acct:
            self.server["host"] = "demo.ebestsec.co.kr"

        else:
            self.server["host"] = "hts.ebestsec.co.kr"


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
