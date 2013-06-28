import optparse
import re
import sys
import time
import math
from cgi import escape
from traceback import format_exc
import codecs
import os
from nltk.corpus import stopwords
from stemming.porter2 import stem

def filter (data):
    final_data = ""
    #filter data
    data = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', data)
    filter_data = ""
    # remove stopword
    important_words=[]
    for word in data.split(" "):
      if word not in stopwords.words("english"):
        filter_data = filter_data + word + " "
    # stemming data
    for world in filter_data.split(" "):
        t = stem(world)
        final_data = final_data + t + " "
    return final_data

