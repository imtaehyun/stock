import sys
import logging
from pprint import pprint

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QAxContainer import QAxWidget

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# streamHandler = logging.StreamHandler()
# streamHandler.setFormatter(formatter)
# logger.addHandler(streamHandler)


class Kiwoom():
    def __init__(self):

        # 키움증권API OCX Instance 생성
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        # event handler 등록
        self.kiwoom.OnReceiveTrData[str, str, str, str, str, int, str, str, str].connect(self.OnReceiveTrData)
        self.kiwoom.OnReceiveRealData[str, str, str].connect(self.OnReceiveRealData)
        self.kiwoom.OnReceiveMsg[str, str, str, str].connect(self.OnReceiveMsg)
        self.kiwoom.OnReceiveChejanData[str, int, str].connect(self.OnReceiveChejanData)
        self.kiwoom.OnEventConnect[int].connect(self.OnEventConnect)
        self.kiwoom.OnReceiveRealCondition[str, str, str, str].connect(self.OnReceiveRealCondition)
        self.kiwoom.OnReceiveTrCondition[str, str, str, int, int].connect(self.OnReceiveTrCondition)
        self.kiwoom.OnReceiveConditionVer[int, str].connect(self.OnReceiveConditionVer)


### Event Handler

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        """OnReceiveTrData: 서버통신 후 데이터를 받은 시점을 알려준다.
        입력값
        sScrNo . 화면번호
        sRQName . 사용자구분 명
        sTrCode . Tran 명
        sRecordName . Record 명
        sPreNext . 연속조회 유무
        nDataLength . 1.0.0.1 버전 이후 사용하지 않음.
        sErrorCode . 1.0.0.1 버전 이후 사용하지 않음.
        sMessage . 1.0.0.1 버전 이후 사용하지 않음.
        sSplmMsg - 1.0.0.1 버전 이후 사용하지 않음.

        비고
        sRQName . CommRqData의 sRQName과 매핑되는 이름이다.
        sTrCode . CommRqData의 sTrCode과 매핑되는 이름이다.
        """
        logger.debug('OnReceiveTrData: ', dict(sScrNo=sScrNo, sRQName=sRQName, sTrCode=sTrCode, sRecordName=sRecordName, sPreNext=sPreNext, nDataLength=nDataLength, sErrorCode=sErrorCode, sMessage=sMessage, sSplmMsg=sSplmMsg))
        self.CommGetData(sTrCode, "", sRQName, 0, "종목명")

    def OnReceiveRealData(self, sJongmokCode, sRealType, sRealData):
        """OnReceiveRealData: 실시간데이터를 받은 시점을 알려준다.

        입력값
        sJongmokCode . 종목코드
        sRealType . 리얼타입
        sRealData . 실시간 데이터전문
        """
        logger.debug('OnReceiveRealData: ', dict(sJongmokCode=sJongmokCode, sRealType=sRealType, sRealData=sRealData))

    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        """OnReceiveMsg: 서버통신 후 메시지를 받은 시점을 알려준다.
        입력값
        sScrNo . 화면번호
        sRQName . 사용자구분 명
        sTrCode . Tran 명
        sMsg . 서버메시지

        비고
        sScrNo . CommRqData의 sScrNo와 매핑된다.
        sRQName . CommRqData의 sRQName 와 매핑된다.
        sTrCode . CommRqData의 sTrCode 와 매핑된다.
        """
        logger.debug(sScrNo, sRQName, sTrCode, sMsg)

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        """OnReceiveChejanData: 체결데이터를 받은 시점을 알려준다.
        입력값
        sGubun . 체결구분
        nItemCnt - 아이템갯수
        sFidList . 데이터리스트

        비고
        sGubun . 0:주문체결통보, 1:잔고통보, 3:특이신호
        sFidList . 데이터 구분은 ‘;’ 이다.
        """
        logger.debug(sGubun, nItemCnt, sFidList)

    def OnEventConnect(self, nErrCode):
        """OnEventConnect: 서버 접속 관련 이벤트
        입력값
        LONG nErrCode : 에러 코드

        비고
        nErrCode가 0이면 로그인 성공, 음수면 실패
        음수인 경우는 에러 코드 참조
        """
        logger.debug(nErrCode)
        self.get_login_info()
        # self.SetInputValue("종목코드", "078890")
        # self.CommRqData("Request1", "opt10001", 0, "0101")

    def OnReceiveRealCondition(self, strCode, strType, strConditionName, strConditionIndex):
        """OnReceiveRealCondition: 조건검색 실시간 편입,이탈 종목을 받을 시점을 알려준다.
        입력값
        LPCTSTR strCode : 종목코드
        LPCTSTR strType : 편입(“I”), 이탈(“D”)
        LPCTSTR strConditionName : 조건명
        LPCTSTR strConditionIndex : 조건명 인덱스

        비고
        strConditionName에 해당하는 종목이 실시간으로 들어옴.
        strType으로 편입된 종목인지 이탈된 종목인지 구분한다.
        """
        logger.debug(strCode, strType, strConditionName, strConditionIndex)

    def OnReceiveTrCondition(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        """OnReceiveTrCondition: 조건검색 조회응답으로 종목리스트를 구분자(“;”)로 붙어서 받는 시점.
        입력값
        LPCTSTR sScrNo : 종목코드
        LPCTSTR strCodeList : 종목리스트(“;”로 구분)
        LPCTSTR strConditionName : 조건명
        int nIndex : 조건명 인덱스
        int nNext : 연속조회(2:연속조회, 0:연속조회없음)
        """
        logger.debug(sScrNo, strCodeList, strConditionName, nIndex, nNext)

    def OnReceiveConditionVer(self, lRet, sMsg):
        """OnReceiveConditionVer: 로컬에 사용자 조건식 저장 성공 여부를 확인하는 시점
        입력값
        long lRet : 사용자 조건식 저장 성공여부 (1: 성공, 나머지 실패)
        """
        logger.debug(lRet, sMsg)


    def login(self):
        """CommConnect: 로그인 윈도우를 실행
        원형: LONG CommConnect()
        설명: 로그인 윈도우를 실행한다.
        입력값: 없음
        반환값: 0 - 성공, 음수값은 실패
        비고: 로그인이 성공하거나 실패하는 경우 OnEventConnect 이벤트가 발생하고 이벤트의 인자 값으로 로그인 성공 여부를 알 수 있다.
        """
        connect_result = self.kiwoom.CommConnect()
        if connect_result == 0:
            print("로그인 윈도우 실행 성공")
        else:
            print("로그인 윈도우 실행 실패")

    def get_connect_state(self):
        """현재접속상태를 반환"""
        connect_state = self.kiwoom.GetConnectState()
        if connect_state == 0:
            print("미연결")
        elif connect_state == 1:
            print("연결완료")

    def get_login_info(self):
        """로그인 정보를 반환

        - “ACCOUNT_CNT” – 전체 계좌 개수를 반환한다.
        - "ACCNO" – 전체 계좌를 반환한다. 계좌별 구분은 ‘;’이다.
        - “USER_ID” - 사용자 ID를 반환한다.
        - “USER_NAME” – 사용자명을 반환한다.
        - “KEY_BSECGB” – 키보드보안 해지여부. 0:정상, 1:해지
        - “FIREW_SECGB” – 방화벽 설정 여부. 0:미설정, 1:설정, 2:해지
        """
        account_cnt = self.kiwoom.GetLoginInfo("ACCOUNT_CNT")
        accno = self.kiwoom.GetLoginInfo("ACCNO")
        user_id = self.kiwoom.GetLoginInfo("USER_ID")
        user_name = self.kiwoom.GetLoginInfo("USER_NAME")
        key_bsecgb = self.kiwoom.GetLoginInfo("KEY_BSECGB")
        firew_secgb = self.kiwoom.GetLoginInfo("FIREW_SECGB")
        pprint(dict(account_cnt=account_cnt, accno=accno, user_id=user_id, user_name=user_name, key_bsecgb=key_bsecgb, firew_secgb=firew_secgb))

    def CommRqData(self, sRQName, sTrCode, nPrevNext, sScreenNo):
        """CommRqData: 통신 데이터를 송신
        ## 원형
        LONG CommRqData(BSTR sRQName, BSTR sTrCode, long nPrevNext, BSTR sScreenNo)
        ## 설명
        Tran을 서버로 송신한다.
        ## 입력값
        - BSTR sRQName
        - BSTR sTrCode
        - long nPrevNext
        - BSTR sScreenNo
        ## 반환값
        - OP_ERR_SISE_OVERFLOW – 과도한 시세조회로 인한 통신불가
        - OP_ERR_RQ_STRUCT_FAIL – 입력 구조체 생성 실패
        - OP_ERR_RQ_STRING_FAIL – 요청전문 작성 실패
        - OP_ERR_NONE – 정상처리
        ## 비고
        - sRQName – 사용자구분 명
        - sTrCode - Tran명 입력
        - nPrevNext - 0:조회, 2:연속
        - sScreenNo - 4자리의 화면번호
        Ex) openApi.CommRqData( “RQ_1”, “OPT00001”, 0, “0101”);
        """
        result = self.kiwoom.CommRqData(sRQName, sTrCode, nPrevNext, sScreenNo)
        logger.debug(result)

    # def SendOrder(self, sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo):
    #     """SendOrder: 주식주문 Tran을 송신
    #     ## 원형
    #     LONG SendOrder( BSTR sRQName, BSTR sScreenNo, BSTR sAccNo, LONG nOrderType, BSTR sCode, LONG nQty, LONG nPrice, BSTR sHogaGb, BSTR sOrgOrderNo)
    #     ## 설명
    #     주식 주문을 서버로 전송한다.
    #     ## 입력값
    #     - sRQName - 사용자 구분 요청 명
    #     - sScreenNo - 화면번호[4]
    #     - sAccNo - 계좌번호[10]
    #     - nOrderType - 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
    #     - sCode, - 주식종목코드
    #     - nQty – 주문수량
    #     - nPrice – 주문단가
    #     - sHogaGb - 거래구분
    #     - sOrgOrderNo – 원주문번호
    #     ## 반환값
    #     - 에러코드 <4.에러코드표 참고>
    #     ## 비고
    #     sHogaGb – 00:지정가, 03:시장가, 05:조건부지정가, 06:최유리지정가, 07:최우선지정가, 10:지정가IOC, 13:시장가IOC, 16:최유리IOC, 20:지정가FOK, 23:시장가FOK, 26:최유리FOK, 61:장전시간외종가, 62:시간외단일가, 81:장후시간외종가
    #     ※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK, 장전시간외, 장후시간외 주문시 주문가격을 입력하지 않습니다.
    #     ex)
    #     지정가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 48500, “00”, “”);
    #     시장가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 0, “03”, “”);
    #     매수 정정 - openApi.SendOrder(“RQ_1”,“0101”, “5015123410”, 5, “000660”, 10, 49500, “00”, “1”);
    #     매수 취소 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 3, “000660”, 10, 0, “00”, “2”);
    #     """

    def SetInputValue(self, sID, sValue):
        """SetInputValue: Tran 입력 값을 서버통신 전에 입력
        입력값
        sID (str) – 아이템명
        sValue (str) – 입력 값

        비고
        통신 Tran 매뉴얼 참고
        Ex) openApi.SetInputValue(“종목코드”, “000660”);
        openApi.SetInputValue(“계좌번호”, “5015123401”);
        """
        self.kiwoom.SetInputValue(sID, sValue)

    def CommGetData(self, sJongmokCode, sRealType, sFieldName, nIndex, sInnerFieldName):
        """CommGetData: 수신 받은 데이터에서 해당 항목을 반환
        원형
        BSTR CommGetData(LPCTSTR sJongmokCode, LPCTSTR sRealType, LPCTSTR sFieldName, long nIndex, LPCTSTR sInnerFieldName)
        설명
        Tran 데이터, 실시간 데이터, 체결잔고 데이터를 반환한다.
        입력값
        1. Tran 데이터
        sJongmokCode : Tran명
        sRealType : 사용안함
        sFieldName : 레코드명
        nIndex : 반복인덱스
        sInnerFieldName: 아이템명

        2. 실시간 데이터
        sJongmokCode : Key Code
        sRealType : Real Type
        sFieldName : Item Index
        nIndex : 사용안함
        sInnerFieldName:사용안함

        3. 체결 데이터
        sJongmokCode : 체결구분
        sRealType : “-1”
        sFieldName : 사용안함
        nIndex : ItemIndex
        sInnerFieldName:사용안함

        반환값
        요청 데이터

        비고
        Ex)
        TR정보 요청 - openApi.CommGetData(“OPT00001”, “”, “주식기본정보”, 0, “현재가”);
        실시간정보 요청 - openApi.CommGetData(“000660”, “A”, 0);
        체결정보 요청 - openApi.CommGetData(“000660”, “-1”, 1);
        """
        result = self.kiwoom.CommGetData(sJongmokCode, "", sFieldName, 0, sInnerFieldName)
        logger.info("CommGetData: ", dict(result=result))
