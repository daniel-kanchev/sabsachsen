import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from sabsachsen.items import Article


class SabsachsenSpider(scrapy.Spider):
    name = 'sabsachsen'
    start_urls = ['https://www.sab.sachsen.de/meta/sab-news.jsp',
                  'https://www.sab.sachsen.de/meta/esf-news-%C3%BCbersichtsseite.jsp']

    def parse(self, response):
        articles = response.xpath('//div[@class="news"]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article.xpath('./h3/text()').get()
            date = article.xpath('./span/text()').get()

            content = article.xpath('./p//text()').getall()
            content = [text for text in content if text.strip()]
            content = "\n".join(content).strip()

            item.add_value('title', title)
            item.add_value('link', response.url)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()



