# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class IcaneMetadataItem(Item):
    # define the fields for your item here like:
     sourceLabel = Field()
     sourceLink = Field()
     initialPeriod = Field()
     lastPeriod = Field()
     units = Field()
     periodicity = Field()
     referenceArea = Field()
     dataUpdated = Field()
