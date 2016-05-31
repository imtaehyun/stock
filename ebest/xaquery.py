import win32com.client
import pythoncom

class XAQueryEvents:
    def __init__(self):
        self.status = 0
        self.code = None
        self.msg = None

    def OnReceiveData(self, szTrCode):
        """서버로부터데이터를수신했을때발생
        szTrCode: TR 명
        """
        print("OnReceiveData: ", szTrCode)
        self.status = 1

    def OnReceiveMessage(self, bIsSystemError, nMessageCode, szMessage):
        """서버로부터메시지를수신했을때발생
        bIsSystemError: TRUE면시스템오류, FALSE면그외오류
        nMessageCode: 메시지코드
        메시지코드의개별정보는홈페이지에공지되어있습니다.
        TR Code가10자리인TR에한해서에러코드의범위는다음과같습니다.
        > 0000~0999 : 정상(ex ) 0040 : 매수주문이완료되었습니다.)
        > 1000~7999 : 업무오류메시지(1584 : 매도잔고가부족합니다.)
        > 8000~9999 : 시스템에러메시지
        szMessage: 메시지
        """
        print("OnReceiveMessage: ", bIsSystemError, nMessageCode, szMessage)

    def OnReceiveChartRealData(self, szTrCode):
        """차트지표실시간데이터를수신했을때발생
        szTrCode: TR 명
        """
        pass

class XAQuery:

    def __init__(self):
        try:
            self.query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
            self.query.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1102.res"
            self.query.SetFieldData("t1102InBlock", "shcode", 0, "078020")
            self.query.Request(0)

            while self.query.status == 0:
                pythoncom.PumpWaitingMessages()
            name = self.query.GetFieldData("t1102OutBlock", "hname", 0)
            price = self.query.GetFieldData("t1102OutBlock", "price", 0)
            print(name)
            print(price)
        except Exception as e:
            print(e)