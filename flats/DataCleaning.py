#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from __future__ import print_function
import sqlite3

conn = sqlite3.connect('Regression2.sqlite')
cur = conn.cursor()

cur.execute('UPDATE Flats SET bathrooms = ? WHERE bathrooms isnull', (1,))
cur.execute('UPDATE Flats SET elevators = ? WHERE elevators isnull', (0,))
cur.execute('UPDATE Flats SET balcony = ? WHERE balcony isnull', (0,))
cur.execute('UPDATE Flats SET loggia = ? WHERE loggia isnull', (0,))

def StrToNum(query):
    cur.execute(query)
    elements = cur.fetchall()
    elements = filter(lambda x: x[0] != None, elements)
    elements = [(i+1, el[0]) for i, el in enumerate(elements)]
    return elements

query1 = 'SELECT DISTINCT view FROM Flats'
update1 = 'UPDATE Flats SET viewId = ? WHERE view = ?'
query2 = 'SELECT DISTINCT renovation FROM Flats'
update2 = 'UPDATE Flats SET renvId = ? WHERE renovation = ?'
query3 = 'SELECT DISTINCT buildingType FROM Flats'
update3 = 'UPDATE Flats SET bTypeId = ? WHERE buildingType = ?'
query4 = 'SELECT DISTINCT metro FROM Flats'
update4 = 'UPDATE Flats SET metroId = ? WHERE metro = ?'
queries = [(query1, update1), (query2, update2), (query3, update3), (query4, update4)]
for query, update in queries:
    for i, el in StrToNum(query):
        cur.execute(update, (i, el))
        print(i, el)
    print(query)
    print(update)
    print()

conn.commit()