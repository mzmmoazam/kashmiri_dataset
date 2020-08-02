import scrapy
from string import ascii_lowercase
from scrapy.loader import ItemLoader
from kashmiri_dataset.items import SHItem


class SH_Spider(scrapy.Spider):
    name = 'sh_dict_spyder'

    alpha_index = 0
    
    domain_name = "uchicago_S_Hassan"

    
    page_url = lambda self, index: \
        f"https://dsalsrv04.uchicago.edu/cgi-bin/app/hassan_query.py?qs={ascii_lowercase[index]}&searchhws=yes"
        
    start_urls = [
        page_url('',alpha_index)
    ]

    def parse(self, response):
        for div in response.xpath('//div[@id="results_display"]/div'):
            fullText = div.xpath('.//text()')
            text = fullText[-1].extract()
            splitIndex = text.index(' ')

            item = ItemLoader(item=SHItem(),selector=div)

            item.add_value('word',fullText[0].extract())
            item.add_value('category',text[:splitIndex])
            item.add_value('meaning',text[splitIndex:])
            item.add_xpath('file_urls','.//audio/source/@src')
            item.add_value('domain_name',self.domain_name)
            item.add_value('file_name',fullText[0].extract())

            yield item.load_item()

        self.alpha_index += 1
        if self.alpha_index < len(ascii_lowercase):
            yield scrapy.Request(self.page_url(self.alpha_index),
                                 self.parse)