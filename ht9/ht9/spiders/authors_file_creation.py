import scrapy


class AuthorsFileCreationSpider(scrapy.Spider):
    name = "authors_file_creation"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json"}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    list_of_authors = []

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            author = quote.xpath("span/small/text()").get()
            if author not in self.list_of_authors:
                self.list_of_authors.append(author)
                author_link = quote.xpath("span/a/@href").get()
                if author_link:
                # Зробити запит на сторінку автора
                    yield scrapy.Request(
                        url=response.urljoin(author_link),
                        callback=self.parse_author,
                        meta={'author_name': author}
                    )

            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                # yield scrapy.Request(url=self.start_urls[0] + next_link) # конспект в LMS
                yield scrapy.Request(url=response.urljoin(next_link), callback=self.parse) # запропонував GPT

    def parse_author(self, response):
        # Зібрати інформацію про автора
        fullname = response.meta['author_name']
        born_date = response.xpath("//span[@class='author-born-date']/text()").get()
        born_location = response.xpath("//span[@class='author-born-location']/text()").get()
        description = response.xpath("//div[@class='author-description']/text()").get()
        
        yield {
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        }