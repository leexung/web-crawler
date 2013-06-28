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






bugidlist =[]
lasttime = 0

def getUpdate (i):
    global bugidlist
    global lasttime
    try:
        url = "http://www.mantisbt.org/bugs/view_all_bug_page.php?page_number=%d" %(i)
        page =  urllib.urlopen(url)
        data = page.read()
        soup = BeautifulSoup(data)
        form =soup.find("table",{"id":"buglist"})
        tab = []
        tab = form.findAll("tr")
        for x in range (5,len(tab)-1):
            column = []
            column = tab[x].findAll("td")

            for i in range (0,len (column)):
                bugid = column[3].text.strip()
                time = column [8].text.strip()
            lasttime = int(time.replace("-",""))
            bugidlist.append(bugid)
    except:
        pass

def update(timeEnd):
    global lasttime
    global bugidlist
    until = timeEnd
    x = 0
    while 1:
        try:
            getUpdate(x)
        except:
            x = x-1
        x = x+1
        lasttime = 0
        if lasttime <= until:
            break
    for x in range (0,len(bugidlist)):
        print "update mantis ", bugidlist[x]
        crawler(int(bugidlist[x]))










def crawler(i):
    try:

        btstype = "mantisbug"
        author = ""
        owner = ""
        severity ="normal"
        status = "open"
        summary = "null"
        cmtid = "null"
        sfeid    = ""
        symid = "null"
        plmid = "linux"
        relbug = "null"
        updated = 0
        created = 0
        resolved = 0
        keyword = ""
        lastbugidx =0
        lastbugid = 0
        assigned =""
        bugid = i
        database = "mantis0"
        #try:
        url = "http://www.mantisbt.org/bugs/view.php?id=%d" %(i)

        page =  urllib.urlopen(url)

        #except:
        #print ("error")
        data = page.read()
        soup = BeautifulSoup(data)
        #get summary
        try:
            summary = soup.find("title").text

        except:
            pass
        try:

            row1 =[]
            row1 = soup.findAll("tr",{"class":"row-1"})
            row1_1 = row1[0]
            data_row_1_1 = []
            data_row_1_1 = row1_1.findAll("td")
            cmtid = data_row_1_1[1].text.strip()
            severity = data_row_1_1[2].text.strip()
            create = data_row_1_1[4].text.strip()
            create = create.replace("-","")
            create = create.replace(":","")
            create = create.replace(" ","")
            created = int(create)
            update = data_row_1_1[5].text.strip()
            update = update.replace("-","")
            update = update.replace(":","")
            update = update.replace(" ","")
            updated = int(update)
        except:
            pass
        try:
        #####
            row1_2 = row1[1]
            data_row_1_2 = []
            data_row_1_2 = row1_2.findAll("td")
            assigned = data_row_1_2[1].text.strip()
        except:
            pass
        try:
        #print ("assigned :",assigned)
        ### status
            row1_3 = row1[2]
            data_row_1_3 = []
            data_row_1_3 = row1_3.findAll("td")
            stt = data_row_1_3[1].text.strip()
            if stt.__contains__('fix')or stt.__contains__('closed'):
                    status = "fixed"
            else:
                status = "open"

            product_version =data_row_1_3[4].text.strip()
            #print ("product_version :",product_version)
        except:
            pass
        try:

        ###############
            row2 =[]
            row2 = soup.findAll("tr",{"class":"row-2"})
            row2_1 = row2[0]
            data_row_2_1 = []
            data_row_2_1 = row2_1.findAll("td")
            author = data_row_2_1[1].text.strip()
        except:
            pass
        try:
        #####priority & resolution
            row2_2 = row2[1]
            data_row_2_2 = []
            data_row_2_2 = row2_2.findAll("td")
            priority = data_row_2_2[1].text.strip()
            severity =  data_row_2_2[3].text.strip()
        except:
            pass
        try:
        ###PLATFORM
            row2_3 = row2[2]
            data_row_2_3 = []
            data_row_2_3 = row2_3.findAll("td")
            #platform = data_row_2_3[3].text.strip()

        except:
            pass
        try:

         ######## description
            row2_5 = row2[4]
            data_row_2_5 = []
            data_row_2_5 = row2_5.findAll("td")
            description = data_row_2_5[1].text.strip()
        except:
            pass
        try:
        ###### comment
            allcomment = ""
            bugnote =[]
            bugnote = soup.findAll("tr",{"class":"bugnote"})
            for x in range (0,len(bugnote)):
                note = bugnote[x]
                detail = []
                detail = note.findAll("span")
                publ = note.find("td",{"class":"bugnote-public"}).text.strip()
                comment = note.find("td",{"class":"bugnote-note-public"}).text.strip()
                allcomment = allcomment + "||" + publ + "||" + comment + "||"
        #######keyword


            keyword = "description: " + description + "||| all comment:" + allcomment
        except:
            pass
        try:
            ######
            row2_3 = row2[2]
            data_row_2_3 = []
            data_row_2_3 = row2_3.findAll("td")
            platform = data_row_2_3[1].text.strip()
            #print (platform)
            check = 0
            if platform.__contains__("Ubuntu"):
                check = check + 1
            if platform.__contains__("mac"):
                check = check + 1
            if platform.__contains__("win"):
                check = check + 1
            if check > 1:
                plmid = "all"
            else:
                if platform.__contains__("Ubuntu"):
                    plmid = "linux"
                elif platform.__contains__("win"):
                    plmid = "win"
                elif platform.__contains__("mac"):
                    plmid = "mac"
                else:
                    plmid = "other"
            os = data_row_2_3[3].text.strip()
            #print("os",os)
            os_version = data_row_2_3[5].text.strip()
            #print ("os_version",os_version)
            ###history and relationship
        except:
            pass
        try:
            relationship = soup.find("div",{"id":"relationships_open"})
            data_relationship =[]
            data_relationship = relationship.findAll("tr")
            relbug =""
        #print(len(data_relationship))
            for x in range (2,len(data_relationship)):
                rowx = []
                rowx = data_relationship[x]
                rowx_data = []
                rowx_data = rowx.findAll("td")
                rowxdata = ""
                for y in range (0,len(rowx_data)):
                    rowxdata = rowxdata + rowx_data[y].text.strip() + " "
                #print(rowxdata)
                relbug = relbug + rowxdata
        except:
            pass
        created = int (created/10000)
        updated = int (updated/10000)
        if status == "fixed":
            resolved = updated
            updated = 0
        try:
            cmtid = re.escape(cmtid)
            summary = re.escape(summary)
            keyword = re.escape(keyword)
            author  = re.escape (author)
            relbug = re.escape (relbug)
        except:
            pass
        if summary == "MantisBT":
            pass
        else:
            try:
                database = "thesis"
                table_database = "bugdata"
                storedata.storedMantis(database,table_database, bugid, btstype, author, created, updated, resolved, summary, severity, status, cmtid, sfeid, symid, plmid, relbug, keyword)
            except:
                print "error save databse mantis" , bugid
    except:
        pass
def run(start,end):
    for x in range (start,end):
        try:
            print "crawler mantis ",x
            crawler(x)
        except:
            print"error crawler mantis ",x
