#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import print_function
import sqlite3
import re

data = open('room4.txt', 'r')
items = data.readlines()

conn = sqlite3.connect('Regression.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Flats (
    itemId VARCHAR(20) PRIMARY KEY,
    builtAt INTEGER,
    bathrooms INTEGER,
    netArea FLOAT,
    metro TEXT,
    floor INTEGER,
    area FLOAT,
    elevator VARCHAR(60),
    elevators INTEGER,
    timeToMetro INTEGER,
    floors INTEGER,
    rooms INTEGER,
    view VARCHAR(60),
    buildingType VARCHAR(60),
    renovation VARCHAR(60),
    allbalcony VARCHAR(60),
    balcony INTEGER,
    loggia INTEGER,
    price INTEGER)
''')

count = 0
for item in items:
    features = item.replace('\n', '').split(', ')
    features = map(lambda x: x.split(':')[1], features)
    features = map(lambda x: None if x in ['-', 'нет', '–', 'отсутствует'] else x, features)
    features[0:1] = map(lambda x: x.decode('utf-8') if x else None, features[0:1])
    features[1:3] = map(lambda x: int(x) if x else None, features[1:3])
    features[3:4] = map(lambda x: float(x) if x else None, features[3:4])
    features[4:5] = map(lambda x: x.decode('utf-8') if x else None, features[4:5])
    features[5:7] = map(lambda x: int(x) if x else None, features[5:7])
    features[7:8] = map(lambda x: float(x) if x else None, features[7:8])
    features[8:9] = map(lambda x: x.decode('utf-8') if x else None, features[8:9])
    features[9:12] = map(lambda x: int(x) if x else None, features[9:12])
    features[12:] = map(lambda x: x.decode('utf-8') if x else None, features[12:])
    
    cur.execute('''INSERT OR IGNORE INTO Flats (itemId, builtAt, bathrooms,
    netArea, metro, floor, price, area, elevator, timeToMetro,
    floors, rooms, view, buildingType, renovation, allbalcony)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(features))

cur.execute('SELECT elevator, itemId FROM Flats')
elevators = cur.fetchall()

elevators = map(lambda x: (re.findall('\d+', x[0]), x[1]) if x[0] else (None, x[1]), elevators)
tointFunc = lambda z: map(lambda y: int(y.encode('utf-8')) if y else None, z)
elevators = [(tointFunc(x[0]), x[1]) if x[0] else (None, x[1]) for x in elevators]
sumFunc = lambda z: reduce(lambda x, y: x + y, z) if z else None 
elevators = [(sumFunc(x[0]), x[1]) for x in elevators]
for el in elevators:
    cur.execute('UPDATE Flats SET elevators = ? WHERE itemId = ?', (el[0], el[1]))

cur.execute('UPDATE Flats SET buildingType = null WHERE buildingType = ?', (u'вторичка',))

cur.execute('SELECT allbalcony, itemId FROM Flats')
balconies = cur.fetchall()

def defineBalc(x):
# 1 - балкон, 2 - лоджия
    if not x:
        return [None, None]
    if '+' in x:
        x = x.split('+')
        x = map(lambda y: int(re.findall('\d', y)[0]), x)
        return x
    else:
        x = x.split(' ')
        x[0] = int(x[0])
        if u'балк' in x[1]:
            return [x[0], None]
        else:
            return [None, x[0]]

for el in balconies:
    el = defineBalc(el[0]) + [el[1]]
    cur.execute('UPDATE Flats SET balcony = ? WHERE itemId = ?', (el[0], el[2]))
    cur.execute('UPDATE Flats SET loggia = ? WHERE itemId = ?', (el[1], el[2]))

conn.commit()