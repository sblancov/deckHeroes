import json


class DeckheroesPipeline(object):

    def __init__(self):

        factions = ['human', 'faen', 'neander', 'mortii']
        self.files = {}
        for i in factions:
            self.files[i] = open('{}.json'.format(i), 'w') 

    def process_item(self, item, spider):
        faction = item['faction']
        line = json.dumps(dict(item), indent=4) + ", "
        self.files[faction].write(line)
        return item
