#coding=utf-8

import re
import logging
def splitJson(world,jsonTemp):
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    logging.debug("debug")

    findSplitWord = re.findall(world, jsonTemp)
    if len(findSplitWord)!=0:
        a=jsonTemp.split(world)

        return "{ \""+world+a[1]
    else:
         logging.info('Not find the world!')
         return 0