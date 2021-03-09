import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import AikbankarsItem
from itemloaders.processors import TakeFirst


class AikbankarsSpider(scrapy.Spider):
	name = 'aikbankars'
	start_urls = ['https://www.aikbanka.rs/media-centar/vesti']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more radius"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="pagination-wrapper"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="article-content radius clearfix"]/p//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="news-date-wrapper"]//text()').get()

		item = ItemLoader(item=AikbankarsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
