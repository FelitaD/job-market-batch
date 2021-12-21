import math
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader

from jobs_crawler.jobs_crawler.items import JobsCrawlerItem
from itemloaders.processors import MapCompose, Join


class WttjSpider(scrapy.Spider):
    name = 'wttj2'
    start_urls = ['https://www.welcometothejungle.com/fr/jobs?page=1&aroundQuery=&query=data%20engineer&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD%20%2F%20Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Autres&refinementList%5Bcontract_type_names.fr%5D%5B%5D=VIE&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance']

    BASE_URL = 'https://www.welcometothejungle.com'

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],
                             self.parse,
                             meta={"playwright": True, "playwright_include_page": True})

    async def parse(self, response):
        page = response.meta['playwright_page']

        # parse jobs list
        for i in range(1, 31):
            async with page.expect_navigation():
                await page.locator(f'//*[@class="ais-Hits-list-item"][{i}]').click()

            await page.screenshot(path=f"screenshot{i}.png", full_page=True)

            title = await page.inner_text('//*[text()="Le poste"]/parent::h4/following-sibling::h4')
            company = await page.inner_text('//*[text()="La tribu"]/parent::h4/following-sibling::a')

            yield {
                'url': response.url,
                'title': title,
                'company': company
            }

            await page.go_back(wait_until='domcontentloaded')


        # go to next page
        next_locator = page.locator('//*[@aria-label="Next page"]')
        # while next_locator:
        for k in range(3):
            async with page.expect_navigation():
                await page.click('//*[@aria-label="Next page"]')

            for i in range(1, 31):
                async with page.expect_navigation():
                    await page.locator(f'//*[@class="ais-Hits-list-item"][{i}]').click()

                await page.screenshot(path=f"screenshot{i}.png", full_page=True)

                title = await page.inner_text('//*[text()="Le poste"]/parent::h4/following-sibling::h4')
                company = await page.inner_text('//*[text()="La tribu"]/parent::h4/following-sibling::a')

                yield {
                    'url': response.url,
                    'title': title,
                    'company': company
                }

                await page.go_back(wait_until='domcontentloaded')


        await page.close()


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
    process.crawl(WttjSpider)
    process.start()
