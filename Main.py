#!/usr/bin/env python
# -*- coding: gbk -*-
# Last modified: 

"""docstring
"""

import sys
from WordSeg import WordSeg
import pdb

def load_test_data(f):
    sentences = []
    with open(f) as fd:
        for line_num, line in enumerate(fd):
            ll = line.strip("\n\r ").split("  ")
            
            one = []
            for it in ll:
                if it.startswith('[') and len(it) > 1:
                    it = it[1:]
                elif it.find("]n") != -1:
                    it = it.split("]")[0]
                it = it.split("/")
                if len(it) < 2:
                    continue
                one.append(it[0])
                if it[0] in ("。", "，", "？", "！", "……", "；"):
                    sentences.append([one, "".join(one)])
                    one = []

            if one != []:
                sentences.append([one, "".join(one)])
    
    return [s[1] for s in sentences], [s[0] for s in sentences]


def calc_precision_recall_F(test, gold):
    test_segs_num = 0
    gold_segs_num = 0
    correct_num = 0
    
    def gbk_len(s):
        return len(s.decode("gbk", "ignore"))
    
    fd_eval = open('eval.html', "w")
    fd_eval.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=gbk" /><style type="text/css">span{margin-right:20px;}</style></head><body>\n')
    line_num = 0 
    for t, g in zip(test, gold):
        cmp = 0
        idt = -1 
        idg = -1 
        len_t = len(t)
        test_segs_num += len_t
        gold_segs_num += len(g)
        line_num += 1
        fd_eval.write("<span style=\"color:blue\">" + str(line_num) + ".</span>")
        while idt < len_t:
            if cmp > 0:
                idg += 1
                cmp -= gbk_len(g[idg])
            elif cmp < 0:
                idt += 1
                if idt == len_t:
                    break
                cmp += gbk_len(t[idt])
                fd_eval.write("<span style=\"color:red\">" + t[idt] + "</span>");
            else:
                idt += 1
                idg += 1
                if idt == len_t:
                    break
                cmp += gbk_len(t[idt]) - gbk_len(g[idg])
                if cmp == 0:
                    correct_num += 1
                    fd_eval.write("<span>" + t[idt] + "</span>");
                else:
                    fd_eval.write("<span style=\"color:red\">" + t[idt] + "</span>");

        fd_eval.write("<br>") 

    fd_eval.write("</body></html>") 
    precise = correct_num * 1.0 / test_segs_num 
    recall = correct_num * 1.0 / gold_segs_num 
    F = 2 * precise * recall / (precise + recall)
    return precise, recall, F

dict_file = "data/199801_train.txt"
test_file = "data/199801_test.txt"

ws = WordSeg(dict_file)
test_X, test_Y = load_test_data(test_file)

predicted = []
for sent in test_X:
    sent, segs =  ws.seg_word(sent)
    predicted.append([sent, segs])

predicted_Y = [it[1].split("\1") for it in predicted]
ret = calc_precision_recall_F(predicted_Y, test_Y)
print "precise:", ret[0]
print "recall:", ret[1]
print "F:", ret[2]


