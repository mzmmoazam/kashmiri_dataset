import scrapy
from string import ascii_lowercase
from scrapy.loader import ItemLoader
from kashmiri_dataset.items import KLItem


class KL_Spider(scrapy.Spider):
    '''
    www.kashmirilanguage.com
    
    usage :
    
      1. To fetch Kashmiri Text from the website
        scrapy crawl kashmir_language_spyder -o csv_files/file_name.csv
      
      2. To fetch all the files from the website 
        scrapy crawl kashmir_language_spyder  -a download_files=True
    
      3. To fetch files of a certain extension e.g *.pdf
        scrapy crawl kashmir_language_spyder  -a download_files=True -a file_extension=".pdf"
    
    Note : files can be found in downloaded_content/
    
    '''
    
    name = 'kashmir_language_spyder'


    start_urls = [
        "http://www.kashmirilanguage.com/WORD_Books/"
    ]

    domain_name = "kashmirilanguage"
    
    def parse(self, response):

        for link in response.xpath('//following::tr[4]/td[2]/a'):
            
            href = link.xpath('.//@href').extract_first()
            
            if href[-1] == '/':
                yield scrapy.Request(response.urljoin(href),
                                     self.parse)

            elif getattr(self,'download_files','False') != 'True':
                
                if '.htm' in href:
                    yield scrapy.Request(response.urljoin(href),
                                            self._scrapText)

            elif getattr(self,'file_extension','') in href:
                
                item = ItemLoader(item=KLItem(),selector=link)
                item.add_value('domain_name',self.domain_name)
                item.add_xpath('file_name','.//text()')
                item.add_value('file_urls',response.urljoin(href))
                yield item.load_item()


    def _scrapText(self, response):
        
        item = ItemLoader(item=KLItem(),selector=response)
        item.add_value('domain_name',self.domain_name)
        item.add_xpath('text_extracted','//div/p/span/text()')
        item.add_value('file_name',response.request.url.split('/')[-1])
        yield item.load_item()

