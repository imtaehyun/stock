import requests
from urllib.parse import urljoin
from scrapy.selector import Selector
from pprint import pprint

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

def fetch_page(url):
    r = requests.get(url)
    return r.text

def get_news(code, page_limit=3):
    """
    네이버 금융 주식 종목 뉴스 파싱
    기본 1~3페이지까지 파싱
    """
    news = []
    for page in range(1,page_limit+1):
        url = 'http://finance.naver.com/item/news_news.nhn?code=' + code + '&page=' + str(page)
        html = fetch_page(url)
        sel = Selector(text=html)
        news_list_sel = sel.css("table:not(.Nnavi) tr[align=center]")
        for news_sel in news_list_sel:
            date = news_sel.css("td:nth-child(1) span::text").extract()[0]
            title = news_sel.css("td.title a::text").extract()[0]
            link = urljoin(url, news_sel.css("td.title a::attr(href)").extract()[0])
            source = news_sel.css("td:nth-child(3)::text").extract()[0]
            news.append(dict(date=date, title=title, link=link, source=source))
    pprint(news)
    return news

def get_notice(code, page_limit=1):
    """
        네이버 금융 공시정보 파싱
        기본 1 페이지만 파싱
        """
    notices = []
    for page in range(1, page_limit + 1):
        url = 'http://finance.naver.com/item/news_notice.nhn?code=' + code + '&page=' + str(page)
        html = fetch_page(url)
        sel = Selector(text=html)
        notice_list_sel = sel.css("table:not(.Nnavi) tr[align=center]")
        for notice_sel in notice_list_sel:
            date = notice_sel.css("td:nth-child(1) span::text").extract()[0]
            title = notice_sel.css("td.title a::text").extract()[0]
            link = urljoin(url, notice_sel.css("td.title a::attr(href)").extract()[0])
            source = notice_sel.css("td:nth-child(3)::text").extract()[0]
            notices.append(dict(date=date, title=title, link=link, source=source))
    pprint(notices)
    return notices

# get_news('056080', 1)
# get_notice('078890', 1)