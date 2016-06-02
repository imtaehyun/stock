import win32com.client
import pythoncom
from pandas import Series, DataFrame

class XAQueryEvents:
    def __init__(self):
        self.status = 0
        self.code = None
        self.msg = None

    def reset(self):
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
        self.code = str(nMessageCode)
        self.msg = str(szMessage)

    def OnReceiveChartRealData(self, szTrCode):
        """차트지표실시간데이터를수신했을때발생
        szTrCode: TR 명
        """
        print("OnReceiveChartRealData: ", szTrCode)


class XAQuery:
    def __init__(self, req_cd, is_occur=False):
        try:
            self.query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
            self.query.LoadFromResFile("Res/" + req_cd + ".res")
            self.req_cd = req_cd
            self.is_occur = is_occur
        except Exception as e:
            print(e)

    def request(self, input, output, isNext=False):

        try:
            # if not input:
            #     input = {"InBlock": {}}
            print("input: ", input)
            print("output: ", output)

            # input data setting
            for k, v in input.items():
                for k2, v2 in v.items():
                    print("{} {} : {}".format(self.req_cd + k, k2, v2))
                    self.query.SetFieldData(self.req_cd + k, k2, 0, v2)

            req_result = self.query.Request(isNext)

            if req_result < 0:
                print("request fail: ", req_result)
                return False

            while self.query.status == 0:
                pythoncom.PumpWaitingMessages()

            self.output = {}

            for k, v in output.items():
                self.output[k] = {}
                for p in v:
                    self.output[k][p] = None
            print("result: ", self.output)

            for k, v in self.output.items():
                count = self.query.GetBlockCount(self.req_cd + k)
                print("count: ", count)
                for i in range(count):
                    for col in v.keys():
                        v[col] = self.query.GetFieldData(self.req_cd + k, col, i)
                    print("result: ", self.output)


            return self.output

        except Exception as e:
            print(e)
