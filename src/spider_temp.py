from app.crawl.spider.ths import TradeCrawl


if __name__ == "__main__":

    trades = TradeCrawl().crawl()

    print(trades)
