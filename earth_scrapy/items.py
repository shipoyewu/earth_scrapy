# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EarthScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Journal(scrapy.Item):
	title_cn = scrapy.Field()
	title_en = scrapy.Field()
	author = scrapy.Field()
	time = scrapy.Field()
	journal_number = scrapy.Field()
	summary_cn = scrapy.Field()
	summary_en = scrapy.Field()
	kw_cn = scrapy.Field()
	kw_en = scrapy.Field()
	detail_url = scrapy.Field()
	download_url = scrapy.Field()
