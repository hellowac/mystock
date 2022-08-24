import time
import json
from app.crawl.spider.ths import (
    TradeCrawl,
    TradeStockCrawl,
    StockCompanyInfoCrawl,
    ArticleCrawl,
)


def crawl_ths_category_stock():
    # 爬同花顺各个分类行业股票

    trades = TradeCrawl().crawl()

    print(json.dumps(trades, ensure_ascii=False))

    stock_crawler = TradeStockCrawl()

    for category, trades in trades.items():

        with open(f"{category}.md", "w") as fw:
            fw.write(f"## {category}\n\n")

            for trade in trades:
                fw.write(f"### {trade['name']}\n\n")

                stocks = stock_crawler.crawl(trade["name"], trade["href"])

                for stock in stocks:
                    fw.write(
                        f"- [{stock['name']}](http://stockpage.10jqka.com.cn/{stock['code']}/)\n"
                    )

                fw.write("\n")

                print(f"抓取完同花顺分类: {category} - {trade['name']}")

                time.sleep(0.5)

    # print(json.dumps(stocks, ensure_ascii=False))


def crawl_ths_stock_info():
    # 爬同花顺股票详细

    stocks = [
        {"code": "000020", "name": "深华发A", "href": "/000020/"},
        {"code": "002025", "name": "航天电器", "href": "/002025/"},
        {"code": "002045", "name": "国光电器", "href": "/002045/"},
        {"code": "002055", "name": "得润电子", "href": "/002055/"},
        {"code": "002137", "name": "实益达", "href": "/002137/"},
        {"code": "002139", "name": "拓邦股份", "href": "/002139/"},
        {"code": "002179", "name": "中航光电", "href": "/002179/"},
        {"code": "002188", "name": "新嘉联", "href": "/002188/"},
        {"code": "002241", "name": "歌尔声学", "href": "/002241/"},
        {"code": "002351", "name": "漫步者", "href": "/002351/"},
        {"code": "002369", "name": "卓翼科技", "href": "/002369/"},
        {"code": "002384", "name": "东山精密", "href": "/002384/"},
        {"code": "002402", "name": "和而泰", "href": "/002402/"},
        {"code": "002475", "name": "立讯精密", "href": "/002475/"},
        {"code": "002547", "name": "春兴精工", "href": "/002547/"},
        {"code": "002635", "name": "安洁科技", "href": "/002635/"},
        {"code": "002655", "name": "共达电声", "href": "/002655/"},
        {"code": "002660", "name": "茂硕电源", "href": "/002660/"},
        {"code": "300083", "name": "劲胜股份", "href": "/300083/"},
        {"code": "300115", "name": "长盈精密", "href": "/300115/"},
        {"code": "300131", "name": "英唐智控", "href": "/300131/"},
        {"code": "300207", "name": "欣旺达", "href": "/300207/"},
        {"code": "300227", "name": "光韵达", "href": "/300227/"},
        {"code": "300256", "name": "星星科技", "href": "/300256/"},
        {"code": "300279", "name": "和晶科技", "href": "/300279/"},
        {"code": "300282", "name": "汇冠股份", "href": "/300282/"},
        {"code": "300319", "name": "麦捷科技", "href": "/300319/"},
        {"code": "601231", "name": "环旭电子", "href": "/601231/"},
    ]

    stock_information_crawler = StockCompanyInfoCrawl()

    stock_info = {}

    for stock in stocks:
        stock_code = stock["code"]

        stock_info[stock_code] = stock_information_crawler.crawl(stock_code)

        break  # 只爬第一个公司

    print(json.dumps(stock_info, ensure_ascii=False))


def crawl_xueqiu_article():
    # 爬取雪球文章

    crawler = ArticleCrawl()

    texts = crawler.crawl()

    print("\n".join(texts))


if __name__ == "__main__":

    crawl_ths_category_stock()
