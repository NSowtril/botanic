import httplib2
from 暂存.global_functions import parse_xml_str

ns_access_key_id = "72ddf45a-c751-44c7-9bca-8db3b4513347"
http = httplib2.Http()


def get_species_by_name(name):
    url = ('https://services.natureserve.org/idd/rest/ns/v1/globalSpecies/list/nameSearch?name=%s&NSAccessKeyId=%s'
           % (name, ns_access_key_id))
    # 请求接口数据
    response = http.request(url, 'GET')[1].decode('utf-8')
    xml_root = parse_xml_str("global_species.xml", response)


def get_species_by_id(uid):
    url = ("https://services.natureserve.org/idd/rest/ns/v1.1/globalSpecies/comprehensive?uid=%s&NSAccessKeyId=%s"
           % (uid, ns_access_key_id))
    response = http.request(url, 'GET')[1].decode('utf-8')
    xml_root = parse_xml_str("global_species.xml", response)


def get_species_images_by_id(uid):
    url = ("https://services.natureserve.org/idd/rest/ns/v1/globalSpecies/images?uid=%s&NSAccessKeyId=%s"
           % (uid, ns_access_key_id))
    response = http.request(url, 'GET')[1].decode('utf-8')
    xml_root = parse_xml_str("global_species.xml", response)


def get_species_images_by_scientific_name(sname):
    url = ("https://services.natureserve.org/idd/rest/ns/v1/globalSpecies/images?scientificName=%s&NSAccessKeyId=%s"
           % (sname, ns_access_key_id))
    response = http.request(url, 'GET')[1].decode('utf-8')
    xml_root = parse_xml_str("global_species.xml", response)


def get_species_images_by_common_name(cname):
    url = ("https://services.natureserve.org/idd/rest/ns/v1/globalSpecies/images?commonName=%s&NSAccessKeyId=%s"
           % (cname, ns_access_key_id))
    response = http.request(url, 'GET')[1].decode('utf-8')
    xml_root = parse_xml_str("global_species.xml", response)


