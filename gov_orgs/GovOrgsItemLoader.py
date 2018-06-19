from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose, Identity


def Split(value, separator=','):
    try:
        return value.split(separator)
    except ValueError:
        pass

def Strip(value, separator=u'\r'u'\n'):
    try:
        return value.get_text().strip().replace(separator,'')
    except ValueError:
        pass

class GovOrgsItemLoader(ItemLoader):
    address_in = MapCompose(Strip, Split) #, ReplaceNoneType, )

    Join_services = Join(' : ')
    services_in = Join_services

    