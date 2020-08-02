import scrapy
from string import ascii_lowercase
from scrapy.loader import ItemLoader
from kashmiri_dataset.items import KZItem


class KZ_Spider(scrapy.Spider):
    '''
    http://kashmirizabaan.com
    
    usage :
        scrapy crawl kashmiri_zabaan_spyder -o csv_files/file_name.csv
    
    '''
    name = 'kashmiri_zabaan_spyder'

    start_urls = {
        "kashmiri_zabaan": "http://kashmirizabaan.com/eng_ver.php"
    }
    
    alpha_first_index = 0
    alpha_sec_index = 0

    # can't use single index query; bug in scrapy
    # https://github.com/scrapy/scrapy/issues/3077
    # as it is fixed revert to single index query
    # alpha_index = 0

    payload = lambda self,indexOne,indexSec: f'meaning_target={ascii_lowercase[indexOne]}{ascii_lowercase[indexSec]}&Submit=Go&lantype=hin&opt_dic=mat_like'
    # payload = lambda self,indexOne: f'meaning_target={ascii_lowercase[indexOne]}&Submit=Go&lantype=hin&opt_dic=mat_like'

    headers = {
        'Connection': "keep-alive",
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept-Language': "en,et;q=0.9,ur;q=0.8",
    }

    def start_requests(self):
        yield scrapy.Request(self.start_urls["kashmiri_zabaan"],
                             self.parse,
                             method="POST",
                             headers=self.headers,
                             body=self.payload(self.alpha_first_index,self.alpha_sec_index))
                             # body=self.payload(self.alpha_index))

    def parse(self, response):
        for table in response.xpath('//table[@width="717"]'):
            if len(table.xpath('.//tr')) == 8:
                item = ItemLoader(item=KZItem(),selector=table)
                item.add_xpath('headword','(.//tr/td)[1]/text()')
                item.add_xpath('category','(.//tr/td)[2]/font/text()')
                item.add_xpath('englishExample','(.//tr/td)[3]/font/text()')
                item.add_xpath('hindiMeaning','(.//tr/td)[4]/font/text()')
                item.add_xpath('hindiExample','(.//tr/td)[5]/font/text()')
                item.add_xpath('englishMeaning','(.//tr/td)[6]/font/text()')
                item.add_xpath('kashmiriExample','(.//tr/td)[7]/font/text()')

                yield item.load_item()



        self.alpha_sec_index += 1
        if self.alpha_sec_index < len(ascii_lowercase):
            yield scrapy.Request(self.start_urls["kashmiri_zabaan"],
                             self.parse,
                             method="POST",
                             headers=self.headers,
                             body=self.payload(self.alpha_first_index,self.alpha_sec_index))
        else:
            self.alpha_first_index += 1
            self.alpha_sec_index = 0
            if self.alpha_first_index < len(ascii_lowercase):
                yield scrapy.Request(self.start_urls["kashmiri_zabaan"],
                                     self.parse,
                                     method="POST",
                                     headers=self.headers,
                                     body=self.payload(self.alpha_first_index, self.alpha_sec_index))
        # self.alpha_index += 1
        # if self.alpha_index < len(ascii_lowercase):
        #     yield scrapy.Request(self.start_urls["kashmiri_zabaan"],
        #                          self.parse,
        #                          method="POST",
        #                          headers=self.headers,
        #                          # body=self.payload(self.alpha_first_index, self.alpha_sec_index))
        #                          body=self.payload(self.alpha_index))

