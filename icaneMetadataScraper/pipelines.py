# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import re

class IcaneMetadataPipeline(object):
    def process_item(self, item, spider):
        print type(item)
        if item['units']:
            units =  re.sub('[.]','',item['units'][0]) #remove any dot
            units = ''.join(units.split()) #remove whitespaces
            if units:
                raise DropItem("Empty unit field in %s" % item)

                
            else:
                return item #return only objects with empty units