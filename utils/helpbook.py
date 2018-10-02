# python3.6
# coding: utf-8

import os
import io

available_tags = [x[0:-4] for x in os.listdir('info/')]

#available_tags.sort()

def content(tag):
    return io.open('info/' + tag + '.txt', 'r', encoding='utf-8').read()
