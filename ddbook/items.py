# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DdbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    isbn = scrapy.Field()
    book_name = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    good_rate = scrapy.Field()
    pub_time = scrapy.Field()
    book_size = scrapy.Field()
    press = scrapy.Field()
    # picSrc = scrapy.Field()
