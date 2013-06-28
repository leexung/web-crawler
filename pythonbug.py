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
import datetime
lastday = ""
bugidlist = []




def run(start,end):
    for x in range (start,end):
        try:
            print "crawl pythonbug ",x
            crawler(x)
        except:
            print "error crawl pythonbug ", x

def getUpdate(x):
    global bugidlist
    global lastday
    url = "http://bugs.python.org/issue?@startwith=%d&@pagesize=50&@sort=-activity" %(x)
    page =  urllib.urlopen(url)
    data = page.read().decode("utf-8")
    soup = BeautifulSoup(data)
    table =[]
    table =soup.find("table",{"class":"list"})
    row = []
    row = table.findAll("tr")
    for x in range (1,len(row)):
        column = []
        column = row[x].findAll("td")
        bugid = column[1].text.strip()
        time = column[3].text.strip()
        bugidlist.append(bugid)
    lastday = time

def update(timeEnd):
    check = ""
    try:
        d = int(timeEnd%100)
        y = int (timeEnd/10000)
        m = int ((timeEnd - 10000*y)/100)

        t = datetime.datetime(y,m,d)
        t.strftime('%Y-%m-%d')
        day = datetime.datetime.now() - t
        numday = []
        numday = str(day).split(" ")

        dayUpdate = int(numday[0])
        if dayUpdate == 1:
            check = "yesterday"
        elif dayUpdate >1 and dayUpdate <30:
            check = "%d days"%(dayUpdate)
        elif dayUpdate >30 :
            mon = dayUpdate/30
            check = "%d months"%(mon)
    except:
        check = "hours"

    global bugidlist
    global lastday
    x = 0
    while 1:
        try:
            getUpdate(x)
        except:
            pass
        x = x+50

        if lastday.__contains__(check) :
            break
    for x in range (0,len(bugidlist)):
        print "updated python bug id", bugidlist[x]
        crawler(int(bugidlist[x]))
def crawler(bugid):
    try:
        url = "http://bugs.python.org/issue%d" %(bugid)
        page =  urllib.urlopen(url)
        data = page.read().decode("utf-8")
        soup = BeautifulSoup(data)
        #get summary
        title = soup.find("title").text.strip()
        ### get table form
        table_form = []
        table_form = soup.findAll("table",{"class":"form"})
        ###### table classification
        table_classification = table_form[0]
        row_classification =[]
        row_classification = table_classification.findAll("td")
        type = row_classification[1].text.strip()
        stage = row_classification[2].text.strip()
        component = row_classification[3].text.strip()
        version = row_classification[4].text.strip()
        #### table process
        table_process = table_form[1]
        row_process = []
        row_process = table_process.findAll("td")
        status_python = row_process[0].text.strip()
        resolution = row_process[1].text.strip()
        dependencies = row_process[2].text.strip()
        superseder = row_process[3].text.strip()
        assign = row_process[4].text.strip()
        nosylist = row_process[5].text.strip()
        priority = row_process[6].text.strip()
        kw = row_process[7].text.strip()
        ### table_time
        p_time = soup.find("p")
        data_time =[]
        data_time = p_time.findAll("strong")
        create = data_time[0].text.strip()
        author = data_time[1].text.strip()
        update = data_time[2].text.strip()
        assign = data_time[3].text.strip()
        time_cre = []
        time_up =[]
        time_cre = create.split(" ")
        time_up = update.split(" ")
        created = str(time_cre[0])
        created = created.replace("-","")

        updated = str(time_up[0])
        updated = updated.replace("-","")
        ##get keyword
        table_mess = soup.find("table",{"class":"messages"})
        row_mess = []
        row_mess = table_mess.findAll("tr")

        for x in range(1,len(row_mess)):
            row_mess_data = row_mess[x]
            column_mess = []
            column_mess = row_mess_data.findAll("th")
            try:
                author_mess = column_mess[1].text.strip()
                time_mess = column_mess[2].text.strip()

            except:
                pass
            try:
                mess = row_mess_data.find("pre").text.strip()
            except:
                pass


        if status_python == "closed":
            status = "fixed"
        else:
            status = "open"
        comtid = component
        owner = assign
        relbug = dependencies
        comment = mess
        keyword = kw
        affect = version
        plmid = "all"
        btstype = "pythonBug"
        database = "thesis"
        table_database = "bugdata"
        resolved = 0
        sfeid = "python"
        symid =priority
        summary = title
        severity = ""
        try:
            storedata.storedPythonBug(database, table_database, bugid, btstype, author, created, updated, resolved, summary, severity, status, comtid, sfeid, symid, plmid, relbug, keyword)
        except:
            print "error save data python bug ",bugid
    except:
        print "error crawl python bug ", bugid