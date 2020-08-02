# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
import mimetypes
import scrapy
import os




class KashmiriDatasetPipeline(FilesPipeline):
    
    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        return [scrapy.Request(u,meta={'file_name': item.get('file_name'),"domain_name":item.get('domain_name')}) for u in urls]
    
    def file_path(self, request, response=None, info=None):
        domain_name = request.meta['domain_name']
        media_guid = request.meta['file_name']
        media_ext = os.path.splitext(request.url)[1]
        
        # Handles empty and wild extensions by trying to guess the
        # mime type then extension or default to empty string otherwise
        if media_ext not in mimetypes.types_map:
            media_ext = ''
            media_type = mimetypes.guess_type(request.url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        return '%s/%s%s' % (domain_name,media_guid, media_ext)
    
    

