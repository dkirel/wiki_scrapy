# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exporters import JsonItemExporter


class WikiScrapyPipeline(object):

  def __init__(self):
    self.file = open('items.json', 'wb')
    self.exporter = JsonItemExporter(self.file)

  @classmethod
  def from_crawler(cls, crawler):
    pl = cls()
    crawler.signals.connect(pl.spider_opened, signal=signals.spider_opened)
    crawler.signals.connect(pl.spider_closed, signal=signals.spider_closed)
    return pl

  def spider_opened(self, spider):
    self.exporter.start_exporting()
    spider.logger.info('Spider opened: %s', spider.name)

  def process_item(self, item, spider):
    self.exporter.export_item(item)

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    self.file.close()
    spider.logger.info('Spider closed: %s', spider.name)
