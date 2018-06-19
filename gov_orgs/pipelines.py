# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy, csv, json
from gov_orgs.items import GovOrgsItem
from scrapy.exceptions import DropItem

class GInformationPipeLine(object):
    
    @staticmethod
    def extract_info(value):
        return value[0].split('>')[-1].replace(',',':')

    def process_item(self, item, spider):
        extract_info = GInformationPipeLine.extract_info

        if item['address']:
            lines = item.pop('address')
            count = min(4,len(lines))
            for i in range(count):
                item['address_line_' + str(i+1)] = lines[i]
            if count < 4:
                for i in range (4-count):
                    item['address_line_' + str(4-i)] = ''
        else:
            # raise DropItem("Missing address in %s" % item)
            pass

        try:
            # to do
            # process this information
            g_info = item.pop('g_info')
            item['gi_telephone'] = ''
            item['gi_fax'] = ''
            item['gi_email'] = ''
            item['gi_website'] = ''
            # return item
            raise DropItem("Missing organizational information in %s" % item)
            # pass
        except KeyError:
            item['gi_telephone'] = extract_info(item['gi_telephone'])
            item['gi_fax'] = extract_info(item['gi_fax'])
            item['gi_email'] = extract_info(item['gi_email'])
            return item


class CPInformationPipeLine(object):

    def process_item(self, item, spider):
        try:
            # to do
            # process this information
            cp_info = item.pop('cp_info')
            item['cp_designation'] = ''
            item['cp_name'] = ''
            item['cp_contact'] = ''
            # return item
            raise DropItem("Missing contact person information in %s" % item)
            # pass
        except KeyError:
            item['cp_designation'] = item['cp_designation'][0].replace('Tel','')
            item['cp_name'] = item['cp_name'][0].replace('Designation','')
            return item


class JsonWriterPipeLine(object):

    def open_spider(self, spider):
        self.file = open('gov_orgs.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        return item

            