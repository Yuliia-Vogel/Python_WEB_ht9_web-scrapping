import scrapy


class QuotesFileCreationSpider(scrapy.Spider):
    name = "quotes_file_creation"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "qoutes.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            # yield scrapy.Request(url=self.start_urls[0] + next_link) # конспект в LMS
            yield scrapy.Request(url=response.urljoin(next_link), callback=self.parse)
 
