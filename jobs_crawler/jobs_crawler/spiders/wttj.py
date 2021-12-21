import math
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader

from jobs_crawler.jobs_crawler.items import JobsCrawlerItem
from itemloaders.processors import MapCompose, Join


class WttjLinksSpider(scrapy.Spider):
    name = 'wttj_links'
    start_urls = ['https://www.welcometothejungle.com/fr/jobs?page={page_number}&aroundQuery=&query=data%20engineer&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD%20%2F%20Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Autres&refinementList%5Bcontract_type_names.fr%5D%5B%5D=VIE&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance']

    BASE_URL = 'https://www.welcometothejungle.com'

    def __init__(self):
        self.links = set()

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0].format(page_number=1),
                             self.parse_jobs_list,
                             meta={"playwright": True, "playwright_include_page": True})

    async def parse_jobs_list(self, response):
        """ Parse javascript rendered results page and obtain individual job page links. """
        page = response.meta['playwright_page']

        job_elements = await page.query_selector_all('//*[@class="ais-Hits-list-item"]//a')
        for job_element in job_elements:
            job_link = await job_element.get_attribute('href')
            job_url = self.BASE_URL + job_link
            self.links.add(job_url)

        while True:
            try:
                next_locator = page.locator('//*[@aria-label="Next page"]')
                async with page.expect_navigation():
                    await next_locator.click()

                job_elements = await page.query_selector_all('//*[@class="ais-Hits-list-item"]//a')
                for job_element in job_elements:
                    job_link = await job_element.get_attribute('href')
                    job_url = self.BASE_URL + job_link
                    self.links.add(job_url)
                print(len(self.links))
            except TimeoutError:
                print("Cannot find a next button on ", page.url)
                break
            finally:
                with open('wttj_links.txt', 'w') as f:
                    f.write(str(self.links))

        await page.close()

    def parse_job(self, response):
        l = ItemLoader(item=JobsCrawlerItem(), response=response)
        l.add_value('url', response.url)
        l.add_value('title', response.xpath('//*[text()="Le poste"]/parent::h4/following-sibling::h4/text()').get())
        l.add_value('company', response.xpath('//*[text()="La tribu"]/parent::h4/following-sibling::a//text()').get())
        l.add_value('remote', response.xpath('//*[@name="remote"]/parent::span/following-sibling::span//text()').get())
        l.add_value('location',
                    response.xpath('//*[@name="location"]/parent::span/following-sibling::span/text()').get())
        l.add_value('type',
                    response.xpath('//*[@name="contract"]/parent::span/following-sibling::span/span/text()').get())
        l.add_value('industry', response.xpath('//*[@name="tag"]/parent::span/following-sibling::span/text()').get())
        l.add_value('text',
                    response.xpath('//h2/following-sibling::div//text()').getall(),
                    Join('\n'))
        yield l.load_item()


if __name__ == '__main__':
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "CONCURRENT_REQUESTS": 32,
            'ROBOTSTXT_OBEY': False,
            'ITEM_PIPELINES': {'jobs_crawler.jobs_crawler.pipelines.JobsCrawlerPipeline': 300,},
            'AUTOTHROTTLE_ENABLED': True,
            'AUTOTHROTTLE_TARGET_CONCURRENCY': 1,
            'AUTOTHROTTLE_START_DELAY': 5,
            'AUTOTHROTTLE_MAX_DELAY': 60
        }
    )
    process.crawl(WttjLinksSpider)
    process.start()
