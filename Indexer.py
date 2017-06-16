#!/usr/bin/env python
# -*- coding: gbk -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import sys
from collections import defaultdict
import Utils

class Indexer(object):
    def __init__(self, dataset):
        self.dataset = dataset

    def build_indexer(self):
        pass

    def search(self, word):
        pass
    
class HashIndexer(Indexer):
    def __init__(self, dataset):
        super(HashIndexer, self).__init__(dataset)
        self.char_indexer = defaultdict(set) 

    def build_indexer(self):
        for word in self.dataset.word2id:
            for char in Utils.get_chars(word): 
                self.char_indexer[char].add(word)

        for char in self.char_indexer:
            self.char_indexer[char] = sorted(list(self.char_indexer[char])) 
    
    def __get_start_char(self, word):
        chars = Utils.get_chars(word) 
        if len(chars) == 0:
            return None
        return chars[0]

    def search(self, word):
        char = self.__get_start_char(word) 
        word_list = self.char_indexer[char]
        if word_list == set():
            return False, None
        l = 0
        r = len(word_list) - 1 

        while l < r:
            m = (l + r) / 2
            _word = word_list[m]
            if word == _word:
                return True, word 
            elif  word < _word:
                r = m - 1
            else:
                l = m + 1
        
        if l < len(word_list) and word_list[l].startswith(word) :
            return True, None
        else:
            return False, None

class TrieIndexer(Indexer):
    def __init__(self, dataset):
        super(TrieIndexer, self).__init__(dataset)
        self.trie_indexer = defaultdict(dict) 
        self.END = "\0"

    def build_indexer(self):
        for word in self.dataset.word2id:
            self.add_word(word)

    def add_word(self, word):
        node = self.trie_indexer
        for char in Utils.get_chars(word): 
            node = node.setdefault(char, {})

        node[self.END] = None

    def search(self, word, is_exact = False):
        node = self.trie_indexer
        for char in Utils.get_chars(word):
            if char not in node:
                return False, None
            else:
                node = node.get(char)
        
        if is_exact == False:
            if self.END in node:
                return True, word 
            else:
                return True, None
        else:
            if self.END in node:
                return True, word 
            else:
                return False, None
        
