#!home/common/scripts/python/bin/python3
#----------------------------------handy ruler---------------------------------#

import os,os.path
import xml.etree.ElementTree as ET
import operator as OPR
from functools import reduce


DATADIR = '/usr/local/DATASET/datasets'

def filename(dset,ftype,*parts):
    return os.path.join(DATADIR,dset,'data',ftype,
        '.'.join((ftype,*parts)))

def sum_dicts(dicts,f,Id):
    """
    Tool for combining dictionaries - 
    
    dicts - a list of dictionaries
    f     - a binary function
    Id    - the identity element under f
    
    returns the dictionary obtained by {x:f(d1[x],d2[x],d3[x],...)}
    for dictionaries d1,d2,... 
    """

    def reducer(acc,dic):
        for key,value in dic.items():
            acc[key] = f(acc.get(key,Id),value)
        return acc
    return reduce(reducer, dicts, {})

def add_lists(*lists):
        return list(map(OPR.add, *lists))


class Garage:
    DATASETS = {'S':'18', 'E':'20'}
    GARAGES = {
        'SUTTON':['A','06','S'],
        'PUTNEY':['AF','07','S'],
        'MERTON':['AL','05','S'],
        'BEXLEYHEATH':['BX','01','S'],
        'CROYDON':['C','16','S'],
        'ORPINGTON':['MB','15','S'],
        'MORDENWHARF':['MG','18','S'],
        'NORTHUMBERLANDPARK':['NP','14','E'],
        'NEWCROSS':['NX','02','S'],
        'WATERSIDEWAY':['PL','10','S'],
        'PECKHAM':['PM','03','S'],
        'CAMBERWELL':['Q','04','S'],
        'WATERLOO':['RA','09','S'],
        'RIVERROAD':['RR','30','E'],
        'SILVERTOWN':['SI','20','E'],
        'STOCKWELL':['SW','08','S']}


class Rota(Garage):
    def __init__(self,version,date):
        self.version = version
        self.draft,self.garage = self._get_garage()
        self.date = self._parse_date(date)
        self._revdate = ''.join((
          self.date['year'],self.date['mth'],self.date['day'],'7D'))
        self.dataset = Garage.DATASETS[Garage.GARAGES[self.garage][2]]
        self.filename = filename(
          self.dataset,'rosterperiod',self.version,self._revdate)
        self.parse = ET.parse(self.filename).getroot()
        self.desc = self.parse.find(".//rosterDescription").text.split(',')[0]
        self.sections = [
            Section(
              filename(
                self.dataset,
                'rostersection',
                self.version,
                self._revdate,
                sec.text))
            for sec in self.parse.findall(".//sectionIdRef")]
        #self.books = {sec.Id:sec.books for sec in self.sections}

    def _get_garage(self):
        if '-' in self.version:
            return self.version.split('-')
        else:
            return ('FINAL', self.version)

    def _parse_date(self,date):
        date = date.replace('/','')
        day = date[0:2]
        mth = date[2:4]
        year = date[4:]
        return {'day':day, 'mth':mth, 'year':year}

    def by_book(self):
        return sum_dicts([sec.by_book() for sec in self.sections],add_lists,[0]*7)

    def requirement(self):
        return reduce(add_lists, [sec.requirement() for sec in self.sections], [0]*7)       


class Section(Garage):
    def __init__(self,filename):
        self.root = ET.parse(filename).getroot()
        self.desc = self.root.find(".//sectionDescription").text.strip()
        self.name = self.root.find(".//sectionName").text.strip()
        self.Id = self.root.find(".//primaryGroup").text.strip()
        self.books = list(set([book.text.strip() for book in self.root.findall(".//shiftBook")]))
        
    def by_book(self):
        dayitems = {
          book:self.root.findall('.//dayItem[shiftBook="%s"]/dayItemId' % book)
          for book in self.books}

        return {
          book:[sum(
            1 for day in dayitems[book]
            if (int(day.text)-(i+1)) % 7 == 0)
          for i in range(7)] for book in self.books}

    def requirement(self):
        dayitems = [
          day.text.strip()
          for day in self.root.findall(".//dayItem[dayItemType='2']/dayItemId") ]
 
        return [
          sum(
            1 for day in dayitems
            if (int(day)-(i+1)) % 7 == 0)
          for i in range(7)]
