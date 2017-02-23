# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from elasticsearch import Elasticsearch
import urllib2
from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

class EarthScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class EsPipeline(object):
	def __init__(self, es_uri, es_index, es_type):
		self.es = Elasticsearch(es_uri)
		self.es_index = es_index
		self.es_type = es_type

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			es_uri=crawler.settings.get('ES_URI'),
			es_index=crawler.settings.get('ES_INDEX'),
			es_type=crawler.settings.get('ES_TYPE')
		)
				
	def process_item(self, item, spider):
		obj = json.dumps(dict(item))
		self.es.index(index=self.es_index, doc_type=self.es_type, body=obj)
		return item


class MyFilesPipeline(FilesPipeline):

	def get_media_requests(self, item, info):
		print ('download_url====================%s' %(item['download_url']))
		for file_url in item['download_url']:
			yield Request(file_url, [])

	def process_item(self, item, spider):
		return item


class DownloadFiles(object):
	def __init__(self, save_dir):
		self.save_dir = save_dir 

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			save_dir = crawler.settings.get('FILES_STORE')
		)

	def process_item(self, item, spider):
		data = urllib2.urlopen(item['download_url'])
		print ("save file path is %s" %(self.save_dir + item['title_cn'] + '.pdf'))
		with open(self.save_dir + '/' + item['title_cn'] + '.pdf','wb') as f:
			f.write(data.read())
		return item
