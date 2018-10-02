# python3.6
# coding: utf-8

import os
import io

available_tags = [x[0:-4] for x in os.listdir('info/')]

available_tags.sort()

for i in range(len(available_tags)):
    available_tags[i] =str(i+1) +' '+ available_tags[i]

def content(tag):
    if tag.isdigit():
        tag = available_tags[int(tag) - 1]
    return io.open('info/' + tag + '.txt', 'r', encoding='utf-8').read()
