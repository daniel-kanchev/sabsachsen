import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from sabsachsen.items import Article


class Sabsachsen_2Spider(scrapy.Spider):
    name = 'sabsachsen_2'
    start_urls = ['https://www.sab.sachsen.de/die-sab/pressemitteilungen/index.jsp']

    def parse(self, response):
        links = response.xpath('//a[@class="list-group-item"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="container"]/h3/text()').get()
        if date:
            date = " ".join(date.split()[1:])

        content = response.xpath('//main/div[@class="container"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[1:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()