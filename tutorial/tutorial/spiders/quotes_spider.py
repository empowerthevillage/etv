from django.http.response import HttpResponse
import scrapy
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.utils.text import slugify
from scrapy.item import Item, Field
from scrapy.selector import Selector
from scrapy.exporters import JsonItemExporter
from itemadapter import ItemAdapter
from dataclasses import dataclass

import json

class VBP(Item):
    name = scrapy.Field()
    address = scrapy.Field()
    category = scrapy.Field()
    phones = scrapy.Field()
    website = scrapy.Field()

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

class SBOSpider(scrapy.Spider):
    name="sbo"

    def start_requests(self):
        urls = [
            'https://www.supportblackowned.com/states/ga?limit=100&limitstart=0&task=searchCompaniesByName&controller=search&categories=&view=search&categoryId=0&searchkeyword=&letter=&categorySearch=&citySearch=&regionSearch=Georgia&areaSearch=&provinceSearch=&countrySearch=226&typeSearch=&zipcode=&geo-latitude=&geo-longitude=&radius=100&featured=&filter-by-fav=&filter_active=&selectedParams=&form_submited=1&moreParams=&orderBy=packageOrder+desc&preserve=',
            'https://www.supportblackowned.com/states/ga?regionSearch=Georgia&resetSearch=1&geolocation=0&radius=100&countrySearch=226&limit=100&task=searchCompaniesByName&controller=search&categoryId=0&form_submited=1&orderBy=packageOrder%20desc&start=100',
            'https://www.supportblackowned.com/states/ga?regionSearch=Georgia&featured=0&resetSearch=1&geolocation=0&radius=100&countrySearch=226&limit=100&task=searchCompaniesByName&controller=search&categoryId=0&form_submited=1&orderBy=packageOrder%20desc&start=200',
            'https://www.supportblackowned.com/states/ga?regionSearch=Georgia&featured=0&resetSearch=1&geolocation=0&radius=100&countrySearch=226&limit=100&task=searchCompaniesByName&controller=search&categoryId=0&form_submited=1&orderBy=packageOrder%20desc&start=300',
            'https://www.supportblackowned.com/states/ga?regionSearch=Georgia&featured=0&resetSearch=1&geolocation=0&radius=100&countrySearch=226&limit=100&task=searchCompaniesByName&controller=search&categoryId=0&form_submited=1&orderBy=packageOrder%20desc&start=400',
            'https://www.supportblackowned.com/states/ga?regionSearch=Georgia&featured=0&resetSearch=1&geolocation=0&radius=100&countrySearch=226&limit=100&task=searchCompaniesByName&controller=search&categoryId=0&form_submited=1&orderBy=packageOrder%20desc&start=500',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("=")[-1]
        filename = f'ga-sbo-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body) 
            names = response.selector.xpath('//span[@itemprop="name"]/text()').getall()
            for x in names:
                url = 'https://www.supportblackowned.com/%s' %(slugify(x))
                yield scrapy.Request(url=url, callback=self.parse_listing, cb_kwargs=dict(name=x))
        
                
    def parse_listing(self, response, name):
        address = response.selector.xpath('//span[@itemprop="address"]/text()').get()
        category = Selector(response=response).xpath('//div[@class="header-subtitle"]/p/a/text()').get()
        phones = Selector(response=response).xpath('//span[@itemprop="phone"]/a/text()').getall()
        website = Selector(response=response).xpath('//a[@itemprop="url"]/@href').get()
        yield {
            'name': name,
            'address': address,
            'category': category,
            'phones': phones,
            'website': website
        }
