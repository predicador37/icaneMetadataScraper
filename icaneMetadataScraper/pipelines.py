# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import re
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter


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
        file = open('metadata_historical.csv', 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['uri', 'title', 'dataUpdated', 'units', 'sourceLink', 'initialPeriod', 'lastPeriod', 'sourceLabel', 'periodicity', 'referenceArea']        
        self.exporter.start_exporting()
        
       
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
        

    def process_item(self, item, spider):

        if not item['sourceLabel'] or not item['sourceLabel'][0]:
            self.exporter.export_item(item)
            return item #return only items with any empty field
        elif not item['sourceLink'] or not item['sourceLink'][0]:
            self.exporter.export_item(item)
            return item #return only items with any empty field
        elif not item['initialPeriod'] or not item['initialPeriod'][0]:
            self.exporter.export_item(item)
            return item #return only items with any empty field
        elif not item['lastPeriod'] or not item['lastPeriod'][0]:
            self.exporter.export_item(item)
            return item #return only items with any empty field
        elif not item['periodicity'] or not item['periodicity'][0]:
            self.exporter.export_item(item)
            return item #return only items with any empty field
        elif not item['referenceArea'] or not item['referenceArea'][0]:
            self.exporter.export_item(item)
            return item #return only items with any empty field
        elif not item['dataUpdated'] or not item['dataUpdated'][0]: 
            self.exporter.export_item(item)
            return item #return only items with any empty field
        elif item['units'][0]:        
            units =  re.sub('[.]','',item['units'][0]) #remove any dot
            units = ''.join(units.split()) #remove whitespaces
            if not units:
                self.exporter.export_item(item)
                return item #return only items with any empty field
        else:
            raise DropItem("Discarded item: metadata fields filled.")  
                
        
        
    
        