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

from bs4 import BeautifulSoup
import cookielib
import os, cookielib, urllib
import Cookie
import MySQLdb
import storedata

def run(start,end):
    for x in range (start,end):
        try:
            print "crawler bugzilla ",x
            crawler(x)
        except:
            print("Error crawler bug ",x," in bugzilla")

def update(bugid):
    print(bugid)

def crawler(i):


    bugid = i
    btstype = "bugzilla"
    author = ""
    owner = ""
    severity ="normal"
    status = "open"
    summary = ""
    cmtid = ""
    sfeid    = ""
    symid = "null"
    plmid = "linux"
    relbug = ""
    updated = 0
    created = 0
    resolved = 0
    keyword = ""
    assigned =""
    url = "https://bugzilla.mozilla.org/show_bug.cgi?id=%d" %(i)
    page =  urllib.urlopen(url)
    data = page.read().decode('utf-8')
    soup = BeautifulSoup(data)
    ###get title
    try:
        title = soup.find("title").text.strip()
        reo = "%d" %(bugid)
        title = title.replace(reo,'').strip()
        try:
            tit =[]
            tit = title.split(' ')
            replaceTitle = tit[0]

            title = title.replace(replaceTitle,'').strip()
        except:
            pass
    except:
        pass

    if (title != "Invalid Bug ID" and title != "Access Denied"):

    ###status
        try:
            status = soup.find("span", {"id":"static_bug_status"}).text
            status = status.strip()
            stt =[]
            stt = status.split()
            status = ""
            for x in range (0,len(stt)):
                status = status + " " +stt[x]

            if status.__contains__('FIXED')or status.__contains__('COMPLETED'):
                status = "fixed"
            else:
                status = "open"
        except:
            pass
        ### product
        try:
            product = soup.find("td",{"class":"field_value "}).text
        except:
            pass
        ### platform
        try:
            platform = soup.find("td",{"class":"field_value"}).text
        except:
            pass
        #print (platform)
        try:
            table = soup.find("table", {"class": "edit_form"})
        except:
            pass
        #print (table)
        ####### reported:
        try:
            table2 = soup.find("td", {"class":"bz_show_bug_column_table"})
            creat= table2.find("td").text.strip()
            cre =[]
            cre = creat.split()
            crea = ""
            crea = cre[0]

            crea = crea.replace("-", "")
            created = int(crea)
            try:
                author = table2.find("span", {"class": "fn"}).text.strip()
            except:
                author = table2.find("span", {"class": "vcard"}).text.strip()
            component  = soup.find ("td", {"class":"field_value ","id":"field_container_component"}).text
        except:
            pass
        #####
        try:
            table3 = soup.find ("td", {"class":"bz_show_bug_column","id":"bz_show_bug_column_1"})
            tr = []
            tr = table3.findAll("tr")
            plt = tr[8]
            plm = plt.find("td").text.strip()
            check = 0
            if plm.__contains__('Ubuntu') :
                check = check + 1
            if plm.__contains__('Mac'):
                check = check + 1
            if plm.__contains__('Windows'):
                check = check + 1
            if check > 1:
                plmid = "all"
            else:
                if plm.__contains__('Ubuntu'):
                    plmid = "linux"
                elif plm.__contains__('Windows'):
                    plmid = "win"
                elif plm.__contains__('Mac'):
                    plmid = "mac"
                else:
                    plmid = "other"
            sfeid = ""
            platform = plmid
        except:
            pass
        try:
            imp = tr[10]
            importa = imp.find("td").text.strip()
            importan =[]
            importan = importa.split()
            importance = importan[1]
            ass = tr[12]
            assigned = ass.find("td").text
            assigned = assigned.strip()
            table4 =  soup.find ("td", {"class":"bz_show_bug_column_table","id":"bz_show_bug_column_2"})
            tr2 =[]
            tr2 = table4.findAll("tr")
            udp = tr2[1]
            upda = udp.find("td").text
            updat =[]
            updat = upda.split()
            update = updat[0]
            update = update.replace("-","")
            updated = int(update)
            resolved =0
        except:
            pass
        if status.__contains__("fixed"):
            resolved = updated
            updated = 0
        #####get kewword
        try:
            table_comment = soup.find("table",{"class":"bz_comment_table"})
            td_comm =[]
            td_des =[]
            td_des =  table_comment.findAll("div",{"class":"bz_comment bz_first_comment"})
            td_description =td_des[0]
            td_comm = table_comment.findAll("div",{"class":"bz_comment"})
            try:
                fn = td_description.find("span",{"class":"fn"}).text
            except:
                fn = td_description.find("span",{"class":"vcard"}).text
            description_time = td_description.find("span",{"class":"bz_comment_time"}).text.strip()
            description_text = td_description.find("pre",{"class":"bz_comment_text"}).text
            keyword = ""
            description = ""
            description = description + "author: " +  fn +"\n" + "time " + description_time +"\n" +"description " + description_text + "\n"
        except:
            pass
        #####
        try:
            user =[""]*(len(td_comm) -1)
            time_comment =[""]*(len(td_comm) -1)
            comment_text =[""]*(len(td_comm) -1)

            for x in range (1,len(td_comm)):
                commentx = td_comm[x]
                user[x-1]= commentx.find("span",{"class","vcard"}).text.strip()
                time_comment[x-1]=commentx.find("span",{"class","bz_comment_time"}).text.strip()
                comment_text[x-1]=commentx.find("pre",{"class","bz_comment_text"}).text.strip()
            allcomment = ""
            for x in range (0,len(user)):
                allcomment = allcomment + "user " + user[x] + "\n" + "time " + time_comment[x]+ "\n" + "comment: " + comment_text[x] + "\n"
        except:
            pass
        try:
            if importance == "feature":
                severity = "feature"
            elif importance == "minor":
                severity = "minor"
            elif importance == "normal":
                severity = "normal"
            else :
                importance = "critical"
        except:
            pass
        relbug =""
        try:
            comtid = re.escape(component)
            summary = re.escape(title)
            keyword = description
            author  = re.escape (author)
            keyword = re.sub('[^a-zA-Z0-9\n\.]', ' ', keyword)
        except:
            pass

        database = "thesis"
        table_database ="bugdata"

        try:
            storedata.storedBugzilla( database, table_database ,bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword)
        except:
            print "error stored data bugzilla ",bugid



