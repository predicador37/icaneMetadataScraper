from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from icaneMetadataScraper.items import IcaneMetadataItem
import uri_util

class IcaneMetadataSpider(BaseSpider):

    API_CALL_URI = 'http://www.icane.es/metadata/api/regional-data/economy/time-series-list'    
    #API_CALL_URI = 'http://www.icane.es/metadata/api/municipal-data/society/education/time-series-list'
        
    name = "metadata"
    allowed_domains = ["icane.es"]
    start_urls = uri_util.getUris(API_CALL_URI)
    #[
    #    "http://www.icane.es/data/historical-data/economy/labour-market/all-workers-affiliated-social-security-regimes-1988-2000#timeseries",
#"http://www.icane.es/data/regional-data/society/health-social-welfare/disabled-population-need-reception-social-health-services-gender#timeseries"
#    ]
    
   
        
    def parse(self, response):
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
        metadata['dataUpdated'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='rgtmetadata']/ul/li[3]/span[2]/@content").extract()
        return metadata
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
