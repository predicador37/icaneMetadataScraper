from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from icaneMetadataScraper.items import IcaneMetadataItem
from scrapy.http.request import Request
import uri_util

class IcaneMetadataSpider(BaseSpider):

    API_CALL_URI = 'http://www.icane.es/metadata/api/regional-data/time-series-list'
        
    name = "metadata"
    start_urls = []
    allowed_domains = ["icane.es"]
    other_urls = uri_util.getUris(API_CALL_URI) #all urls
    start_urls.append(other_urls[0]) #first one here
    
   
        
    def parse(self, response):
        items = []
        x = HtmlXPathSelector(response)
        metadata = IcaneMetadataItem()
        metadata['uri'] = response.url   
        metadata['sourceLabel'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[1]/span/a/text()").extract()
        metadata['sourceLink'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[1]/span/a/@href").extract()
        if not metadata['sourceLabel']:
            metadata['sourceLabel'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[1]/span[2]/span/text()").extract()
            metadata['sourceLink']=['']
        metadata['initialPeriod'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[2]/span[2]/text()").extract()
        metadata['lastPeriod'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[3]/span[2]/text()").extract()
        metadata['units'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[4]/text()").extract()
        metadata['periodicity'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='rgtmetadata']/ul/li[1]/span[2]/text()").extract()
        metadata['referenceArea'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='rgtmetadata']/ul/li[2]/span[2]/span[2]/text()").extract()
        #metadata['dataUpdated'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='rgtmetadata']/ul/li[3]/span[2]/@content").extract()
        metadata['dataUpdated'] =  x.select("//html/body/div[4]/div/div[2]/ul/li[3]/span[2]/@content").extract()
        items.append(metadata)
        
        uri_to_remove = response.url + '#timeseries'
        self.other_urls.remove(uri_to_remove)
        if self.other_urls:
            r = Request(url=self.other_urls[0], callback=self.parse)
            items.append(r)        
        
        return items