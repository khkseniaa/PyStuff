from __future__ import print_function
import urllib2
import re
from bs4 import *

# file = open('flats.txt', 'r')
# itemsoup = BeautifulSoup(file, "html.parser")
# active = itemsoup.find('li', {'class': 'active'})
# nextPage = active.find_next_sibling('li').find('a').get('href')
# print(nextPage)

datasets = [1, 2, 3, 4]
x = [0]*len(datasets)
print(x)