# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import re
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter


class IcaneMetadataPipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass
        
       

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        file = open('metadata_problems.json', 'w+b')
        self.fields_to_export = ['uri','units','dataUpdated']
        self.files[spider] = file
        self.exporter = JsonItemExporter(file,fields_to_export=self.fields_to_export )
        self.exporter.start_exporting()
        if item['dataUpdated']:
            dataUpdated = ''.join(item['dataUpdated'][0].split())
            if dataUpdated:
                raise DropItem("Not empty dataUpdated field in %s" % item)
       ## if item['units']:
        ##    units =  re.sub('[.]','',item['units'][0]) #remove any dot
         ##   units = ''.join(units.split()) #remove whitespaces
          ##  if units:
           ##     raise DropItem("Not empty unit field in %s" % item)

            else:
                self.exporter.export_item(item)
                return item #return only objects with empty units
        
    
        