from scrapy import Request, Spider

from deckHeroes.items import CreatureItem

BASE_URL = 'http://deck-heroes.wikia.com'


class WikiaSpider(Spider):
    name = "creatures"
    allowed_domains = ['wikia.com']
    start_urls = [
        BASE_URL + '/wiki/Creatures',
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
                creature_url = row.xpath('td[1]/a/@href').extract_first()
                yield Request(BASE_URL + creature_url, callback=self.parse_creature)


    def parse_creature(self, response):

        aside = response.xpath('//aside')[0]

        def skill_link(number):
            skill_with = aside.xpath('div[{}]/div/a/text()'.format(number))
            if not skill_with:
                return aside.xpath('div[{}]/div/text()'.format(number))
            return skill_with

        creature = CreatureItem()
        creature['image'] = aside.xpath('nav//a//img/@src').extract_first()
        creature['name'] = aside.xpath('h2/center/text()').extract_first().lower()
        creature['faction'] = aside.xpath('div[1]//a/text()').extract_first().lower()
        creature['rating'] = len(aside.xpath('div[2]/div/text()').extract_first())
        creature['timer'] = aside.xpath('div[3]/div/text()').extract_first()
        creature['cost'] = aside.xpath('div[4]/div/text()').extract_first()
        creature['attack'] = aside.xpath('div[5]/div/text()').extract_first()
        creature['health'] = aside.xpath('div[6]/div/text()').extract_first()
        role = aside.xpath('div[7]/h3/text()').extract_first()
        if role == 'Role':
            creature['role'] = aside.xpath('div[7]//a/text()').extract_first().lower()
            creature['skill1'] = skill_link(8).extract_first().lower()
            creature['skill2'] = skill_link(9).extract_first().lower()
            creature['skill3'] = skill_link(10).extract_first().lower()
        else:
            creature['role'] = ''
            creature['skill1'] = skill_link(7).extract_first().lower()
            creature['skill2'] = skill_link(8).extract_first().lower()
            creature['skill3'] = skill_link(9).extract_first().lower()

        return creature
