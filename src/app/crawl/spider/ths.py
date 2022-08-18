import random
from typing import Dict, List
from lxml import etree
from collections import defaultdict

from bs4 import BeautifulSoup
from requests import Session, Response
from requests.structures import CaseInsensitiveDict

from ..settings import agents, base_headers, logger


class CrawlBase(object):
    # 同花顺爬虫基础类

    def __init__(self) -> None:

        self.haders = base_headers.copy()
        self.haders["User-Agent"] = random.choice(agents)
        self.haders["Host"] = "basic.10jqka.com.cn"

        # 构造session
        self.session: Session = Session()
        self.session.headers = CaseInsensitiveDict(self.haders)


class TradeCrawl(CrawlBase):
    # 同花顺行业爬取

    def crawl(self) -> List:
        """同花顺行业爬取

        返回数据格式:
            [
                {
                    'code': '420700',
                    'name': '湖北省',
                    'href': '/dq/420700.html'
                }
            ]
        """

        url = "http://basic.10jqka.com.cn/48/"
        resp: Response = self.session.get(url, verify=False)

        if resp.status_code != 200:
            logger.info(f"爬取行业信息错误, CODE[{resp.status_code}]: {resp.text}")
            return

        # logger.info(resp.text)

        soup = BeautifulSoup(resp.content.decode("gbk"), "html.parser")

        trade_category: Dict[str : List[Dict[str, str]]] = defaultdict(list)

        # 按行业分类查询
        for category in soup.find_all("div", class_="category"):

            title = category.find("div", class_="c_title").get_text()
            trade_category[title] = []

            # 各个a标签的text
            for trade in category.find_all("a"):

                trade_code = trade["name"]  # name属性
                trade_name = trade.get_text()

                # 该行业下各个股票, 也就是 http://basic.10jqka.com.cn + href
                trade_href = trade["href"]

                trade_category[title].append(
                    {"code": trade_code, "name": trade_name, "href": trade_href}
                )

        return trade_category


class TradeStockCrawl(CrawlBase):
    # 同花顺行业股票爬取

    def crawl(self, trade: str, href: str) -> List:
        """同花顺行业的股票爬取

        返回数据格式:
            [
                {
                    'code': '420700',
                    'name': '湖北省',
                    'href': '/dq/420700.html'
                }
            ]
        """

        url = f"http://basic.10jqka.com.cn{href}"
        resp: Response = self.session.get(url, verify=False)

        if resp.status_code != 200:
            logger.info(f"爬取行业股票信息错误, CODE[{resp.status_code}]: {resp.text}")
            return

        # logger.info(resp.text)

        soup = BeautifulSoup(resp.content.decode("gbk"), "html.parser")

        stocks: List = []

        elements = (
            soup.find("div", class_="category")
            .find("div", class_="c_content")
            .find_all("a")
        )

        # 按行业分类查询
        for element in elements:

            # 该股票的同花顺F10, 也就是 http://basic.10jqka.com.cn + href
            stock_href = element["href"]  # name属性
            stock_name = element.get_text()
            stock_code = stock_href[1:-1]

            stocks.append({"code": stock_code, "name": stock_name, "href": stock_href})

        return stocks


class StockCompanyInfoCrawl(CrawlBase):
    # 同花顺股票公司资料爬取

    def crawl(self, code: str) -> List:
        """同花顺行业的股票爬取

        返回数据格式:
            [
                {
                    'code': '420700',
                    'name': '湖北省',
                    'href': '/dq/420700.html'
                }
            ]
        """

        url = f"http://basic.10jqka.com.cn/{code}/company.html"
        resp: Response = self.session.get(url, verify=False)

        if resp.status_code != 200:
            logger.info(f"爬取行业股票信息错误, CODE[{resp.status_code}]: {resp.text}")
            return

        # logger.info(resp.text)

        soup = BeautifulSoup(resp.content.decode("gbk"), "html.parser")

        attrs: Dict = {}

        # 解析详细情况

        detail_element = soup.find("div", id="detail").find(class_="bd")

        for td in detail_element.find_all("td"):

            has_title = td.find("strong", class_="hltip")

            if not has_title:
                continue

            attr_name = has_title.get_text()
            attr_value = (td.find("span") or td.find("p")).get_text()
            attr_value = attr_value.replace("\t", "").replace("\n", "")

            attrs[attr_name] = attr_value

        return attrs
