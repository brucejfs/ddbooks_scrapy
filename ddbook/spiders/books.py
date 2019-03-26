# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import DdbookItem
import json


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.54.00.00.00.00.html']

    def parse(self, response):

        # 提取书籍列表页面中每本书的链接
        pattern = 'http://product\.dangdang\.com/.+\d+\.html$'
        le = LinkExtractor(restrict_xpaths='//a[@name="itemlist-picture"]', allow=pattern)
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_book)

        # 提取"下一页"链接
        le = LinkExtractor(restrict_xpaths='//div[@class="paging"]//li[@class="next"]/a[@title="下一页"]')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse)

        # 书籍页面的解析函数
    def parse_book(self, response):
        book = DdbookItem()

        # 页面上部信息
        top_info = response.xpath('//div[@id="product_info"]')
        book['book_name'] = top_info.xpath('.//h1/@title').extract_first()  # 书名
        book_author = top_info.xpath('//span[@id="author"]/a/text()').extract()
        join_sign = ', '
        book['author'] = join_sign.join(book_author)  # 作者
        book['price'] = top_info.xpath('//p[@id="dd-price"]/text()').extract()[-1].rstrip()  # 价格
        # book['price'] = top_info.xpath('//p[@id="dd-price"]/text()').extract()  # 价格
        book['pub_time'] = top_info.xpath('//span[@class="t1"]/text()').re_first('(\d+年\d+月)')  # 出版时间
        book['press'] = top_info.xpath('.//a[@dd_name="出版社"]/text()').extract_first()  # 出版社

        # 页面底部信息
        bottom_info = response.xpath('//div[@id="product_tab"]//div[@id="detail_describe"]')
        book['isbn'] = bottom_info.xpath('//li/text()').re_first('ISBN：(\d+)')  # ISBN 号
        book['book_size'] = bottom_info.xpath('.//li/text()').re_first('开 本：(\d+开)')  # 开本

        # 获取好评率
        post_url = 'http://product.dangdang.com/index.php?r=comment/list&productId=%s&categoryPath=%s&mainProductId=%s&mediumId=0&pageIndex=1&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish'
        # post_str = LinkExtractor(restrict_xpaths='//div[@id="breadcrumb"]/a[last()]')
        category_path = response.xpath('//div[@id="breadcrumb"]/a[last()]/@href').re_first('cp(\d+.*).html$')
        # category_path = post_str.extract_links(response)[0].url[-22:-5]
        product_id = response.url[28:-5]
        yield scrapy.Request(post_url % (product_id, category_path, product_id), meta={'item': book}, callback=self.parse_all)

        # 提取好评率，获得完整书籍信息
    def parse_all(self, response):
        info = json.loads(response.body.decode('utf8'))
        book = response.meta['item']
        book['good_rate'] = info['data']['list']['summary']['goodRate']
        yield book
