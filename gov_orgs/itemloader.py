from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst


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

def GrabFirst(value):
    try:
        return (i for i in value if i)
    except ValueError:
        pass

class GovOrgsItemLoader(ItemLoader):
    # default single value fields
    # default_input_processor = TakeFirst

    # address is a multi-valued field
    address_in = MapCompose(Strip, Split) #, ReplaceNoneType, )

    # misc information
    # misc_info = MapCompose(TakeFirst)

    # customizing the Join function to use
    Join_services = Join(' : ')
    # services is a muti-valued field
    services_in = Join_services

    