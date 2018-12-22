# -*- coding: utf-8 -*-

import scrapy


class RootUrlResult(scrapy.Item):
  url = scrapy.Field()
  depth = scrapy.Field()
  success = scrapy.Field()
