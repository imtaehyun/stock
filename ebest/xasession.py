import win32com.client
import pythoncom

class XASessionEvents:
    def __init__(self):
        self.code = -1
        self.msg = None

    def reset(self):
        self.code = -1
        self.msg = None

    def OnLogin(self, code, msg):
        self.code = str(code)
        self.msg = str(msg)

    def OnDisconnect(self):
        print("OnDisconnect")

class XASession:

    def __init__(self):
        self.session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents) # XASession 초기화

    def login(self, server, user):
        """로그인"""
        print("server: {}:{}".format(server["host"], server["port"]))
        print("user: ", str(user))

        connectResult = self.session.ConnectServer(server["host"], server["port"])

        if not connectResult:
            print("Connect Server Error: ", self.session.GetLastError())
            return False

        loginResult = self.session.Login(user["id"], user["pwd"], user["certpwd"], 0, False)

        if not loginResult:
            print("Login Error: ", loginResult, self.session.GetLastError())
            return False

        while self.session.code == -1:
            pythoncom.PumpWaitingMessages()

        if self.session.code == "0000":
            print("로그인 성공")
            return True
        else:
            print("로그인 실패 : [{}] {}".format(self.session.code, self.session.msg))
            return False

    def logout(self):
        """로그아웃"""
        print("로그아웃")
        self.session.DisconnectServer()

    def account(self):
        """사용자 계좌번호 리스트 가져오기"""
        acc = []
        for i in range(self.session.GetAccountListCount()):
            acc.append({
                "no": self.session.GetAccountList(i), # 계좌번호
                "name": self.session.GetAccountName(self.session.GetAccountList(i)), # 계좌명
                "detail_name": self.session.GetAcctDetailName(self.session.GetAccountList(i)) #계좌 상세명
            })
        return acc
