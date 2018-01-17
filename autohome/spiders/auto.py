# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import AutohomeItem

class AutoSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['autohome.com.cn']
    start_urls = ['http://autohome.com.cn/']



    def start_requests(self):
        start_url = 'https://www.autohome.com.cn/news/'
        yield Request(start_url,callback=self.parse_index)

    def parse_index(self,response):
        other_page_numList =  response.xpath('//a[contains(@href,"liststart")]/@href').extract()
        for other_page in other_page_numList:
            other_page_url = response.urljoin(other_page)
            yield Request(other_page_url,dont_filter=False,callback=self.parse_index)

        detail_pageList = response.css("#auto-channel-lazyload-article ul li a::attr(href)").extract()
        for detail_page_url in detail_pageList:
            detail_page_url = response.urljoin(detail_page_url)
            yield Request(detail_page_url,dont_filter=False,callback=self.parse_detail)

    def parse_detail(self,response):

        url = response.url
        title = response.xpath('//*[@id="articlewrap"]/h1/text()').extract_first().strip()
        content = ''.join(response.css('#articleContent p::text').extract()).replace(']','').replace('[','')
        desc = content[:50]

        yield AutohomeItem(url=url,title=title,content=content,desc=desc)
