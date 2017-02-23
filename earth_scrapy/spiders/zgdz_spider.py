# -*- coding: utf-8 -*-

#!/usr/bin/env python2

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request  
from scrapy import log
from scrapy.selector import Selector
from lxml import etree
from earth_scrapy.items import Journal
from earth_scrapy.spiders.db.es import EsDao

class ZGDZSpider(CrawlSpider):
	name = 'zgdz.cn'
	allowed_domains = ['zgdz.eq-j.cn']
	start_urls = [
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2016&quarter_id=1',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2016&quarter_id=2',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2015&quarter_id=1',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2015&quarter_id=2',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2015&quarter_id=3',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2015&quarter_id=4',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2014&quarter_id=1',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2016&quarter_id=2',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2014&quarter_id=3',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2014&quarter_id=4',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2013&quarter_id=1',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2013&quarter_id=2',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2013&quarter_id=3',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2013&quarter_id=4',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2012&quarter_id=1',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2012&quarter_id=2',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2012&quarter_id=3',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2012&quarter_id=4',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2011&quarter_id=1',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2011&quarter_id=2',
#		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2011&quarter_id=3',
		'http://zgdz.eq-j.cn/zgdz/ch/reader/issue_list.aspx?year_id=2011&quarter_id=4'
	]

	rules = []
	base_url = 'http://zgdz.eq-j.cn/zgdz/ch/reader/'

	def parse(self, response):
		resp = Selector(text=response.body)
		els = resp.xpath('//div[@class="center-xk"]/ul')
		self.log('Hi, this is an item page! %s, this page contains %d articles.' %(response.url, len(els)))
		for el in els:
			item = self.load_item(el)
			yield Request(self.base_url + item['detail_url'], meta={'item':item}, callback=self.detail_item)

	def load_item(self, response):
		self.log('load item.....')
		item = Journal()
		item['title_cn'] = response.xpath('li[@class="title"]/a/@title').extract()[0]
		item['author'] = response.xpath('li[@class="author"]/text()').extract()[0]
		item['journal_number'] = response.xpath('li[@class="other"]/text()').extract()[0]
		item['detail_url'] = response.xpath('li[@class="title"]/a/@href').extract()[0]
		item['download_url'] = self.base_url + response.xpath('li[@class="other"]/a/@href').extract()[1]
		#print item
		return item

	def detail_item(self, response):
		self.log('detail item ......')
		resp = Selector(text=response.body)
		item = response.meta['item']
		summary = resp.xpath('//td[@class="unnamed3"]/span/text()')
		item['summary_cn'] = summary.extract()[0]
		item['summary_en'] = summary.extract()[1]
		item['time'] = resp.xpath('//span[@id="SendTime"]/text()').extract()[0]
		item['kw_cn'] = resp.xpath('//span[@id="KeyWord"]/a/font/u/text()').extract()
		item['kw_en'] = resp.xpath('//span[@id="EnKeyWord"]/a/font/u/text()').extract()
#		print item
		#self.conn.save('scrapy_test', 'scrapy_type', item)
		return item

