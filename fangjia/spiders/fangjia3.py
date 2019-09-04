# -*- coding: utf-8 -*-
import scrapy
from fangjia.items import FangjiaItem

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

class fangjiaSpider(scrapy.Spider):
    name = "fangjia"
    allowed_domins = ["http://cd.fang.lianjia.com/"]
    start_urls = []

    def start_requests(self):
        global headers
        urlhead = 'http://cd.fang.lianjia.com/loupan/'
        for i in range(18):
            url = urlhead+'pg%snht1' % i
            self.start_urls.append(url)
        for url in self.start_urls:
            print (url)
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        item = FangjiaItem()
        fang_links = response.xpath('//div[@class="content__list--item xh-highlight"]')
        for i in fang_links:
            title = i.xpath('//p[@class="content__list--item--title twoline"]').extract()[0]
            url = i.xpath('//p[@class="content__list--item--title twoline"/a/@href]').extract()[0] #需要域名
            attribute = i.xpath('//p[@class="content__list--item--des"]').extract()[0]#应该取出所有字段
            attribute2 = i.xpath('//p[@class="content__list--item--time oneline"]').extract()[0]
            attribute += '/'+attribute2
            price = i.xpath('//span[@class="content__list--item-price"]').extract()[0]
            if '独栋' in title:
                yield scrapy.Request(url, headers=headers, callback=self.parse_fangjia)

        if fang_links:
            for fang_link in fang_links:
                url = 'http://cd.fang.lianjia.com'+fang_link
                yield scrapy.Request(url, headers=headers, callback=self.parse_fangjia)

    def parse_fangjia(self, response):   # /是在根节点找(只找根节点下面一层,绝对) //是在根节点下面的所有节点找,相对
        item = FangjiaItem()
        name = response.xpath('//div[@class="name-box"]/a/@title').extract()[0]
        url = response.xpath('//div[@class="name-box"]/a/@href').extract()[0]
        price = response.xpath('//p[@class="jiage"]/span[@class="junjia"]/text()').extract()[0]
        address = response.xpath('//p[@class="where"]/span/@title').extract()[0]
        item['FANGJIA_NAME'] = name
        item['FANGJIA_ADDRESS'] = address
        item['FANGJIA_PRICE'] = price
        item['FANGJIA_URL'] = 'http://cd.fang.lianjia.com'+url
        print (item['FANGJIA_NAME'])
        print (item['FANGJIA_ADDRESS'])
        print (item['FANGJIA_PRICE'])
        print (item['FANGJIA_URL'])
        yield item

