import re
import requests
from scrapy import Request
from scrapy.spiders import Spider
from ..items import QiushibaikespiderItem


class qiushi_spider(Spider):
    name = 'qiushi_spider'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    proxypool_url = 'http://127.0.0.1:5555/random'

    def start_requests(self):
        first_url = 'https://www.qiushibaike.com/text/'
        temp_proxy = 'http://' + self.get_random_proxy()
        print(temp_proxy)
        yield Request(first_url, meta={'proxy': temp_proxy}, headers=self.headers)

    def parse(self, response):
        next_url_head = 'https://www.qiushibaike.com'
        contents = response.xpath('//div[contains(@class,"article block untagged mb15")]/a[@class="contentHerf"]/@href')
        temp_proxy = 'http://' + self.get_random_proxy()
        for content in contents:
            content_href = next_url_head + content.extract()
            yield Request(content_href, headers=self.headers, meta={'proxy': temp_proxy}, callback=self.parse_content)

        for i in range(13):
            next_url = 'https://www.qiushibaike.com/text/page/' + str(i+1) + '/'
            temp_proxy = 'http://' + self.get_random_proxy()
            yield Request(next_url, headers=self.headers, meta={'proxy': temp_proxy})
        # next_url = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').extract()
        # print(next_url)
        # print(''.join(next_url))
        # next_url = next_url_head + ''.join(next_url)

    def parse_content(self, response):
        item = QiushibaikespiderItem()
        item['author'] = response.xpath('//a[@class="side-left-userinfo"]/img/@alt').extract()
        item['stat_time'] = response.xpath('//div[@class="stats"]/span[@class="stats-time"]/text()').extract()
        item['thumbs_up'] = response.xpath('//div[@class="stats"]/span[@class="stats-vote"]/i/text()').extract()
        item['content'] = response.xpath(
            '//div[@class="article block untagged noline"]/div[@class="word"]/div[@class="content"]/text()').extract()
        yield item

    def get_random_proxy(self):
        return requests.get(self.proxypool_url).text.strip()
