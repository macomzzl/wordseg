#!/usr/bin/env python
# -*- coding: gbk -*-
# Last modified: 

"""docstring
"""
import sys
from collections import defaultdict
import math

class DataSet():
    def __init__(self, file):
        self.currid = 0
        self.word2num = defaultdict(int) 
        self.twoword2num = defaultdict(int) 
        self.p = defaultdict(dict) 
        self.word2id = {}
        self.file = file 
        self.word_total_num = 0
    
    def __yield_lines(self, dict):
        with open(dict) as fd:
            for line_num, line in enumerate(fd):
                ll = line.strip("\n\r ").split("  ")
                
                fds = []
                for it in ll:
                    if it.startswith('[') and len(it) > 1:
                        it = it[1:]
                    elif it.find("]n") != -1:
                        it = it.split("]")[0]
                    it = it.split("/")
                    if len(it) < 2:
                        continue
                    fds.append(it)
                yield fds

    def load_dict(self):
        for fds in self.__yield_lines(self.file): 
            pre_word_id = None
            for it in fds:
                w = it[0]
                normial = it[1]

                if w not in self.word2id:
                    self.word2id[w] = self.currid 
                    self.currid += 1

                self.word2num[self.word2id[w]] += 1
                self.twoword2num[(pre_word_id, self.word2id[w])] += 1

                pre_word_id = self.word2id[w] 
            
            self.twoword2num[(pre_word_id, None)] += 1
        
        self.word_total_num = len(self.word2id.keys())
        #self.compute_p()

    def compute_p(self):
        for idx in range(self.word_total_num):
            for idy in range(self.word_total_num):
                if self.twoword2num[(idx, idy)] == 0:
                    continue
                _p = - math.log((self.twoword2num[(idx, idy)] + 1) *1.0 / (self.word2num[idx] + self.word_total_num), 2) 
                self.p[idx][idy] = _p

    def seek_p(self, w1, w2):
        idw1 = self.word2id.get(w1, None)
        idw2 = self.word2id.get(w2, None)

        if idw1 == None or idw2 == None:
            return 99999  ##没在词典中出现的连续两个词，则赋值为无穷大 
        if idw1 not in self.p or idw2 not in self.p[idw1]:
           return -math.log((self.twoword2num[(idw1, idw2)] + 1) *1.0 / (self.word2num[idw1] + self.word_total_num), 2) 
        else :
            return self.p[idw1][idw2]

