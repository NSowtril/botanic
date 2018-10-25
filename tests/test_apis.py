from botanic_website.views.apis import *
import logging
logging.basicConfig(level=logging.DEBUG)


# def test_gbif_species():
#     log = logging.getLogger('test_gbif_species')
#
#     content1 = gbif_species()
#     assert content1 is not None
#     log.debug('\n------------content-1-------------------')
#     for n in content1['results']:
#         # log.debug("  key: %s, canonicalName: %s" % (n['key'], n['canonicalName']))
#         log.debug('\n===========')
#         log.debug(n)

    # content2 = gbif_species(key="1883")
    # assert content2 is not None
    # log.debug('\n------------content-2-------------------')
    # log.debug("  key: %s, canonicalName: %s" % (content2['key'], content2['canonicalName']))
    #
    # content3 = gbif_species(name="Rose")
    # assert content3 is not None
    # log.debug('\n------------content-3-------------------')
    # for n in content3['results']:
    #     log.debug("  key: %s, scientificName: %s, canonicalName: %s" % (n['key'], n['scientificName'], n['canonicalName']))


# def test_gbif_species_match():
#     log = logging.getLogger('test_gbif_species_search')
#
#     content4 = gbif_species_match(name="rose")
#     assert content4 is not None
#     log.debug('\n------------content-4-------------------')
#     if 'usageKey' in content4:
#         log.debug('  usageKey: %s, scientificName: %s, canonicalName: %s, kingdom:%s, confidence: %s'%(content4['usageKey'], content4['scientificName'], content4['canonicalName'], content4['kingdom'], content4['confidence']))
#     else:
#         log.debug('  no match')
#     if 'alternatives' in content4:
#         log.debug("  -------alternatives---------")
#         for n in content4['alternatives']:
#             log.debug('  usageKey: %s, scientificName: %s, canonicalName: %s, kingdom:%s, confidence: %s' % (n['usageKey'], n['scientificName'], n['canonicalName'], n['kingdom'], n['confidence']))


# def test_gbif_species_search():
#     log = logging.getLogger('test_gbif_species_search')
#
#     content5 = gbif_species_search(q='rose')
#     assert content5 is not None
#     log.debug('\n------------content-5-------------------')
#     log.debug('  offset: %s, limit: %s, count: %s' % (content5['offset'], content5['limit'], content5['count']))
#     for n in content5['results']:
#         msg = '  key: %-10s, scientificName: %-40s, canonicalName: %-30s' % (n['key'], n['scientificName'], n['canonicalName'])
#         if 'kingdom' in n.keys():
#             msg = msg + (", kingdom: %-10s" % n['kingdom'])
#         if 'commonName' in n.keys():
#             msg = msg + (', commonName: %-10s' % n['commonName'])
#         log.debug(msg)


# def test_ns_global_species():
#     log = logging.getLogger('test_ns_global_species')
#     log.debug('testing ns_global_species')
#
#     content6 = ns_global_species('ELEMENT_GLOBAL.2.100925')
#     # assert content6.__len__()
#     log.debug('\n------------content-6-------------------')
#     log.debug("\n"+content6)

# def test_ns_species_images():
#     log = logging.getLogger('test_ns_species_images')
#     log.debug('testing ns_species_images')
#
#     root = ns_species_images(commonName="*eagle")
#     assert root is not None
#     log.debug(root.tag)


# def test_plant_nsdc_social():
#     log = logging.getLogger('test_plant_nsdc_social')
#     log.debug("testting plant_nsdc_social")
#
#     root = plant_nsdc_social("北京", "植物")
#     assert root is not None
#     log.debug(root.tag)


# def test_plant_nsdc_map():
#     log = logging.getLogger('test_plant_nsdc_map')
#     log.debug("testing plant_nsdc_map")
#
#     root = plant_nsdc_map('49', '114')
#     assert root is not None
#     log.debug(root.tag)

# def test_get_unsplash_photos():
#     log = logging.getLogger('test_get_unsplash_photos')
#     log.debug("testing get_unsplash_photos")
#
#     results = get_unsplash_photos()
#     log.debug(results)

# def test_get_unsplash_random_photos():
#     log = logging.getLogger('test_get_unsplash_random_photos')
#     log.debug("testing get_unsplash_random_photos")
#
#     results = get_unsplash_random_photos()
#     log.debug(results)


# def test_search_unsplash_photos():
#     log = logging.getLogger('test_search_unsplash_photos')
#     log.debug("testting get_unsplash_search_photos")
#
#     results = search_unplash_photos("Rose")
#     log.debug(results)


# def test_baidu_image_classify_plant():
#     log = logging.getLogger('test_baidu_image_classify_plant')
#     log.debug('testing baidu_image_classify_plant')
#     response, content = baidu_image_classify_plant("botanic_website/static/images/yueji.jpg")
#     assert response is not None
#     # log.debug(img)
#     # log.debug(response)
#     log.debug(content)


# def test_aliyun_plant_recognize():
#     log = logging.getLogger('test_aliyun_plant_recognize')
#     log.debug('testing Aliyun Plant Recognize.')
#     resonse, content = aliyun_plant_recognize("botanic_website/static/images/yueji.jpg")
#     assert resonse is not None
#     # log.debug(resonse)
#     log.debug(content['Result'][0]['ImageUrl'])
#
#
# def test_alicloud_geocode():
#     log = logging.getLogger('test_alicloud_geocode')
#     log.debug('testing alicloud geocode.')
#     response, content = alicloud_geocode('上海市嘉定区同济大学')
#     assert response is not None
#     log.debug(content)



class Plant(object):
    def __init__(self):
        self.names = {}
        self.classifications = {}
        self.images = {}
        self.descriptions = {}
        self.distributions = {}

    def from_json_result(self, result):
        NAMES = ['scientificName', 'canonicalName']
        CLASSIFICATION = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
        if 'rank' in result.keys():
            self.rank = result['rank']

        for i in range(len(NAMES)):
            key = NAMES[i]
            if key in result.keys():
                self.names[key] = result[key]

        for i in range(len(CLASSIFICATION)):
            key = CLASSIFICATION[i]
            if key in result.keys():
                self.classifications[key] = result[key]


def test_comb():
    log = logging.getLogger('test_comb')
    plant_info = []
    i = 0
    log.debug('\n--------- testing apis combined -----------')
    offset = 0
    r1 = gbif_species(offset=offset)
    # log.debug(r1)
    log.debug('endOfRecords: %s', r1['endOfRecords'])
    for r in r1['results']:
        plant = Plant()
        plant.from_json_result(r)
        log.debug(''.join(['\n %-10s: %-10s ' % item for item in plant.__dict__.items()]))
        log.debug(rm_ns_tag_prefix(ns_species_images(commonName='rose').tag))
        plant_info.append(plant)
        break
