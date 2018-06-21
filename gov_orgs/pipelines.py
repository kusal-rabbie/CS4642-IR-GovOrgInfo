import scrapy, csv, json, logging
from bs4 import BeautifulSoup as bs
from gov_orgs.items import GovOrgsItem
from scrapy.exceptions import DropItem


class GInformationPipeline(object):
    address_lines = 5
    
    @staticmethod
    def extract_info(value):
        return value.get_text().split(':')[-1].replace(',',':')

    def process_item(self, item, spider):

        extract_info = GInformationPipeline.extract_info
        n = GInformationPipeline.address_lines

        try:    
            # populate address fields
            lines = item.pop('address')
            count = min(n,len(lines))
            for i in range(count):
                item['address_line_' + str(i+1)] = lines[i]
            if count < n:
                for i in range (n-count):
                    item['address_line_' + str(n-i)] = ''
        except IndexError:
            logging.log(logging.INFO,('%s has no address'%item['name']))
            pass
        finally:
            try:
                # populating general information fields
                gi_telephone, gi_fax, gi_email, gi_website = item.pop('g_info')
                item['gi_telephone'] = extract_info(gi_telephone)
                item['gi_fax'] = extract_info(gi_fax)
                item['gi_email'] = extract_info(gi_email)
                item['gi_website'] = gi_website.a['href']
            except IndexError:
                logging.log(logging.INFO,('%s has no general information'%item['name']))
                # process g_info
                pass
            finally:
                # populating misc_info if available
                try:
                    misc_info = item.pop('misc_info')
                    misc_info = ' : '.join([line.get_text() for line in misc_info])
                    item['misc_info'] = misc_info
                except KeyError:
                    pass
                except TypeError:
                    pass
                finally:
                    return item


class CPInformationPipeline(object):

    def process_item(self, item, spider):
        try:
            # print item['cp_info']
            cp_name, cp_designation, cp_contact = item.pop('cp_info')[0].split(':',2)
            print cp_name
            item['cp_name'] = cp_name.replace('Designation','')
            item['cp_designation'] = cp_designation.replace('Tel','')
            item['cp_contact'] = cp_contact
        except IndexError:
            # process cp_info
            logging.log(logging.INFO,('%s has no contact person information '%item['name']))
            pass
        finally:
            return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('gov_orgs.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        return item

            