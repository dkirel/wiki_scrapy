# -*- coding: utf-8 -*-

# Scrapy settings for wiki_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wiki_scrapy'

SPIDER_MODULES = ['wiki_scrapy.spiders']
NEWSPIDER_MODULE = 'wiki_scrapy.spiders'

LOG_LEVEL = 'INFO'
DEPTH_PRIORITY = -1
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

ITEM_PIPELINES = {
   'wiki_scrapy.pipelines.WikiScrapyPipeline': 300,
}
