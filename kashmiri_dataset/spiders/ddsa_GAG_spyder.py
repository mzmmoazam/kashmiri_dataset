import scrapy
from scrapy.loader import ItemLoader
from kashmiri_dataset.items import GAGItem


class GAG_Spider(scrapy.Spider):
    '''
    George A. Grierson
    Digital Dictionaries of South Asia
    
    usage :
        scrapy crawl gag_dict_spyder -o csv_files/file_name.csv
    
    '''


    name = 'gag_dict_spyder'

    page = 1
    page_url = lambda self,page : f"https://dsalsrv04.uchicago.edu/cgi-bin/app/grierson_query.py?page={page}"
    start_urls = [
        page_url('',page)
    ]

    def parse(self, response):
        for div in response.xpath('//div[@id="results_display"]/div/div'):
            item = ItemLoader(item=GAGItem(),selector=div)

            item.add_xpath('word','.//p1/b[1]')
            item.add_xpath('hindiPron','.//p1/d[1]')
            item.add_xpath('meaning','.//p1')

            yield item.load_item()

        if self.page <= 1247:
            self.page += 1
            yield scrapy.Request(url=self.page_url(self.page),
                                 callback=self.parse
                                 )

