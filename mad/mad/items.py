# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MadItem(scrapy.Item):
    category = scrapy.Field()
    subcategory = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    year = scrapy.Field()
    funding = scrapy.Field()
    website = scrapy.Field()
    summary = scrapy.Field()
