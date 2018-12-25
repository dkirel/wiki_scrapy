# wiki_scrapy

wiki_scrapy is a web crawler that models the behavior wikipedia article links leading to wikipedia's philosophy page. This project models the following:

  - The percentage of pages that lead to philosophy
  - The distribution of path lengths for links that eventually make it to Philosophy

### Methodology

The webscraper starts from a random Wikipedia article (example: http://en.wikipedia.org/wiki/Art) and clicks on the first non-italicized link not surrounded by parentheses or brackets in the main text. It then redirects to that link and continue until it reaches Philosophy or until it fails to do so. Failure in this case is defined as the following:
* Reaching a page with an error status code i.e. 404
* Encounterning a loop
* Reaching a web page that has no links in the main text area
* Being redirected to a web page outside of wikipedia.org

The webscraper minimizes the number of requests by prioritizing requests with a higher depth (those that have gone through multiple redirects) and by keeping track of sucessful and unsuccessful paths.

Below are some statistics summarizing the findings of this project:
* Sample starting random articles used: 500
* Average successful path length: 14.6
* The successful path length distribution is comparable to a normal distribution with a slight positive skew and lower levels of kurtosis as it seems to be less tail-heavy

### Libraries

This project uses a number of libraries. The main ones are:

* [Scrapy](https://scrapy.org/) - a framework for extracting data from websites
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - library for pulling data out of HTML and XML files
* [Matplotlib](https://matplotlib.org/) - A plotting library
* [Pandas](http://pandas.pydata.org/) - an open source library providing data analysis tools

#### Running the project
For web-scraping and data analysis:
```sh
$ python run.py
```
For web-scraping without any analysis:
```sh
$ python run.py -na
```
For running analysis on stored data:
```sh
$ python run.py -ao
```

### Todos

 - Write unit tests
 - Find ways to improve performance and lower # of requests made

