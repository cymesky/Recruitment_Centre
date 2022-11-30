from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI('http://localhost:6800')


def update_scrapy():
    task = scrapyd.schedule('default', 'eve_crawler')
    print(f'Database updating: log scrapy_app/logs/default/eve_crawler/{task}.log')
