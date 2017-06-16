#!/usr/bin/env python
# -*- coding: gbk -*-
# Last modified: 

"""docstring
"""

import sys

def get_chars(word):
    return map(lambda x:x.encode("gbk", "ignore"), word.decode("gbk", "ingore"))


