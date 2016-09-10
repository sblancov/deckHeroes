from scrapy.exporters import JsonItemExporter


class DeckheroesPipeline(object):

    def __init__(self):
        factions = ['human', 'faen', 'neander', 'mortii']
        self.exporters = {}
        for i in factions:
            file_ = open('data/{}.json'.format(i), 'w')
            self.exporters[i] = JsonItemExporter(file_)

    def process_item(self, item, spider):
        faction = item['faction']
        self.exporters[faction].export_item(item)
        return item
