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
        print self.DataSet.seek_p("����", "ϣ��11")
        self.assertEqual(self.DataSet.word2num[self.DataSet.word2id.get("����")], 2)
    
    def test_indexer(self):
        self.assertTrue(self.trieindexer.search("ϣ��1")[0])
        self.assertTrue(self.trieindexer.search("ϣ��")[0])
        self.assertFalse(self.trieindexer.search("��")[0])
        self.assertTrue(self.hashindexer.search("ϣ��11")[0])
        self.assertTrue(self.hashindexer.search("ϣ��")[0])
        self.assertFalse(self.hashindexer.search("��")[0])


if __name__ == '__main__':  
    unittest.main()

