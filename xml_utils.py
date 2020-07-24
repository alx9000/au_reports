#!/home/common/scripts/python/bin/python3
#----------------------------------handy ruler---------------------------------#

import xml.etree.ElementTree as ET
import os,os.path
from functools import reduce


DATADIR = '/usr/local/DATASET/datasets'
ns = {'mz':'http://www.mentz.de/LBSLScheduleInterface/1.0',
      'xsi':'http://www.w3.org/2001/XMLSchema-instance'}

class xmlNamespace:
    def __init__(self,**kwargs):
        self.namespaces = {}
        for name,uri in kwargs.items():
            self.register(name,uri)
    
    def register(self,name,uri):
        self.namespaces[name] = '{' + uri + '}'

    def __call__(self,path):
        return path.format_map(self.namespaces)


class caesarFile:
    def __init__(self,file):
        self.root = ET.parse(file).getroot()
        self.mileage = {}
        self.set_mileage()

    def set_mileage(self):
        _livemiles = self.root.findall(".//mz:ServiceMileage", ns)
        _deadmiles = self.root.findall(".//mz:NonServiceMileage", ns)
        self.mileage['live'] = sum(
            float(live.text) for live in _livemiles)
        self.mileage['dead'] = sum(
            float(dead.text) for dead in _deadmiles)

    def sortnodes(self,nodes):
        self[:] = sorted(
            self, key = order(nodes))

    def order(nodelist):
        def nodesorter(item):
            return nodelist[item]
        return nodesorter

# Our key is a function which takes a node and returns that node's position.
# In essence we curry order(node_dict,node) on node_dict - 
# where node_dict gives our desired node order:
# nodelist = {'NODE1':0, 'NODE2':1, ... }

