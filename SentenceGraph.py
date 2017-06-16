#!/usr/bin/env python
# -*- coding: gbk -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import sys
import Utils
from collections import defaultdict
from DataSet import DataSet
from Indexer import HashIndexer
from Indexer import TrieIndexer

class Vertex():
    def __init__(self, word, s, e):
        self.word = word
        self.start = s
        self.end = e

class Edge():
    def __init__(self, sv, ev, weight):
        self.sv = sv
        self.ev = ev
        self.weight = weight

class SentenceGraph():
    def __init__(self, dictfile, indexer = "Trie"):
        self.dict = DataSet(dictfile) 
        print >>sys.stderr, "loading dict..."
        self.dict.load_dict()
        print >>sys.stderr, "load dict ok, word total num is %s." % self.dict.word_total_num 
        if indexer == "Hash":
            self.indexer = HashIndexer(self.dict) 
        elif indexer == "Trie":
            self.indexer = TrieIndexer(self.dict) 
        else:
            print >>sys.stderr, "Indexer type error: Trie/Hash is supported!"
            raise Exception("IndexerTypeError")
        self.indexer.build_indexer()

        self.vertexs = []
        self.edges = defaultdict(list)
        self.beginv = Vertex(None, -1, -1)
        self.endv = Vertex(None, -1, -1)

    def reinit(self):
        self.vertexs = []
        self.edges = defaultdict(list)
        
    def generate_vertexs(self, sentence):
        chars = Utils.get_chars(sentence)
        self.len_sentence = len(chars)
        if self.len_sentence == 0:
            print>>sys.stderr, "Warning:Input is empty!"
            raise Exception("Input is empty")
        self.vertexs.append(self.beginv) 
        self.vertexs.append(self.endv) 
        for idx in range(0, self.len_sentence):
            idy = idx + 1
            found_word = False
            while idy <= self.len_sentence: 
                word = "".join(chars[idx:idy])
                ret, se_word = self.indexer.search(word)
                if ret == False:
                    break
                else:
                    if se_word != None:
                        self.vertexs.append(Vertex(se_word, idx, idy))
                        found_word = True
                idy += 1
    
            if not found_word:
                self.vertexs.append(Vertex(chars[idx], idx, idx + 1))

    def add_edge(self, v1, v2):
        weight = self.dict.seek_p(v1.word, v2.word)
        self.edges[v1].append(Edge(v1, v2, weight))

    def build_graph(self):
        starts_vertexs = defaultdict(set)
        for v in self.vertexs:
            starts_vertexs[v.start].add(v)
        
        for v in self.vertexs:
            if v.word == None:
                continue
            end = v.end
            for v2 in starts_vertexs[end]:
                self.add_edge(v, v2)
            if v.start == 0:
                self.add_edge(self.beginv, v)
            if v.end == self.len_sentence:
                self.add_edge(v, self.endv)

    def find_shortest_path(self):
        S = set()
        dis = dict((k, float("inf")) for k in self.vertexs)
        dis[self.beginv] = 0 
        len_dis = len(dis.keys())
        v_prev = {}
        def seek_minv():
            _minv = None
            for v in dis:
                if v in S: 
                    continue
                if _minv == None:
                    _minv = v
                else:
                    if dis[_minv] > dis[v]: 
                        _minv = v

            return _minv
        
        def update_shortest_path(_minv):
            for edge in self.edges[_minv]:
                if edge.weight + dis[_minv] < dis[edge.ev]:
                    dis[edge.ev] =  edge.weight + dis[_minv]
                    v_prev[edge.ev] = _minv

        def format_shortest_path(): 
            path = []
            v = self.endv
            while v != self.beginv:
                path.append(v)
                v = v_prev[v]

            path.append(v)
            return reversed(path[1:-1])

        while True:
            minv = seek_minv() 
            if minv == self.endv:
                break
            S.add(minv)
            update_shortest_path(minv)
        
        return format_shortest_path() 
