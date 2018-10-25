import httplib2
import json
# from flask import session, flash, request
from werkzeug.exceptions import abort


import base64
import urllib
import xml.etree.ElementTree as ET
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



http = httplib2.Http()

gbif_root_url = "http://api.gbif.org/v1"


def append_url_param(url, param_name, param_value):
    error = None
    if url is None:
        error = 'url required.'
    elif param_name is None:
        error = 'param_name required.'
    elif param_value is not None:
        url = url + "&%s=%s" % (param_name, param_value.replace(' ', '%20'))

    if error is not None:
        abort(404, error)

    return url


# name：学名和俗名，区分大小写，前端精确匹配

def gbif_species(name=None, offset="0", limit="20"):
    url = gbif_root_url + '/species?'

    url = append_url_param(url, 'name',name)
    url = url + ('&offset=%s&limit=%s' % (offset, limit))

    response, content = http.request(url, 'GET')
    content = json.loads(content.decode('utf-8'))

    return content


# key：物种在gbif中的ID
def gbif_species_feature(key=None, feature=None):
    FEATURES = {'name', 'parents', 'children', 'related', 'synonyms', 'descriptions', 'distributions', 'media', 'references', 'speciesProfiles', 'vernacularNames', 'typeSpecimens'}

    error = None
    if key is None:
        error = 'GBIF ID required.'
    if feature is not None:
        if feature not in FEATURES:
            error = 'Invalid feature'

    if error is not None:
        abort(404, error)

    url = gbif_root_url + "/species/%s" % key
    if feature is not None:
        url = url + "/%s" % feature

    response, content = http.request(url, 'GET')
    content = json.loads(content.decode('utf-8'))

    return content



RANK = ["DOMAIN","SUPERKINGDOM","KINGDOM","SUBKINGDOM","INFRAKINGDOM","SUPERPHYLUM","PHYLUM","SUBPHYLUM","INFRAPHYLUM","SUPERCLASS","CLASS","SUBCLASS","INFRACLASS","PARVCLASS","SUPERLEGION","LEGION","SUBLEGION","INFRALEGION","SUPERCOHORT","COHORT","SUBCOHORT","INFRACOHORT","MAGNORDER","SUPERORDER","GRANDORDER","ORDER","SUBORDER","INFRAORDER","PARVORDER","SUPERFAMILY","FAMILY","SUBFAMILY","INFRAFAMILY","SUPERTRIBE","TRIBE","SUBTRIBE","INFRATRIBE","SUPRAGENERIC_NAME","GENUS","SUBGENUS","INFRAGENUS","SECTION","SUBSECTION","SERIES","SUBSERIES","INFRAGENERIC_NAME","SPECIES_AGGREGATE","SPECIES","INFRASPECIFIC_NAME","GREX","SUBSPECIES","CULTIVAR_GROUP","CONVARIETY","INFRASUBSPECIFIC_NAME","PROLES","RACE","NATIO","ABERRATION","MORPH","VARIETY","SUBVARIETY","FORM","SUBFORM","PATHOVAR","BIOVAR","CHEMOVAR","MORPHOVAR","PHAGOVAR","SEROVAR","CHEMOFORM","FORMA_SPECIALIS","CULTIVAR","STRAIN","OTHER","UNRANKED"]
KINGDOM = ["INCERTAE_SEDIS","ANIMALIA","ARCHAEA","BACTERIA","CHROMISTA","FUNGI","PLANTAE","PROTOZOA","VIRUSES"]


# 模糊匹配
# name：查询字段
# rank：查询分级
# kingdom：界
# phylum：门
# class：纲
# order：目
# family：科
# genus：属
def gbif_species_match(name=None, rank=None, kingdom=None, phylum=None, _class=None, order=None, family=None, genus=None, verbose="true"):
    url = gbif_root_url + '/species/match?verbose=%s'%verbose
    error = None

    if name is None:
        error = 'name required.'
    else:
        url = append_url_param(url, "name", name)
        if rank is not None:
            if rank not in RANK:
                error = 'Invalid rank.'
            else:
                url = append_url_param(url, "rank", rank)
        if kingdom is not None:
            if kingdom not in KINGDOM:
                error = 'Invalid kingdom.'
            else:
                url = append_url_param(url, "kingdom", kingdom)
        url = append_url_param(url, "phylum", phylum)
        url = append_url_param(url, "class", _class)
        url = append_url_param(url, "order", order)
        url = append_url_param(url, "family", family)
        url = append_url_param(url, "genus", genus)

    if error is not None:
        abort(404, error)

    response, content = http.request(url, 'GET')
    content = json.loads(content.decode('utf-8'))
    return content


