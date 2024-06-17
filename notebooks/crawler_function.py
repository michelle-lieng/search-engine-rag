import scrapy
from scrapy.crawler import CrawlerProcess

class WebsiteSpider(scrapy.Spider):
    name = 'website_spider'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'trial_scraped_data.json'
    }

    def __init__(self, urls, *args, **kwargs):
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls

    def parse(self, response):
        content = ' '.join([p.get() for p in response.css('p::text')])
        yield {
            'url': response.url,
            'content': content
        }

def run_spider(urls):
    process = CrawlerProcess()
    process.crawl(WebsiteSpider, urls=urls)
    process.start()

"""
# HAS COMMENTS BETWEEN SO CAN SEE HOW THIS SCRAPER WORKS!!!!!!!!!!!!!!!

# Define Scrapy Spider
# WebsiteSpider inherits from scrapy.Spider (base class for Scrapy spiders)
class WebsiteSpider(scrapy.Spider): 
    # name attribute gives spider an identifier so we can use from cl or through script
    name = 'website_spider'
    # custom settings is a dictionary that can override scrapy's default settings
    custom_settings = {
        'FEED_FORMAT': 'json', # species that output should be in json format
        'FEED_URI': 'scraped_data.json' # sets file name where scraped data will be saved
    }

    # initializes the spider instance
    def __init__(self, urls, *args, **kwargs):
        # call superclass constructor - superclass initization
        # allow you to refer to the parent class scrapy.Spider as WebsiteSpider
        # calls the constructor of the parent class (basically initialising the base class and passing any needed variables for that)
        super(WebsiteSpider, self).__init__(*args, **kwargs)
        # tells scrapy where to start crawling from
        self.start_urls = urls

    #Scrapy reads the start_urls attribute.
    #Scrapy generates requests for each URL in start_urls.
    #These requests are scheduled and sent, with the parse method set as the callback.

    # this processes the response from each url
    def parse(self, response):
        content = ' '.join([p.get() for p in response.css('p::text')])
        # response.css('p::text') selects all paragraph elements (<p>).
        # p.get() extracts the text content from each paragraph.
        # content is a string of all paragraph texts joined together.
        yield {
            'url': response.url,
            'content': content
        }
        #yield returns a dictionary containing the URL and the combined content.



# Step 3: Run the Scrapy Spider
def run_spider(urls):
    # CrawlerProcess is used to start the Scrapy process from within a script.
    process = CrawlerProcess()
    process.crawl(WebsiteSpider, urls=urls) # sets up spider with provided url
    process.start() # start crawling process

# Scrape content from URLs using Scrapy
run_spider(urls)

# EXTRA: CHECK VALUE OF START_URLS
#spider = WebsiteSpider(urls=urls)
#spider.start_urls
"""