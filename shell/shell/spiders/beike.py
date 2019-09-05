# -*- coding: utf-8 -*-
import scrapy
from shell.items import ShellItem
import requests
#from urllib.parse import urljoin

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

class shellSpider(scrapy.Spider):
    name = "beike"
    allowed_domins = ["https://bj.zu.ke.com/"]
    start_urls = []

    def start_requests(self):
        for i in range(1,101):
            url = 'https://bj.zu.ke.com/zufang/pg{0}/#contentList'.format(i)
            self.start_urls.append(url)
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        item = ShellItem()
        fang_links = response.xpath('//div[@class="content__list--item--main"]')
        if fang_links:
            for fang_link in fang_links:
                #房源链接
                link_url = response.urljoin(fang_link.xpath('p[@class="content__list--item--title twoline"]//a/@href').extract_first())
                #名称
                name = fang_link.xpath('p[@class="content__list--item--title twoline"]//a/text()').extract_first().replace('\n','').replace(' ','')
                #属性
                attribute = fang_link.xpath('p[@class="content__list--item--des"]//text()').extract()
                attribute=''.join(attribute).replace('\n','').replace(' ','')
                #价格
                price = fang_link.xpath('span[@class="content__list--item-price"]//text()').extract()
                price=''.join(price).replace('\n','').replace(' ','')
                #地址
                if '独栋' in name:
                    selector =scrapy.Selector(text=requests.get(link_url,headers=headers).text)
                    address=selector.xpath('//p[@class="flat__info--title online"]//text()').extract_first().replace('\n','').replace(' ','')
                else:
                    address=attribute[:attribute.index('/')]

                item['address'] = address
                item['name'] = name
                item['url'] = link_url
                item['price'] = price
                item['attribute'] = attribute

                print(item['address'])
                print(item['name'])
                print(item['url'])
                print(item['price'])
                print(item['attribute'])
                yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute('scrapy crawl beike -o beijing.csv '.split())
    #cmdline.execute('scrapy crawl beike'.split())