# 全文搜索，结果按相关性排序
# q：查询字段
# rank：查询分级
# isExtinct：现存与否
def gbif_species_search(q=None, rank=None, isExtinct=None, limit=20, offset="0"):
    url = gbif_root_url + "/species/search"

    error = None

    if q is None:
        error = 'No query input.'
    else:
        url = url + ("?q=%s" % q)
        url = append_url_param(url, "rank", rank)
        url = append_url_param(url, "isExtinct", isExtinct)
        url = append_url_param(url, 'offset', offset)
        url = append_url_param(url, 'limit', limit)

    if error is not None:
        abort(404, error)

    response, content = http.request(url, 'GET')
    content = json.loads(content.decode('utf-8'))

    return content


NSAccessKeyId = "72ddf45a-c751-44c7-9bca-8db3b4513347"
def ns_global_species(uid=None):
    url = "https://services.natureserve.org/idd/rest/ns/v1.1/globalSpecies/comprehensive"
    error = None
    if uid is None:
        error = 'uid required.'
    else:
        url = url + ("?uid=%s&NSAccessKeyId=%s" % (uid, NSAccessKeyId))

    if error is not None:
        abort(404, error)

    response, content = http.request(url, 'GET')
    root = ET.fromstring(content)
    # tree = ET.parse('response.xml')
    # root = tree.getroot()

    results = ""
    schema_location = '{http://services.natureserve.org/docs/schemas/biodiversityDataFlow/1}'
    for name in root.findall('.//'+add_ns_tag_prefix('names')+'/*'):
        results += "----------------------------------------------\n >> "
        results += rm_ns_tag_prefix(name.tag) + ": " +name.text + "\n"
        for n in name.findall('./*'):
            results += (" >>>>  " + rm_ns_tag_prefix(n.tag) + ": " + n.text + " ")
            for i in n.items():
                results += "    | " + i[0] + ": " + i[1] + "  "
            results += "\n"

    return results

ns_tag_prefix = '{http://services.natureserve.org/docs/schemas/biodiversityDataFlow/1}'
def rm_ns_tag_prefix(tag):
    return tag.replace(ns_tag_prefix, '')
def add_ns_tag_prefix(tag):
    return ns_tag_prefix+tag

# 支持通配符
# includeSynonyms: 检索同义字段
def ns_species_images(uid=None, scientificName=None, includeSynonyms='N', commonName=None, resolution=None):
    url = "https://services.natureserve.org/idd/rest/ns/v1/globalSpecies/images?includeSynonyms=%s&NSAccessKeyId=%s" % (includeSynonyms, NSAccessKeyId)
    error = None

    if (uid is None) & (scientificName is None) & (commonName is None):
        error = 'uid, scientificName or commonName required.'

    if error is not None:
        abort(400, error)

    url = append_url_param(url, "uid", uid)
    url = append_url_param(url, "scientificName", scientificName)
    url = append_url_param(url, "commonName", commonName)
    url = append_url_param(url, "resolution", resolution)

    header, content = http.request(url, 'GET')
    # content = content.decode('utf-8')
    root = ET.fromstring(content)

    return root


# 支持学名和拉丁名查询
# nmae: 植物名称，拉丁学名或中文名
# ntype: chname-中文名，sname-拉丁学名
def plant_nsdc_image(name=None, ntype="chname"):
    NTYPE = {'chanem', 'sname'}
    url = "http://www.plant.csdb.cn/api.php?"
    error = None

    if name is None:
        error = 'plant name required.'
    if ntype not in NTYPE:
        error = 'Invalid ntype.'

    if error is not None:
        abort(404, error)

    response, content = http.request(url, 'GET')
    root = ET.fromstring(content.decode('utf-8'))

    return root


PROVINCES = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西",
             "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃",
             "青海", "宁夏", "新疆", "香港", "澳门", "台湾"]


# 植物领域社交媒体数据
def plant_nsdc_social(p=None, s=None):
    url = "http://www.plant.nsdc.cn/api_social.php"
    error = None
    if p is None:
        error = 'Province required.'
    elif s is None:
        error = 'Search keyword required.'
    else:
        if p not in PROVINCES:
            error = 'Invalid province.'
        else:
            url = url + ("?p=%s&s=%s" % (p, s))

    if error is not None:
        abort(404, error)

    response, content = http.request(url, 'GET')
    root = ET.fromstring(content)

    return root


# plant_nsdc地图API
def plant_nsdc_map(lat=None, lng=None):
    url = "http://www.plant.nsdc.cn/api_spm.php"
    error = None
    if lat is None:
        error = 'Latitude required.'
    elif lng is None:
        error = 'Longitude required.'
    else:
        url = url + ("?lat=%s&lng=%s" % (lat, lng))

    if error is not None:
        abort(404, error)

    response, content = http.request(url, 'GET')
    root = ET.fromstring(content)

    return root


unsplash_client_id = "Client-ID b5b4bc0d17d1e3e9523768a01b0bb9e954b6df83922548aef16bf65cae372664"
unsplash_base_url ="https://api.unsplash.com"
unsplash_headers = {
        "Authorization": ("%s" % unsplash_client_id)
    }


