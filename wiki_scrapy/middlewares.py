import logging

from scrapy.http import Request
from scrapy.spidermiddlewares import depth

from wiki_scrapy.spiders.wiki_spider import RAND_URL

logger = logging.getLogger(__name__)


class RootPathMiddleware(object):

  rootKey = 'path_root_url'

  def process_spider_output(self, response, result, spider):
    def _filter(request):
      if isinstance(request, Request):
        import pdb; pdb.set_trace()
        if 'root_path_url' not in response.meta:
          request['root_path_url'] = response.url
      return True

    if 'root_path_url' not in response.meta:
      path_root = response.url
      response.meta[self.rootKey] = path_root
      spider.visited_urls_in_path[path_root] = []

    return (r for r in result or () if _filter(r))


"""
class DepthAfterFirstMiddleware(depth.DepthMiddleware):

  def process_spider_output(self, response, result, spider):
    def _filter(request):
      if isinstance(request, Request):
        if response.meta['depth'] == 1:
          request.meta['root_path_url'] = response.url
        depth = response.meta['depth'] + 1
        request.meta['depth'] = depth
        if self.prio:
          request.priority -= depth * self.prio
        if self.maxdepth and depth > self.maxdepth:
          logger.debug(
            "Ignoring link (depth > %(maxdepth)d): %(requrl)s ",
            {'maxdepth': self.maxdepth, 'requrl': request.url},
            extra={'spider': spider})
          return False
        elif self.stats:
          if self.verbose_stats:
              self.stats.inc_value('request_depth_count/%s' % depth,
                                   spider=spider)
          self.stats.max_value('request_depth_max', depth,
                               spider=spider)
      return True

    # base case (depth=0)
    if self.stats and 'depth' not in response.meta and response.url != RAND_URL:
      response.meta['depth'] = 1
      if self.verbose_stats:
        self.stats.inc_value('request_depth_count/0', spider=spider)

    return (r for r in result or () if _filter(r))
"""
