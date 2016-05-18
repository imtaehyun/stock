import requests
"""
네이버 증권 정보 파서
종합정보: http://finance.naver.com/item/main.nhn?code=
시세: http://finance.naver.com/item/sise.nhn?code=
차트: http://finance.naver.com/item/fchart.nhn?code=
투자자별 매매동향: http://finance.naver.com/item/frgn.nhn?code=
뉴스/공시: http://finance.naver.com/item/news.nhn?code=
종목분석: http://finance.naver.com/item/coinfo.nhn?code=
종목토론실: http://finance.naver.com/item/board.nhn?code=
"""

def get_news(stock_no):
    url = 'http://finance.naver.com/item/news.nhn?code=' + stock_no
    r = requests.get(url)
    print(r.text)

get_news('078890')