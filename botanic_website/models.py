NAMES = ['scientificName', 'canonicalName', 'commonName']
CLASSIFICATION = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']


class Plant(object):
    # def __init__(self):
    #     self.names = {}
    #     self.classifications = {}
    #     self.images = {}
    #     self.descriptions = {}
    #     self.distributions = {}
    #
    # def from_json_result(self, result):
    #     if 'rank' in result.keys():
    #         self.rank = result['rank']
    #
    #     for i in range(len(NAMES)):
    #         key = NAMES[i]
    #         if key in result.keys():
    #             self.names[key] = result[key]
    #
    #     for i in range(len(CLASSIFICATION)):
    #         key = CLASSIFICATION[i]
    #         if key in result.keys():
    #             self.classifications[key] = result[key]
    #
    # def __set_name__(self, owner, name):


    @property
    def names(self):
        return self.names

    @property
    def classifications(self):
        return self.classifications



