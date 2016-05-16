# coding=utf-8
import requests

"""한국거래소(http://www.krx.co.kr/) 정보 파싱"""


def generate_otp():
    """주식종목 리스트 뽑기전 OTP Key 생성"""
    r = requests.get('http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=COM%2Ffinder_stkisu&name=form')
    print('otp: {}'.format(r.text))
    return r.text


def get_stock_list():
    """주식종목 리스트 뽑기"""
    key = generate_otp()
    payload = dict(isuCd='', no='P1', mktsel='ALL', searchText='', pagePath='/contents/COM/FinderStkIsu.jsp', code=key)
    r = requests.post('http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx', data=payload)
    print(r.text)


get_stock_list()
