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
        name_list = response.xpath('//*[@id="user-repositories-list"]/ul//div[1]/h3/a/text()').re(r'\s*(.+)')
        time_list = response.xpath('//*[@id="user-repositories-list"]/ul/li/div[3]/relative-time/@datetime').extract()
        for name,time in zip(name_list,time_list):
            item = ShiyanlouItem({
                'name':name,
                'update_time':time
                })
            yield item

