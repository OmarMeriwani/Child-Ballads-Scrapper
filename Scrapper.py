import numpy as np
import pandas as pd
import re
import sys
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.request import urlopen
import nltk
import requests
import urllib.parse
from html.parser import HTMLParser
import csv

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    # print(html)
    s.feed(html)
    return s.get_data()

def between(cur, end):
    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                yield text
        cur = cur.next_element


'''Defining URLS'''
# url1 = urllib.parse.quote(url1)
'''Reading URLs' content'''
def getNextInside(num, node):
    for i in range(0, num):
        print('NEXT ', i, ' FOR ', node)
        node = node.next_element
    return node

def getNextAdjacent(num,node,type):
    result = ''
    CurrentName = re.sub('[\n]', '', strip_tags(str(node)))
    print(CurrentName)
    prevText = ''
    beginning = True
    NextName = None
    node2 = None
    for i in range(0, num):
        if node != None:
            if re.sub('[\n]', '', strip_tags(str(node))) == "الموسوعة":
                break
            node2 = node.find_previous('h1')
            if beginning == True:
                beginning = False
            else:
                NextName = re.sub('[\n]', '', strip_tags(str(node2)))

            if (CurrentName != NextName and NextName != 'None' and NextName != None):
                #print('Names:', CurrentName, NextName)
                break
            node = node.find_next(type)
        result = result + prevText
        prevText = re.sub('[\n]', '', strip_tags(str(node)))
    return result

def ArchivePage(url1):
    Page1 = urlopen(url=url1, data=None)
    Page1 = BeautifulSoup(Page1, features="html5lib")

    hdrs1 = Page1.find_all(lambda tag: tag and tag.name.startswith("h1"))
    hdrs2 = Page1.find_all(lambda tag: tag and tag.name.startswith("h2"))
    hdrs3 = Page1.find_all(lambda tag: tag and tag.name.startswith("h3"))

    texts = Page1.find_all(lambda tag: tag and tag.name.startswith("pre"))
    # print(elements)
    headers = []
    headersAll = []
    paragraphs = []
    for h in hdrs1:
        print(strip_tags(str(h)))
    #print()
    t = ''
    for tt in texts:
        t += strip_tags(str(tt))
    h = strip_tags(str(hdrs1[0]))
    return h,t
#links  = getAllLinks()

df = pd.DataFrame(columns=['Number','Title','Text'])
seq = 0
#with open(r'C:\Users\Omar\Documents\GitHub\Child Ballads Scrapper\Child.csv','w', encoding='utf-8') as csvFile:
    #writer = csv.writer(csvFile,  delimiter='\t')
    #csvFile.write('Number,Title,Text')
'''
for i in range(100,305):
    try:
        istr = ''
        if len(str(i)) == 1:
            istr = '00' + str(i)
        elif len(str(i)) == 2:
            istr = '0' + str(i)
        else:
            istr = str(i)
        link = 'https://www.sacred-texts.com/neu/eng/child/ch' + istr + '.htm'
        header, text = ArchivePage(link)
        row = ','.join([istr,header,text])
        df.loc[seq] = [istr,header,text]
        seq += 1
    except  Exception as ex:
        print(ex)
        break
    #    csvFile.write(row)
    #csvFile.close()
    '''

def ArchivePage2(url1,istr):
    Page1 = urlopen(url=url1, data=None)
    Page1 = BeautifulSoup(Page1, features="html5lib")

    body = Page1.find_all(lambda tag: tag and tag.name.startswith("body"))

    bb = ''
    for b in body:
        bb = (strip_tags(str(b)))
    bb = bb.split('\n')
    title = bb[1]
    desc = ''
    author = ''
    earliest_date = ''
    keywords = ''
    found_in = ''
    for line in bb:
        if line.startswith('DESCRIPTION:')== True:
            desc = line[13:]
        if line.startswith('AUTHOR:')== True:
            author = line[7:]
        if line.startswith('EARLIEST DATE:')== True:
            earliest_date = line[15:]
        if line.startswith('KEYWORDS:')== True:
            keywords = line[10:]
        if line.startswith('FOUND IN:')== True:
            found_in = line[10:]
        '''
        bb = bb[0:bb.find('REFERENCES ')]
        desc = bb.split('\n')[2][13:]
        author = bb.split('\n')[3][7:]
        earliest_date = bb.split('\n')[4][15:]
        keywords = bb.split('\n')[5][10:]
        found_in = bb.split('\n')[6][10:]'''
    print('title: ',title,'\n','desc: ',desc,'\n','author: ',author,'\n','earliest_date: ',earliest_date,'\n','keywords: ',keywords,'\n','found_in: ',found_in )
    return [istr,title,desc,author,earliest_date,keywords,found_in]

df = pd.DataFrame(columns=['number','title','desc','author','earliest_date','keywords','found_in'])
for i in range(1,306):
    try:
        istr = ''
        if len(str(i)) == 1:
            istr = '00' + str(i)
        elif len(str(i)) == 2:
            istr = '0' + str(i)
        else:
            istr = str(i)
        link = 'https://www.fresnostate.edu/folklore/ballads/C' + istr + '.html'
        body = ArchivePage2(link,istr)
        row = ','.join(body)
        df.loc[seq] = body
        seq += 1
    except  Exception as ex:
        print(ex)
        break
    #    csvFile.write(row)
    #csvFile.close()
df.to_excel(r'C:\Users\Omar\Documents\GitHub\Child Ballads Scrapper\Child_info.xlsx')