# python3.6
# coding: utf-8

import os
import io

available_tags = [x[0:-4] for x in os.listdir('info/')]

available_tags.sort()

available_tags_dig_list = list()

for i in range(len(available_tags)):
    lst_apnd = str(i+1) + available_tags[i]
    available_tags_dig_list.append(lst_apnd)

def content(tag):
    if tag.isdigit():
        tag = available_tags[int(tag)-1]
    return io.open('info/' + tag + '.txt', 'r', encoding='utf-8').read()
