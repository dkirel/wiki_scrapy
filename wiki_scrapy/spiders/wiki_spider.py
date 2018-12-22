import scrapy
from bs4 import BeautifulSoup
from urlparse import urlparse

from utils import remove_parentheses
from wiki_scrapy.items import RootUrlResult

WIKI_URL = 'https://en.wikipedia.org'
RANDOM_ARTICLE_PATH = '/wiki/Special:Random'
PHILOSOPHY_PATH = '/wiki/Philosophy'
PHILOSOPHY_URL = WIKI_URL + PHILOSOPHY_PATH
RAND_URL = WIKI_URL + RANDOM_ARTICLE_PATH


class WikiSpider(scrapy.Spider):

  name = 'WikiSpider'

  # {path, steps to phiosophy}
  succesful_paths = {PHILOSOPHY_PATH: 0}
  handle_httpstatus_list = [400, 404, 500]

  failed_paths = {}
  visited_paths = {}

  def __init__(self, sample_size=500, *args, **kwargs):
    self.start_urls = [WIKI_URL + RANDOM_ARTICLE_PATH] * sample_size

  def parse(self, response):
    root_path_url = response.meta.get('root_path_url')
    if not root_path_url:
      root_path_url = response.url
      self.visited_paths[root_path_url] = {}

    visited_paths = self.visited_paths[root_path_url]
    depth = response.meta['depth']
    xpath = "//div[@class = 'mw-parser-output']/p | " \
            "//div[@class = 'mw-parser-output']/ul/li"
    next_path = None

    # Handle error status codes and off-site requests
    if (response.status in self.handle_httpstatus_list or
        not urlparse(response.url).hostname.endswith('wikipedia.org')):
      self.failed_paths.update(visited_paths)
      yield RootUrlResult(url=root_path_url, depth=None, success=False)
      return

    html_components = response.xpath(xpath)
    for component in html_components:
      # Remove parentheses & brackets
      clean_text = remove_parentheses(component.extract())

      soup = BeautifulSoup(clean_text, 'html.parser')
      # Remove italics
      [s.extract() for s in soup('i')]
      # Remove small text that isn't part of the main text
      [s.extract() for s in soup.find_all(attrs={"style": "font-size: small;"})]

      links = [a for a in soup.find_all('a') if not self.is_bracket_a_tag(a)]
      if links:
        # Remove trailing # content
        next_path = links[0]['href'].split('#')[0]
        break

    if (not next_path or next_path.startswith('http') or
        next_path in visited_paths):
      # Update failed_paths if loop or dead end is encountered
      self.failed_paths.update(visited_paths)
      yield RootUrlResult(url=root_path_url, depth=None, success=False)
    elif next_path in self.succesful_paths:
      # Update visited_path lengths to reflect length to philosophy
      depth = depth + self.succesful_paths[next_path] + 1
      for key in visited_paths:
        visited_paths[key] = depth - visited_paths[key]
      self.succesful_paths.update(visited_paths)

      yield RootUrlResult(url=root_path_url, depth=depth, success=True)
    else:
      # Update visited paths and go to next link
      visited_paths[next_path] = depth + 1
      yield scrapy.Request(
        WIKI_URL + str(next_path),
        meta={'root_path_url': root_path_url},
        callback=self.parse)

  def is_bracket_a_tag(self, a):
    return a.text and a.text[0] == '[' and a.text[-1] == ']'
