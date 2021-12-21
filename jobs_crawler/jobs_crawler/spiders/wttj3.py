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

        job_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="ais-Hits-list-item"]')))
        print(len(job_links))
        for i in range(len(job_links)):
            jobs_elements = driver.find_elements_by_xpath('//*[@class="ais-Hits-list-item"]')
            print(len(jobs_elements))
            jobs_elements[i].click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-testid="job_sticky_left-button-apply"]')))

            title_element = driver.find_element_by_xpath('//*[text()="Le poste"]/parent::h4/following-sibling::h4')
            company_element = driver.find_element_by_xpath('//*[text()="La tribu"]/parent::h4/following-sibling::a')
            try:
                remote_element = driver.find_element_by_xpath('//*[@name="remote"]/parent::span/following-sibling::span')
            except NoSuchElementException:
                continue
            try:
                location_element = driver.find_element_by_xpath('//*[@name="location"]/parent::span/following-sibling::span')
            except NoSuchElementException:
                continue
            type_element = driver.find_element_by_xpath('//*[@name="contract"]/parent::span/following-sibling::span/span')
            industry_element = driver.find_element_by_xpath('//*[@name="tag"]/parent::span/following-sibling::span')
            text_elements = driver.find_elements_by_xpath('//h2/following-sibling::div')

            url = driver.current_url
            title = title_element.get_attribute('innerText')
            company = company_element.get_attribute('innerText')
            remote = remote_element.get_attribute('innerText')
            location = location_element.get_attribute('innerText')
            type = type_element.get_attribute('innerText')
            industry = industry_element.get_attribute('innerText')

            texts = ''
            for text_element in text_elements:
                text = text_element.get_attribute('innerText')
                texts = texts + '\n' + text

            yield from self.yield_job_item(response, url, title, company, remote, location, type, industry, texts)

            driver.get_screenshot_as_file(f'job_{i}.png')
            driver.execute_script("window.history.go(-1)")

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
