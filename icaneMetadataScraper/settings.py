# Scrapy settings for icaneMetadataScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'icaneMetadataScraper'

SPIDER_MODULES = ['icaneMetadataScraper.spiders']
NEWSPIDER_MODULE = 'icaneMetadataScraper.spiders'
ITEM_PIPELINES = [ 'icaneMetadataScraper.pipelines.IcaneMetadataPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'icaneMetadataScraper (+http://www.yourdomain.com)'
