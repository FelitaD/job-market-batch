import math
import re
from scrapy_selenium import SeleniumRequest
import selenium.webdriver.support.ui as UI
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader

from jobs_crawler.jobs_crawler.items import JobsCrawlerItem
from itemloaders.processors import MapCompose, Join


class WttjSpider(scrapy.Spider):
    name = 'wttj3'
    start_urls = ['https://www.welcometothejungle.com/fr/jobs?page={page_number}&aroundQuery=&query=data%20engineer&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDI&refinementList%5Bcontract_type_names.fr%5D%5B%5D=CDD%20%2F%20Temporaire&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Autres&refinementList%5Bcontract_type_names.fr%5D%5B%5D=VIE&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Freelance']

    BASE_URL = 'https://www.welcometothejungle.com'

    def start_requests(self):
        yield SeleniumRequest(url=self.start_urls[0].format(page_number=1), callback=self.parse)

    def parse(self, response):
        driver = response.meta['driver']
        wait = UI.WebDriverWait(driver, 10)

        cookie_ok_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "OK pour moi")]')))
        cookie_ok_element.click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        job_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="ais-Hits-list-item"]/article/div[1]/a')))
        print(job_elements)
        for job_element in job_elements:
            job_link = job_element.get_attribute('href')
            print(job_link)


    def yield_job_item(self, response, url, title, company, remote, location, type, industry, texts):
        l = ItemLoader(item=JobsCrawlerItem(), response=response)
        l.add_value('url', url)
        l.add_value('title', title)
        l.add_value('company', company)
        l.add_value('remote', remote)
        l.add_value('location', location)
        l.add_value('type', type)
        l.add_value('industry', industry)
        l.add_value('text', texts)
        yield l.load_item()


if __name__ == '__main__':
    process = CrawlerProcess(
        settings={
            'SELENIUM_DRIVER_NAME': 'chrome',
            'SELENIUM_DRIVER_EXECUTABLE_PATH': '/Users/donor/PycharmProjects/de_job_market/jobs_crawler/chromedriver',
            'SELENIUM_DRIVER_ARGUMENTS': ['--headless'],
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy_selenium.SeleniumMiddleware': 800
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
