import hashlib
from jkj_project.settings import BASE_DIR
import os
import codecs

def md(text):
    md = hashlib.md5()
    md.update(text.encode('utf-8'))
    return md.hexdigest()

# 读取文件
def file2obj(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        return eval(f.read())

provinces = file2obj(os.path.join(BASE_DIR, 'assets/province.json'))  #list  [{name, id}]
cities = file2obj(os.path.join(BASE_DIR, 'assets/city.json'))
areas = file2obj(os.path.join(BASE_DIR, 'assets/area.json'))

def get_cities_by_id(provinceid):
    return cities[provinceid]

def get_areas_by_id(cityid):
    return areas[cityid]

def get_province_by_id(provinceid):
    for province in provinces:
        if province['id'] == str(provinceid):
            return province['name']

def get_city_by_id(provinceid, cityid):
    for city in cities[str(provinceid)]:
        if city['id'] == str(cityid):
            return city['name']

def get_area_by_id(cityid, areaid):
    for area in areas[str(cityid)]:
        if area['id'] == str(areaid):
            return area['name']
