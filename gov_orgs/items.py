import scrapy

class GovOrgsItem(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    
    misc_info = scrapy.Field()
    address = scrapy.Field()
    address_line_1 = scrapy.Field()
    address_line_2 = scrapy.Field()
    address_line_3 = scrapy.Field()
    address_line_4 = scrapy.Field()
    address_line_5 = scrapy.Field()

    # head of organization information
    hod_designation = scrapy.Field()
    hod_name = scrapy.Field()
    hod_contact = scrapy.Field()
    
    # temporary attribute to hold contact person information
    cp_info = scrapy.Field()
    
    cp_designation = scrapy.Field()
    cp_name = scrapy.Field()
    cp_contact = scrapy.Field()
    
    # temporary attribute to hold general information
    g_info = scrapy.Field()

    gi_telephone = scrapy.Field()
    gi_fax = scrapy.Field()
    gi_email = scrapy.Field()
    gi_website = scrapy.Field()
    
    services = scrapy.Field()
    # pass
