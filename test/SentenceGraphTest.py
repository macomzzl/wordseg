#!/usr/bin/env python
# -*- coding: gbk -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import sys
import unittest
from unittest import TestCase
sys.path.append("..")
sys.path.append(".")
from DataSet import DataSet
from Indexer import HashIndexer
from Indexer import TrieIndexer
from SentenceGraph import SentenceGraph
import pdb

class SentenceGraphTest(TestCase):
    def setUp(self):
        self.sg = SentenceGraph("./data/199801.txt.tmp")

    def test_generate_vertexs(self):
        self.sg.generate_vertexs("你好吗希望11")
        print "_".join([str(v.word) for v in self.sg.vertexs])
    
    def test_build_graph(self):
        self.sg.generate_vertexs("你好吗希望11迈向")
        self.sg.build_graph()
        import copy
        def dfs(n, d):
            if n == self.sg.endv:
                print "_".join(d)
                return
            d.append(str(n.word))
            for e in self.sg.edges[n]: 
                dfs(e.ev, copy.deepcopy(d))

        #print "_".join([ e.ev.word for e in self.sg.edges[self.sg.beginv]])
        dfs(self.sg.beginv, [])
    

    def test_shortest_path(self):
        self.sg.generate_vertexs("怀揣这如泣如诉的呵护，")
        self.sg.build_graph()
        for v in self.sg.vertexs:
            print "v", v.word
            for e in self.sg.edges[v]:
                print "e", e.sv.word, e.ev.word, e.weight 
        shortest_path = self.sg.find_shortest_path()
        print "shortest path", '_'.join([str(v.word) for v in shortest_path])

if __name__ == '__main__':  
    unittest.main()