def get_unsplash_photos(page="1", per_page="10", order_by="latest", id=None, w=None, h=None, rect=None):
    url = unsplash_base_url+"/photos"
    headers = unsplash_headers
    if id is not None:
        url = url + ("/%s?" % id)
        url = append_url_param(url, "w", w)
        url = append_url_param(url, "h", h)
        url = append_url_param(url, "rect", rect)
    else:
        url = url + ("?")
    url = url+("&page=%s&per_page=%s&order_by=%s" % (page, per_page, order_by))
    results = json.loads(http.request(url, 'GET', None, headers)[1].decode('utf-8'))

    return results


def get_unsplash_random_photos(query=None, w=None, h=None, orientation=None, count="1"):
    url = unsplash_base_url+("/photos/random?count=%s" % count)
    headers = unsplash_headers
    url = append_url_param(url, "query", query)
    url = append_url_param(url, "w", w)
    url = append_url_param(url, "h", h)
    url = append_url_param(url, "orientation", orientation)

    results = json.loads(http.request(url, 'GET', None, headers)[1].decode('utf-8'))

    return results


def search_unplash_photos(query=None, page="1", per_page="10", orientation=None):
    url = unsplash_base_url+("/search/photos?page=%s&per_page=%s" % (page, per_page))
    headers = unsplash_headers
    error = None
    if query is None:
        error = 'Missing query'
    else:
        url = url+("&query=%s" % query)
        url = append_url_param(url, 'orientation', orientation)
    results = json.loads(http.request(url, 'GET', None, headers)[1].decode('utf-8'))

    return results


# 获取百度AI Access Token
def get_baidu_access_token():
    baidu_api_key = "SpK2t9uRxCs3LaEUANILRcP1"
    baidu_secret_key = "dB4CV92xpx4XjIIlgnmiDV5a0Nx1L9af"
    bidu_ai_host = 'https://aip.baidubce.com/oauth/2.0/token?' \
                   'grant_type=client_credentials&client_id=%s&client_secret=%s' \
                   % (baidu_api_key, baidu_secret_key)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    access_token = json.loads(http.request(bidu_ai_host, 'POST', None, headers)[1].decode('utf-8'))['access_token']
    return access_token






# 百度植物图像识别
def baidu_image_classify_plant(image=None, baike_num=0):
    baidu_access_token = get_baidu_access_token()
    baidu_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant"
    url = url + ("?access_token=%s" % baidu_access_token)
    headers = baidu_headers
    error = None
    if image is None:
        error = 'Image required.'
    else:
        # 二进制方式打开图片文件
        try:
            f = open(image, 'rb')
        except FileNotFoundError:
            error = 'Invalid image location.'

    if error is not None:
        abort(404, error)

    img = base64.b64encode(f.read())
    body = {
        "image": img,
        "baike_num": baike_num
    }
    body = urllib.parse.urlencode(body).encode(encoding='utf-8')

    response, content = http.request(url, 'POST', body, headers)
    content = content.decode('utf-8')

    return response, content


def aliyun_plant_recognize(image=None):
    url = "https://plantgw.nongbangzhu.cn/plant/recognize2"
    headers = {
        "Host": "plantgw.nongbangzhu.cn",
        "X-Ca-Request-Mode": "debug",
        "X-Ca-Key": "25085772",
        "X-Ca-Stage": "RELEASE",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Authorization": "APPCODE 5b3a64c4816340e1af255e6e5a7f27e5"
    }
    error = None
    if image is None:
        error = 'Image required.'
    else:
        try:
            f = open(image, 'rb')
        except FileNotFoundError:
            error = 'Invalid image location.'

    if error is not None:
        abort(404, error)

    img = base64.b64encode(f.read())
    body = {
        "img_base64": img
    }
    body = urllib.parse.urlencode(body).encode(encoding='utf-8')

    response, content= http.request(url, 'POST', body, headers)
    content = content.decode('utf-8')
    content = json.loads(content)

    return response, content


# batch: 支持批量操作（最大为10）
def alicloud_geocode(address=None, batch="false", city=None, output="JSON"):
    host = 'http://geo.market.alicloudapi.com'
    path = '/v3/geocode/geo'
    method = 'GET'
    appcode = "5b3a64c4816340e1af255e6e5a7f27e5"
    error = None

    if address is None:
        error = 'Address required.'

    if error is not None:
        abort(404, error)

    query = 'address=%s&batch=%s&output=%s' % (address, batch, output)
    query = append_url_param(query, 'city', city)
    bodys = {}
    headers = {
        'Authorization': 'APPCODE '+appcode
    }
    url = host + path + '?' + query
    response, content = http.request(url, method, bodys, headers)
    content = json.loads(content.decode('utf-8'))

    return response, content

