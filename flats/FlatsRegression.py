#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import print_function
import urllib2
import re
from bs4 import *
from time import sleep
#import sqlite3

doc = open('FlatsRegression.txt', 'a')
url = 'https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&foot_min=20&maxprice=25000000&minsu=1&object_type%5B0%5D=1&offer_type=flat&only_foot=2&region=1&room1=1&wp=1'

countDoc = open('counter.txt', 'a')
parseCount = 0

# conn = sqlite3.connect('Regression.sqlite')
# cur = conn.cursor()

def parsePage(url):
    try:
        page = urllib2.urlopen(url)
        countDoc.write('parsing url: ' + url + '\n')
    except urllib2.HTTPError, e:
        print('Error status:', e.code)

    return BeautifulSoup(page, "html.parser")

def GetInfo(page, doc):
    global parseCount
    catalog = page.findAll('div', {'class': 'offer-container--38nzf'})
    for item in catalog:
        itemlink = item.find('a', {'class': 'cardLink--3KbME'}).get('href')
        # sleep(10)
        itempage = urllib2.urlopen(itemlink)
        itemsoup = BeautifulSoup(itempage, "html.parser")

        parseCount += 1
        countDoc.write('Flat: ' + str(parseCount) + ', url: ' + itemlink + '\n')

        values = {}
        # itemId = itemsoup.find('h3', {'class': 'realtor-card__title'}).text.strip().replace('ID:', '')
        itemId = re.findall('\d+', itemlink)[0]
        values['itemId'] = itemId

        rooms = itemsoup.find('div', {'class': 'object_descr_title'})
        rooms = rooms.text if rooms else None
        rooms = re.findall('\d', rooms)[0] if rooms else '-'
        values['rooms'] = rooms

        metro = itemsoup.find('p', {'class': 'objects_item_metro_prg'})
        metro = metro.find('a').string[:-1] if metro else '-'
        values['metro'] = metro

        spantime = itemsoup.find('span', {'class': 'object_item_metro_comment'})
        spantime = spantime.contents[0].strip() if spantime else None
        timetometro = re.findall('(\d+)\s', spantime)[0] if spantime else '-'
        values['timeToMetro'] = timetometro

        price = itemsoup.find('div', {'class': 'object_descr_price'})
        price = price.contents[0] if price else None
        price = price.strip().replace(' ', '').replace(u'руб.', '') if price else '-'
        values['price'] = price

        table = itemsoup.find('table', {'class': 'object_descr_props flat sale'})
        if not table:
            continue

        features = [
            u'Этаж:', u'Тип дома:', u'Год постройки:', u'Общая площадь:',
            u'Жилая площадь:', u'Совмещенных санузлов:', u'Балкон:', u'Лифт:',
            u'Вид из окна:', u'Ремонт:'
        ]
        fields = [
            'floor', 'buildingType', 'builtAt', 'area',
            'netArea', 'bathrooms', 'balcony', 'elevator',
            'view', 'renovation',
            'itemId', 'rooms', 'metro', 'timeToMetro', 'price', 'floors'
        ]

        for row in table.findAll('tr'):
            if not row.find('td'):
                continue

            feature = row.find('th')
            if not feature: continue
            feature = feature.text

            if feature in features:
                text = row.find('td')
                if not text: continue
                text = text.text
                text = re.sub('\n', '', text, 0, flags = re.MULTILINE) if text else None
                text = re.sub('\s{2,}', '', text, 0, flags = re.MULTILINE) if text else None
                text = text.replace(u'м2', '').strip() if text else None
                text = text.replace(',', '.').strip() if text else None
                if not text: continue
                index = features.index(feature)

                field = fields[index]
                if field == 'floor':
                    floorsText = text.split('/')
                    values['floor'] = floorsText[0].strip()
                    values['floors'] = floorsText[1].strip() if floorsText[1] else '-'
                elif field == 'buildingType' and '.' in text:
                    values[field] = text.split('.')[1]
                else:
                    values[field] = text

        # check if all the fields are present, put a '-' if not
        valueFields = values.keys()
        for field in fields:
            if not field in valueFields:
                values[field] = '-'

        output = ', '.join([k + ':' + v for k, v in values.iteritems()]).encode('utf-8')
        doc.write(output + '\n')
        # print(output)

def GetNextUrl(root):
    nav = root.find('ul', {'class': 'list--35Suf'})
    if not nav:
        return None

    currPage = nav.find('li', {'class': 'list-item--active--2-sVo'} )
    nextPage = currPage.find_next_sibling('li').find('a').get('href')
    if not nextPage:
        return None

    return str(nextPage)

count = 0
nextPage = url
while nextPage:
    soup = parsePage(nextPage)
    itemsdata = GetInfo(soup, doc)
    nextPage = GetNextUrl(soup)
    count +=1
    print('Count', count)

doc.close()
countDoc.close()
