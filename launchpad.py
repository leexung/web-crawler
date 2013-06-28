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
bugidlist = []
lastedtime = [1]



def run(start,end):
    for x in range (start,end):
        try:
            print "crawler launchpad bug ", x
            crawler(x)
        except:
            print "error crawler launchpad ", x

def update(timeEnd):
    out_file = open("bugidlist.txt", "w")
    term = " "
    out_file.write(term)
    out_file.close()

    global bugidlist
    until = timeEnd
    x = 0
    while 1:
        try:
            getUpdate(x)
        except:
            x = x-75
        x = x+75
        lastTime = 0
        try:
            lastTime = int(lastedtime[0])
        except:
            pass
        if lastTime == until:
            break
    """
    f = open('bugidlist.txt')
    data = f.read()
    f.close()
    buglist = []
    buglist = data.split(" ")
    """
    for x in range (0,len(bugidlist)):
        crawler(int(bugidlist[x]))


def getUpdate(i):
    global bugidlist
    number = i
    cj = cookielib.MozillaCookieJar()
    cj.load(os.path.join(os.path.expanduser(""),"cookies.txt"))
    url1 = "https://bugs.launchpad.net/bugs/+bugs?field.searchtext=&search=Search&field.status%3Alist=NEW&field.status%3Alist=OPINION&field.status%3Alist=INVALID&field.status%3Alist=WONTFIX&field.status%3Alist=EXPIRED&field.status%3Alist=CONFIRMED&field.status%3Alist=TRIAGED&field.status%3Alist=INPROGRESS&field.status%3Alist=INCOMPLETE_WITH_RESPONSE&field.status%3Alist=INCOMPLETE_WITHOUT_RESPONSE&assignee_option=any&field.assignee=&field.bug_reporter=&field.bug_commenter=&field.subscriber=&field.tag=&field.tags_combinator=ANY&field.status_upstream-empty-marker=1&field.has_cve.used=&field.omit_dupes.used=&field.omit_dupes=on&field.affects_me.used=&field.has_patch.used=&field.has_branches.used=&field.has_branches=on&field.has_no_branches.used=&field.has_no_branches=on&field.has_blueprints.used=&field.has_blueprints=on&field.has_no_blueprints.used=&field.has_no_blueprints=on&orderby=-date_last_updated&start="
    url2 = "%d"%(number)
    url = url1+url2
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    r = opener.open(url).read()
    data = r.decode("utf-8")
    soup = BeautifulSoup(data)
    try:
        tab = []
        tab = soup.findAll("div", {"class": "buglisting-row"})
    except:
        pass
    try:
        for x in range(0,len(tab)):
            table = tab[x]
            bugid = table.find("span",{"class":"bugnumber"}).renderContents().decode("utf-8").strip()
            time = table.find("span",{"class":"sprite milestone field"}).renderContents().decode("utf-8").strip()
            bugid = bugid.replace("#", "")
            bugidlist.append(bugid)
            time = time.replace("Last updated", "")
            time = time.replace("ago", "")
            time = time.replace("on", "")
            time = time.replace("-", "")
            out_file = open("bugidlist.txt", "a")
            term = bugid + " "
            out_file.write(term)
            out_file.close()
            lastedtime[0] = time
    except:
        pass





