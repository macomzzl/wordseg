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

class DataSetAndIndexerTest(TestCase):
    def setUp(self):
        self.DataSet = DataSet("./data/199801.txt.tmp") 
        self.DataSet.load_dict()
        self.hashindexer = HashIndexer(self.DataSet)
        self.hashindexer.build_indexer()
        self.trieindexer = TrieIndexer(self.DataSet)
        self.trieindexer.build_indexer()
    
    def test_load_dict(self):
        print self.DataSet.seek_p("充满", "希望11")
        self.assertEqual(self.DataSet.word2num[self.DataSet.word2id.get("充满")], 2)
    
    def test_indexer(self):
        self.assertTrue(self.trieindexer.search("希望1")[0])
        self.assertTrue(self.trieindexer.search("希望")[0])
        self.assertFalse(self.trieindexer.search("望")[0])
        self.assertTrue(self.hashindexer.search("希望11")[0])
        self.assertTrue(self.hashindexer.search("希望")[0])
        self.assertFalse(self.hashindexer.search("望")[0])


if __name__ == '__main__':  
    unittest.main()

