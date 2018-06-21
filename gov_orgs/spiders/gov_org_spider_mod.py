import scrapy
from gov_orgs.items import GovOrgsItem
from gov_orgs.itemloader import GovOrgsItemLoader

import datetime as dt
from bs4 import BeautifulSoup as bs


class GovOrgSpider(scrapy.Spider):
    name = "gov_org"
    base_url = "http://www.gic.gov.lk"

    def start_requests(self):
        self.log('%s Scraping started.' % dt.datetime.now())
        urls = [
            "http://www.gic.gov.lk/gic/index.php/en/component/org/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_and_extract_base_urls)
    
    def parse_and_extract_base_urls(self, response):
        categories = response.css('a.componentheading2::text').extract()
        urls = response.css('a.componentheading2::attr(href)').extract()
        for i in range(len(categories)):
            req = scrapy.Request(url=GovOrgSpider.base_url+urls[i], callback=self.parse_and_extract_urls)
            req.meta['category'] = categories[i]
            yield req
    

    def parse_and_extract_urls(self, response):
        organizations = response.css('td a::text').extract()[:-2]
        urls = response.css('td a::attr(href)').extract()
        for i in range(len(organizations)):
            req = scrapy.Request(url=GovOrgSpider.base_url+urls[i], callback=self.parse)
            req.meta['category'] = response.meta['category']
            req.meta['name'] = organizations[i]
            yield req
        
        
    def parse(self, response):
        item_loader = GovOrgsItemLoader(item=GovOrgsItem(), response=response)
        
        # apparently no further processing required
        item_loader.add_value('category', response.meta['category'])
        item_loader.add_value('name', response.meta['name'])

        # head of organization information
        item_loader.add_value('hod_designation', response.css('div#minister-des p b::text').extract_first())
        item_loader.add_value('hod_name', response.css('div#minister-des p::text').extract_first())
        item_loader.add_value('hod_contact', response.css('div#minister-des::text').extract_first())

        # Storing values for further processing
        rows = response.xpath('//table/tr/td/p').extract()

        # determining the contact person section
        cp_line = sum(rows.index(line)+1 for line in rows if "Contact Person" in line)
        # determining the general information section
        gi_line = sum(rows.index(line)+1 for line in rows if "General Information" in line)

        # output proccesor for address formatting
        item_loader.add_value('address', bs(rows[0]))
        item_loader.add_value('misc_info', [bs(row) for row in rows[1:cp_line-1]])

        # Contact person information for further processing
        item_loader.add_value('cp_info', bs(rows[cp_line]).get_text())        

        # General organization information for further processing
        item_loader.add_value('g_info', [bs(row) for row in rows[gi_line].split('<br>', 3)])

        # output processor to format the list of services
        services = response.xpath('//table/tr/td/a/text()').extract()
        item_loader.add_value('services', services)

        return item_loader.load_item()
        

        
        