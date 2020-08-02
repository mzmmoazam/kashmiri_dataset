# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join,Identity
from w3lib.html import remove_tags

def replace_sup(res):
    return res.replace('<sup>','^').replace('</sup>','')


def remove_whitespaces(res):
    return res.strip()

def split_filename(res):
    return res.split('.')

def remove_sno(res):
    if ")" in res:
        return res[res.index(')')+1:]
    else:
        return res


def remove_reducdant(res):
    # remove word and hindi pron
    if '</d>' in res:
        return res[res.index('</d>') + 4:] # can cause bugs need a more robust fix
    else:
        return res

class KZItem(scrapy.Item):
    headword = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )
    category = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )
    englishExample = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )
    hindiMeaning = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )
    hindiExample = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )
    englishMeaning = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )
    kashmiriExample = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )

class GAGItem(scrapy.Item):
    word = scrapy.Field(
        input_processor=MapCompose(replace_sup,remove_tags,remove_whitespaces),
        output_processor=Join()
    )

    hindiPron = scrapy.Field(
        input_processor=MapCompose(replace_sup,remove_tags,remove_whitespaces),
        output_processor=Join()
    )
    meaning = scrapy.Field(
        input_processor=MapCompose(remove_reducdant,remove_tags,remove_whitespaces),
        output_processor=Join()
    )

class SHItem(scrapy.Item):
    word = scrapy.Field(
        input_processor=MapCompose(remove_sno,remove_whitespaces),
        output_processor=TakeFirst()
    )

    category = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )
    meaning = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )

    domain_name = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )
    
    file_name = scrapy.Field(
        input_processor=MapCompose(split_filename,remove_sno,remove_whitespaces),
        output_processor=TakeFirst()
    )
    
    file_urls = scrapy.Field()
    
    files = scrapy.Field()

class KLItem(scrapy.Item):
    
    domain_name = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=TakeFirst()
    )
    
    file_name = scrapy.Field(
        input_processor=MapCompose(split_filename,remove_whitespaces),
        output_processor=TakeFirst()
    )
    
    file_urls = scrapy.Field()
    
    files = scrapy.Field()
    
    text_extracted = scrapy.Field(
        input_processor=MapCompose(remove_whitespaces),
        output_processor=Join()
    )