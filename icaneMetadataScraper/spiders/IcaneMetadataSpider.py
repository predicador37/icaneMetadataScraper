from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from icaneMetadataScraper.items import IcaneMetadataItem

class IcaneMetadataSpider(BaseSpider):
    name = "metadata"
    allowed_domains = ["icane.es"]
    start_urls = [
        "http://www.icane.es/data/regional-data/society/health-social-welfare/nhs-2012-population-health-status-last-12-months-gender#timeseries",
"http://www.icane.es/data/regional-data/society/health-social-welfare/disabled-population-need-reception-social-health-services-gender#timeseries"
    ]

    def parse(self, response):
        x = HtmlXPathSelector(response)
        metadata = IcaneMetadataItem()
        metadata['uri'] = response.url   
        metadata['sourceLabel'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[1]/span/a/text()").extract()
        metadata['sourceLink'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[1]/span/a/@href").extract()
        metadata['initialPeriod'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[2]/span[2]/text()").extract()
        metadata['lastPeriod'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[3]/span[2]/text()").extract()
        metadata['units'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='lftmetadata']/ul/li[4]/text()").extract()
        metadata['periodicity'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='rgtmetadata']/ul/li[1]/span[2]/text()").extract()
        metadata['referenceArea'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='rgtmetadata']/ul/li[2]/span[2]/span[2]/text()").extract()
        metadata['dataUpdated'] = x.select("//div[@id='contFooter']/div[@id='footer']/div[@id='rgtmetadata']/ul/li[3]/span[2]/@content").extract()
        return metadata
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
