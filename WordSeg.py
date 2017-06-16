#!/usr/bin/env python
# -*- coding: gbk -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import sys
import Utils
import traceback
from SentenceGraph import  SentenceGraph

class WordSeg:
    def __init__(self, dictfile):
        try:
            self.graph = SentenceGraph(dictfile)
        except Exception, e:
            traceback.print_exc()
            sys.exit(-1)

    def seg_word(self, sentence):
        self.graph.reinit()

        try:
            self.graph.generate_vertexs(sentence)
        except:
            return None 

        self.graph.build_graph()
        
        vs =  self.graph.find_shortest_path()
        segs = [v.word for v in vs]
        return sentence, "\1".join(segs)