def crawler(bugid):
    btstype = "launchpad"
    database = "thesis"
    table_database = "bugdata"
    url = "https://bugs.launchpad.net/ubuntu/+bug/" + str(bugid)

    try:

        page = urllib.urlopen(url)
        html = page.read().decode("utf-8")

        soup = BeautifulSoup(html)

        titletemp = soup.find('span',"yui3-editable_text-text ellipsis")
        title = titletemp.string.encode('utf-8').strip()

        authortemp = soup.find('div',"registering").get_text()
        authortemp1 = authortemp.strip().encode('utf-8')
        authortemp2 = re.search("Reported by",authortemp1)
        authortemp3 = authortemp1[authortemp2.end():]
        author1 = re.sub(r'\son\s.*$',"",authortemp3)
        author = author1.strip()

        create = re.search(r'\d+-\d+-\d+',authortemp3).group()
        #create = "-".join(createtemp)
        create = str(create)
        updatetemp = soup.find('script', id="json-cache-script").get_text()
        updatetemp1 = re.search(r'("date_last_updated": .\d+-\d+-\d+)', updatetemp).group()
        update = re.sub(r'"date_last_updated": .',"",updatetemp1)
        update = str (update)
        affecttemp = soup.find_all('a', "sprite product",True)
        affecttemp1 = soup.find_all('a', "sprite distribution",True)
        affecttemp2 = soup.find_all('a', "sprite package-source",True)
        affect1 = []
        for value in affecttemp:
            text = value.get_text()
            affect1.append(text.encode('utf-8'))
        for value in affecttemp1:
            text = value.get_text()
            affect1.append(text.encode('utf-8'))
        for value in affecttemp2:
            text = value.get_text()
            affect1.append(text.encode('utf-8'))
        affect = " | ".join(affect1)

        table = []
        tabletemp = soup.find_all("tr", {"id" : re.compile("tasksummary")})
        for value in tabletemp:
            text = value.get_text().encode('utf-8')
            table.append(str(text.strip()))
        table1 = re.sub(r'\s+Edit',""," | ".join(table))
        table2 = re.sub(r'\xe2\x80\x8b',"",table1)
        table3 = re.sub("\s+\n+"," ,",table2)
        a = table3.split('|')
        checkok = []
        if len(a)<2:
            note =""
        else:
            for value in a:
                checka = value.split(',')
                if checka[0] == " " or checka == "":
                    del checka[0]
                else:
                    pass
                checkb = " , ".join(checka)
                checkok.append(checkb)
            note = " | ".join(checkok)

        highlighttemp = soup.find('tr', {"class" : re.compile("highlight")})
        highlighttemp1 = highlighttemp.get_text().encode('utf-8')
        highlight1 = re.sub(r'\sEdit'," ",highlighttemp1)
        highlight2 = re.sub(r'\xe2\x80\x8b',"",highlight1)
        highlight3 = re.sub("\s+\n+",",",highlight2)
        b = highlight3.split(',')
        c = []
        for value in b:
            if value!="":
                c.append(value)
        highlight = ",".join(c)

        duplicatetemp = soup.find_all('a',{"class" : "sprite bug"})
        duplicatetemp2 = soup.find_all('a',{"id" : "duplicate-of-warning-link-bugtasks"})
        duplicatetemp1 = []
        duplicatetemp3 = []
        for value in duplicatetemp:
            text = value.get_text().encode('utf-8')
            duplicatetemp1.append(str(text.strip()))
        for value in duplicatetemp2:
            text = value.get_text().encode('utf-8')
            if text!="":
                duplicatetemp3 = text.split(':')
                duplicatetemp1.append(duplicatetemp3[0].strip())
            else:
                duplicatetemp1.append(str(text.strip()))
        duplicate = " | ".join(duplicatetemp1)

        comtidtemp = soup.base.get('href')
        comtidtemp1 = re.split('/',comtidtemp)
        comtid = comtidtemp1[3]

        relbugtemp = soup.find_all('div',{"class" : "bug-branch-summary"})
        relbugtemp1 = []
        for value in relbugtemp:
            text = value.get_text().encode('utf-8')
            relbugtemp1.append(str(text.strip()))
        relbug = " | ".join(relbugtemp1)

        descriptiontemp = soup.find_all('div',{"class" : "yui3-editable_text-text"})
        descriptiontemp1 = []
        for value in descriptiontemp:
            text = value.get_text().encode('utf-8')
            descriptiontemp1.append(str(text.strip()))
        description = " ".join(descriptiontemp1)

        commenttemp = soup.find_all('div',{"itemtype" : "http://schema.org/UserComments"})
        commenttemp1 = []
        for value in commenttemp:
            text = value.get_text().encode('utf-8')
            commenttemp1.append(str(text.strip()))
        commenttemp2 = " | ".join(commenttemp1)
        commenttemp3 = re.sub(r'\n+'," ",commenttemp2)
        comment = re.sub(r'\s+'," ",commenttemp3)

        numcomment = str(len(commenttemp1))

        storedata.storedLaunchpad(database,table_database, title, author, create, update, affect, note, highlight, duplicate, comtid, relbug, description, comment, numcomment, bugid, btstype)
    except urllib2.HTTPError:
        pass