import scrapy
from gov_orgs.items import GovOrgsItem
from gov_orgs.GovOrgsItemLoader import GovOrgsItemLoader

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
        hod_designation = response.css('div#minister-des p b::text').extract_first()
        hod_name = response.css('div#minister-des p::text').extract_first()
        hod_contact = response.css('div#minister-des::text').extract_first()

        item_loader.add_value('hod_designation', hod_designation)
        item_loader.add_value('hod_name', hod_name)
        item_loader.add_value('hod_contact', hod_contact)

        # Storing values for further processing
        rows = response.xpath('//table/tr/td/p').extract()

        # output proccesor for address formatting
        item_loader.add_value('address', bs(rows[0]))

        if "Contact Person" in rows[1]:
            cp_line = 2
        else:
            cp_line = 3

        # Contact person information for further processing
        cp_info = bs(rows[cp_line]).get_text()
        try:
            cp_info = cp_info.split(':', 2)
            item_loader.add_value('cp_designation', cp_info[1])
            item_loader.add_value('cp_name', cp_info[0])
            item_loader.add_value('cp_contact',cp_info[2])
        except IndexError:
            item_loader.add_value('cp_info', cp_info)
        

        # General organization information for further processing
        g_info = rows[cp_line+2].split('<br>', 3)
        try:
            item_loader.add_value('gi_telephone', g_info[0])
            item_loader.add_value('gi_fax', g_info[1])
            item_loader.add_value('gi_email', g_info[2])
        except IndexError:
            item_loader.add_value('g_info', g_info)

        # no further processing required
        item_loader.add_value('gi_website', bs(rows[cp_line+2]).a['href'])

        # output processor to format the list of services
        services = response.xpath('//table/tr/td/a/text()').extract()
        item_loader.add_value('services', services)

        return item_loader.load_item()
        

        
        