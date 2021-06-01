import scrapy
from scrapy import Request 
from scrapy.loader import ItemLoader
from lumens.items import LumensItem
#import chompjs
import math
import re
import json
from math import ceil
from scrapy.shell import inspect_response

class InfosSpider(scrapy.Spider):
    name = 'infos'
    allowed_domains = ['lumens.com']
    start_urls = ['https://www.lumens.com/bend-goods/?sz=96']

    def __init__(self):
        self.search_template = 'https://www.lumens.com/bend-goods/?sz=96&start={}'
        self.total_product_per_page = 96
        self.product_variation_template = '?dwvar_{}_AttrValue1={}'


    def parse(self, response):
        total_page = ceil(int(response.xpath('//span[@class="total-sort-count"]/text()').re('\d+')[0])/29)
        #inspect_response(response, self)
        for page_id in range(total_page):
            yield Request(
                self.search_template.format(page_id*self.total_product_per_page),
                callback = self.parse_page
            )

    def parse_page(self,response):
        products_urls = set(response.xpath('//a[@class="thumb-link"]/@href').getall())
        base_url = 'https://www.lumens.com/'
        for url in products_urls :
            yield Request(
                base_url + url,
                callback = self.parse_product
            )

    def parse_product(self,response): 
        product_id = self.get_product_id(response)
        colors = response.xpath('//img[@class="rounded-circle swatch-image-style swatch-prod-img"]/@alt').getall()
        for color in colors :
            yield Request(
                response.url + self.product_variation_template.format(product_id,color),
                callback = self.parse_product_variations,
                meta={
                    'color':color
                }

            )

            
    def parse_product_variations(self,response):
        data = json.loads(response.xpath('//div[@class="selectedVariant"]/text()').get())
        loader = ItemLoader(LumensItem(),response)

        loader.add_value('name',data['variant']['productName'])
        loader.add_value('sku',data['variant']['skuId'])
        loader.add_value('color',response.meta['color'])
        loader.add_value('finish',response.meta['color'])
        loader.add_value('price',data['variant']['price']['salePrice'])
        loader.add_value('product_description',self.get_description(response))  
        #loader.add_value('technical_description',self.get_technical_description(response))
        loader.add_xpath('display_dimentions','//span[contains(text(),"Dim")]/following-sibling::ul/li[1]/text()')
        
        loader.add_value('width',self.get_width(response))
        loader.add_value('height',self.get_height(response))
        loader.add_value('depth',self.get_depth(response))
        loader.add_value('weight',self.get_weight(response))

        loader.add_value('seat_height',self.get_seat_height(response))
        loader.add_xpath('maximum_dimentions','//span[contains(text(),"Dimensions")]/following-sibling::ul/li/text()')
        loader.add_xpath('images','//img[@class="lazyload"]/@src')

        loader.add_value('swatch_images',self.get_swatch_images_urls(response))
        loader.add_value('made_in',self.get_made_in(response))
        
        loader.add_value('warranty_care',self.get_warranty(response))
        loader.add_value('voltage',self.get_voltage(response))
        loader.add_value('bulb_text',self.get_bulb_text(response))
        loader.add_value('bulb_type',self.get_bulb_type(response))
        loader.add_value('category',data['variant']['prodCat'])
        loader.add_value('available_new',data['variant']['availabilityMessage'])
        loader.add_value('designer',data['variant']['prodBrand'])
        loader.add_value('collection',loader._values['name'][0].split()[0])
        #loader.add_xpath('length','//span[contains(text(),"Dim")]/following-sibling::ul/li[1]/text()')
        loader.add_value('url',response.url)
        yield loader.load_item()
        


    def get_swatch_images_url(self,string):
        url = string.replace("background-image:url('",'').replace("')",'')
        return url 
    
    def get_swatch_images_urls(self,response):
        swatch_urls = response.xpath('//ul[@class="viewer-thumbs justify-content-center"]/li/@style').re(r"'[\s\S]+'")
        return [self.get_swatch_images_url(url.replace("'",'')) for url in swatch_urls]
    

    def get_bulb_text(self,response):
        return response.xpath('//span[contains(text(),"Lighting")]/following-sibling::ul/li/text()').get()

    def get_voltage(self,response):
        try:
            payload = self.get_bulb_text(response)
            return re.findall('\d+ Volt',payload)[0]
        except:
            return ''
    
    def get_bulb_type(self,response):
        try:
            payload = self.get_bulb_text(response)
            return payload.split('Volt')[-1]
        except:
            return ''

    def get_dimentions(self,response):
        return response.xpath('//span[contains(text(),"Dim")]/following-sibling::ul/li/text()').getall()


    def get_product_id(self,response):
        url = response.url 
        return url.split('-')[-1].replace('.html','')

    def get_description(self,response):
        return ''.join(response.xpath('//div[@class="mt-2 mr-3 font-weight-medium detabs-details"]//text()').getall())
    
    def get_technical_description(self,response):
        return ''.join(response.xpath('//div[@class="details-tab-specifications mb-2 pb-3 mr-3 font-weight-medium detabs-details"]//text()').getall())

    def get_length(self,response):
        pass
    
    def get_width(self,response):
        try: 
            return response.xpath('//span[contains(text(),"Dim")]/following-sibling::ul/li[1][contains(text(),"Width")]').re('Width \d+')[0]
        except:
            return ''

    def get_height(self,response):
        try:
            return response.xpath('//span[contains(text(),"Dim")]/following-sibling::ul/li[1][contains(text(),"Width")]').re('Width \d+')
        except:
            return ''

    def get_depth(self,response):
        try:
            return response.xpath('//span[contains(text(),"Dim")]/following-sibling::ul/li[1][contains(text(),"Depth")]').re('Depth \d+')
        except:
            return ''
    def get_weight(self,response):
        try:
            return response.xpath('//span[contains(text(),"Dim")]/following-sibling::ul/li[1][contains(text(),"Weight")]').re('Weight \d+')
        except:
            return ''

    def get_length(self,response):
        try: 
            return response.xpath('//span[contains(text(),"Dim")]/following-sibling::ul/li[contains(text(),"Length")]').re('Length \d+')
        except:
            return ''        

    def get_seat_height(self,response):
        payload = response.xpath('//span[contains(text(),"Dim")]/following-sibling::ul/li[2]/text()').get()
        try :
            return payload.split(':')[-1]
        except:
            return ''

    def get_made_in(self,response):
        return response.xpath('//li[contains(text(),"Made")]/text()').get().split()[-1]

    def get_warranty(self,response):
        try:
            return response.xpath('//ul[@class="attributes"]//li[contains(text(),"Warranty")]/text()').get().split(' ',1)[-1]
        except:
            return ''