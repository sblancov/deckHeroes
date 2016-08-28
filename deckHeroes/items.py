import scrapy


class CreatureItem(scrapy.Item):
    name = scrapy.Field()
    faction = scrapy.Field()
    rating = scrapy.Field()
    attack = scrapy.Field()
    health = scrapy.Field()
    cost = scrapy.Field()
    timer = scrapy.Field()
    skill1 = scrapy.Field()
    skill2 = scrapy.Field()
    skill3 = scrapy.Field()
