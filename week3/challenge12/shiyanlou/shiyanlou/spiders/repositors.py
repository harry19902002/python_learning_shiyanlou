# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlouItem


class RepositorsSpider(scrapy.Spider):
    name = 'repositors'
    allowed_domains = ['github.com']

    @property
    def start_urls(self):
        urls_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (urls_tmpl.format(i) for i in range(1,4))

    def parse(self, response):
        for repo in response.css('li.col-12'):
            item = ShiyanlouItem()
            item['name'] = repo.xpath('.//div[@class="d-inline-block mb-1"]/h3/a/text()').re_first(r'\s*(.+)')
            item['update_time'] = repo.xpath('.//div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first()
            repo_url = response.urljoin(repo.xpath('.//div[@class="d-inline-block mb-1"]/h3/a/@href').extract_first())
            request = scrapy.Request(repo_url, callback = self.parse_repo)
            request.meta['item'] = item
            yield request

    def parse_repo(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath('//ul[@class="numbers-summary"]/li[1]/a/span/text()').re_first('[^\d]*(\d*)[^\d]*')
        item['branches'] = response.xpath('//ul[@class="numbers-summary"]/li[1]/a/span/text()').re_first('[^\d]*(\d*)[^\d]*')
        item['releases'] = response.xpath('//ul[@class="numbers-summary"]/li[1]/a/span/text()').re_first('[^\d]*(\d*)[^\d]*')
        yield item

