import argparse
import pandas as pd
import matplotlib.pyplot as plt

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from wiki_scrapy.spiders.wiki_spider import WikiSpider

plt.style.use('ggplot')

msg = 'A web crawler that estimates the percentage of wiki pages that' \
      'eventually lead to philisophy'
parser = argparse.ArgumentParser(
  description='A web crawler that  that ')
parser.add_argument('-ao', '--analysis_only', action='store_true',
                    help='Run the anlayisis with the stored data')
parser.add_argument('-na', '--no_analysis', action='store_true',
                    help='Scrape the data, but do not run analysis on it')
args = parser.parse_args()


if not args.analysis_only:
  process = CrawlerProcess(get_project_settings())
  process.crawl(WikiSpider)
  process.start()

if not args.no_analysis:
  df = pd.read_json('items.json')
  success_q = df['success']
  success_count = success_q.sum()
  count = df['url'].count()

  print('Total sample pages: %d' % (count))
  print('Philosopy reached rate: %.1f%%' %
        ((1.0 * success_count / count) * 100))
  print('Average path length: %.1f' % (df[success_q]['depth'].mean()))
  print('A histogram of successful path lengths will be generated shortly.')

  df[success_q]['depth'].plot(kind='hist')
  plt.show()
