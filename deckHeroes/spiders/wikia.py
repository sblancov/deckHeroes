import scrapy
from deckHeroes.items import CreatureItem

class WikiaSpider(scrapy.Spider):
    name = "creatures"
    allowed_domains = ['wikia.com']
    start_urls = [
        'http://deck-heroes.wikia.com/wiki/Creatures',
    ]
        

    def parse(self, response):

        tables = response.css('table')
        factions = {
            'human': 0,
            'faen': 1,
            'neander': 2,
            'mortii': 3,
        }

        for current in factions:
            current_creatures = tables[factions[current]].css('tr')
            # Remove firsh row because it contents table headers instead of a creature
            current_creatures.pop(0)
            for row in current_creatures:
                creature = CreatureItem()
                creature['name'] = row.xpath('td[1]/a/text()').extract_first()
                creature['faction'] = current
                creature['rating'] = len(row.xpath('td[2]/text()').extract_first()) - 1
                creature['attack'] = row.xpath('td[3]/text()').extract_first()[:-1]
                creature['health'] = row.xpath('td[4]/text()').extract_first()[:-1]
                creature['cost'] = row.xpath('td[5]/text()').extract_first()[:-1]
                creature['timer'] = row.xpath('td[6]/text()').extract_first()[:-1]
                creature['skill1'] = row.xpath('td[7]/a/text()').extract_first()
                creature['skill2'] = row.xpath('td[8]/a/text()').extract_first()
                creature['skill3'] = row.xpath('td[9]/a/text()').extract_first()
                yield creature
