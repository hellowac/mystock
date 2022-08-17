import random
from typing import Dict, List
from lxml import etree
from collections import defaultdict

from bs4 import BeautifulSoup
from requests import Session, Response
from requests.structures import CaseInsensitiveDict

from ..settings import agents, base_headers, logger


class TradeCrawl(object):
    # 同花顺行业爬取

    def __init__(self) -> None:

        self.haders = base_headers.copy()
        self.haders["User-Agent"] = random.choice(agents)
        self.haders["Host"] = "basic.10jqka.com.cn"

        # 构造session
        self.session: Session = Session()
        self.session.headers = CaseInsensitiveDict(self.haders)

    def crawl(self) -> List:
        url = "http://basic.10jqka.com.cn/48/"
        resp: Response = self.session.get(url, verify=False)

        if resp.status_code != 200:
            logger.info(f"爬取行业信息错误, CODE[{resp.status_code}]: {resp.text}")
            return

        # logger.info(resp.text)

        soup = BeautifulSoup(resp.content.decode("gbk"))

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
