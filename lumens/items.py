# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re 

def extract_number(string):
    try:
        return re.findall('\d+',string[0])[0]
    except :
        pass

class LumensItem(scrapy.Item):
    name = scrapy.Field()
    sku = scrapy.Field()
    GTIN = scrapy.Field()
    color = scrapy.Field()
    finish = scrapy.Field() # same as color
    price = scrapy.Field()
    product_description = scrapy.Field()
    technical_description = scrapy.Field()
    display_dimentions = scrapy.Field()
    length = scrapy.Field(
        output_processor = extract_number
    )
    width = scrapy.Field(
        output_processor = extract_number
    )
    height = scrapy.Field(
        output_processor = extract_number
    )
    depth = scrapy.Field(
        output_processor = extract_number
    )
    diametre = scrapy.Field(
        output_processor = extract_number
    )
    weight = scrapy.Field(
        output_processor = extract_number
    )
    arm_height = scrapy.Field()
    seat_height = scrapy.Field()
    table_clearance_height = scrapy.Field()
    maximum_dimentions = scrapy.Field()
    images = scrapy.Field()
    swatch_images = scrapy.Field()
    pdfs = scrapy.Field()
    installations = scrapy.Field()
    designer = scrapy.Field()
    collection = scrapy.Field()
    category = scrapy.Field()
    available_new = scrapy.Field()
    made_in = scrapy.Field()
    voltage = scrapy.Field(
        output_processor = extract_number
    )
    bulb_type = scrapy.Field()
    bulb_text = scrapy.Field()
    canopy_dimentions = scrapy.Field()
    ul_listed = scrapy.Field()
    certification = scrapy.Field()
    warranty_care = scrapy.Field()
    position = scrapy.Field()
    notes = scrapy.Field()
    url = scrapy.Field()
