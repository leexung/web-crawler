import urllib2
import optparse
import re
import sys
import time
import math
from cgi import escape
from traceback import format_exc
import codecs
import os
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import cookielib
import os, cookielib, urllib
import Cookie
import MySQLdb
import storedata

def run(start,end):
    for x in range (start,end):
        try:
            print "crawl debian ", x
            crawler(x)
        except:
            print "error crawl debian",x

def update(bugid):
    print(bugid)

def crawler(bugid):
    try:
        btstype = "debian"
        table_database = "bugdata"
        author = ""
        owner = ""
        severity ="normal"
        status = "open"
        summary = ""
        comtid = ""
        sfeid    = ""
        symid = ""
        plmid = "linux"
        relbug = ""
        updated = 0
        created = 0
        resolved = 0
        keyword = ""
        lastbugidx =0
        lastbugid = 0
        assigned =""
        bugid = bugid
        database = "thesis"
        url = "http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=%d" %(bugid)
        page =  urllib.urlopen(url)
        data = page.read().decode("utf-8")
        soup = BeautifulSoup(data)
        #get summary
        summary = soup.find("title").text.strip()

        #get pkginfo
        info = soup.find("div",{"class":"pkginfo"})
        packet = info.find("a").text.strip()

        # get buginfo
        buginfo = soup.find("div",{"class":"buginfo"})
        p_data = []
        p_data = buginfo.findAll("p")
        reporter = p_data[0]
        author = reporter.find("a").text.strip()
        """
        date_time = p_data[1].text.strip()
        date = []
        date = date_time.split(" ")

        mon = ""
        if str(date[4]) == "Jan":
            mon = "01"
        elif str(date[4]) == "Feb":
            mon = "02"
        elif str(date[4]) == "Mar":
            mon = "03"
        elif str(date[4]) == "Apr":
            mon = "04"
        elif str(date[4]) == "May":
            mon = "05"
        elif str(date[4]) == "Jun":
            mon = "06"
        elif str(date[4]) == "Jul":
            mon = "07"
        elif str(date[4]) == "Aug":
            mon = "08"
        elif str(date[4]) == "Sep":
            mon = "09"
        elif str(date[4]) == "Oct":
            mon = "10"
        elif str(date[4]) == "Nov":
            mon = "11"
        elif str(date[4]) == "Dec":
            mon = "12"
        created = "%s%s%s"%(date[5],mon,date[3])
        """
        created = 0
        severity = p_data[2].text.strip()
        affect = severity

        unkown = p_data[3]
        version = p_data[4].text.strip()

        done = p_data[5].text.strip()

        description = p_data[6].text.strip()


        ### mess
        mess = []
        mess = soup.findAll("pre")
        for x in range (0,len(mess)):
            data_mess = mess[x]
            if x%2 ==0:
                b_data = data_mess.findAll("b")
                infomess = data_mess.text.strip()
            if x %2 ==1 :
                comment = data_mess.text.strip()

    except:
        pass
    try:
        storedata.storedDebian(database, table_database, bugid, btstype, author, created, updated, resolved, summary, affect, status, comtid, sfeid, symid, plmid, relbug, keyword)
    except:
        print "error save data debian", bugid