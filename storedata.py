import optparse
import re
import sys
import time
import math
from cgi import escape
from traceback import format_exc
import codecs
import os
import os, cookielib, urllib
import MySQLdb

pass_database = "123456"
user_database = "root"
def storedLaunchpad( database, table_database, title , author , create,update,affect,note,highlight,duplicate,comtid,relbug,description,comment,numcomment,bugid,btstype):
    global pass_database
    global user_database
    create = create.replace('-','')
    update = update.replace('-','')
    table_database = table_database
    comment = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', comment)
    title = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', title)
    description = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', description)
    note = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', note)
    highlight = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', highlight)
    affect = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',affect)
    author = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',author)
    comtid = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',comtid)
    relbug = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',relbug)

    database = re.escape(database)
    title = re.escape(title)
    author = re.escape(author)
    created = int(create)
    updated = int(update)
    affect = re.escape(affect)
    note = re.escape(note)
    highlight = re.escape(highlight)
    duplicate = re.escape(duplicate)
    comtid = re.escape(comtid)
    relbug = re.escape(relbug)
    description = re.escape(description)
    comment = re.escape(comment)
    numcomment = re.escape(numcomment)
    btstype = re.escape(btstype)
    conn = MySQLdb.connect(user = user_database, db = database, passwd = pass_database, host = "localhost" , port = 3306)
    cur = conn.cursor()

    sqlcreated = "INSERT INTO %s (bugid,btstype,author,summary,created,updated,affect,note,highlight,duplicate,comtid,relbug,description,comment,numcomment) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (table_database,bugid,btstype,author,title,created,updated,affect,note,highlight,duplicate,comtid,relbug,description,comment,numcomment)

    cur.execute(sqlcreated)
    conn.commit()
    cur.close()
    conn.close()

def storedBugzilla( database, table_database ,bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword):
    global pass_database
    global user_database

    table_database = table_database

    title = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', summary)
    keyword = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', keyword)


    author = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',author)
    comtid = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',comtid)
    relbug = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',relbug)


    title = re.escape(title)
    author = re.escape(author)
    created = int(created)
    updated = int(updated)
    comtid = re.escape(comtid)
    relbug = re.escape(relbug)
    keyword = re.escape(keyword)
    btstype = re.escape(btstype)

    conn = MySQLdb.connect(user = user_database, db = database, passwd = pass_database, host = "localhost" , port = 3306)
    cur = conn.cursor()
    sqlcreated = "INSERT INTO %s (bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword) VALUES ('%d','%s','%s','%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (table_database,bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword)
    cur.execute(sqlcreated)
    conn.commit()
    cur.close()
    conn.close()

def storedMantis( database,table_database,bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword):
    global pass_database
    global user_database
    table_database = table_database

    title = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', summary)
    keyword = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', keyword)


    author = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',author)
    comtid = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',comtid)
    relbug = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',relbug)

    database = re.escape(database)
    title = re.escape(title)
    author = re.escape(author)
    created = int(created)
    updated = int(updated)
    comtid = re.escape(comtid)
    relbug = re.escape(relbug)
    keyword = re.escape(keyword)
    btstype = re.escape(btstype)




    conn = MySQLdb.connect(user = user_database, db = database, passwd = pass_database, host = "localhost" , port = 3306)
    cur = conn.cursor()
    sqlcreated = "INSERT INTO %s (bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword) VALUES ('%d','%s','%s','%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (table_database,bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword)
    cur.execute(sqlcreated)
    conn.commit()
    cur.close()
    conn.close()



def storedPythonBug( database,table_database,bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword):
    global pass_database
    global user_database
    table_database = table_database

    title = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', summary)
    keyword = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', keyword)


    author = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',author)
    comtid = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',comtid)
    relbug = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',relbug)

    database = re.escape(database)
    title = re.escape(title)
    author = re.escape(author)
    created = int(created)
    updated = int(updated)
    comtid = re.escape(comtid)
    relbug = re.escape(relbug)
    keyword = re.escape(keyword)
    btstype = re.escape(btstype)




    conn = MySQLdb.connect(user = user_database, db = database, passwd = pass_database, host = "localhost" , port = 3306)
    cur = conn.cursor()
    sqlcreated = "INSERT INTO %s (bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword) VALUES ('%d','%s','%s','%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (table_database,bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword)
    cur.execute(sqlcreated)
    conn.commit()
    cur.close()
    conn.close()

def storedDebian( database,table_database,bugid,btstype,author,created,updated,resolved,summary,affect,status,comtid,sfeid,symid,plmid,relbug,keyword):
    global pass_database
    global user_database
    table_database = table_database

    title = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', summary)
    keyword = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', keyword)

    affect = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '', affect)
    author = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',author)
    comtid = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',comtid)
    relbug = re.sub('[^a-zA-Z0-9\n\.\:\-\ \g]', '',relbug)
    affect = re.escape(affect)
    database = re.escape(database)
    title = re.escape(title)
    author = re.escape(author)
    created = int(created)
    updated = int(updated)
    comtid = re.escape(comtid)
    relbug = re.escape(relbug)
    keyword = re.escape(keyword)
    btstype = re.escape(btstype)
    summary = re.escape(summary)
    severity = ""



    conn = MySQLdb.connect(user = user_database, db = database, passwd = pass_database, host = "localhost" , port = 3306)
    cur = conn.cursor()
    sqlcreated = "INSERT INTO %s (bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword) VALUES ('%d','%s','%s','%d','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (table_database,bugid,btstype,author,created,updated,resolved,summary,severity,status,comtid,sfeid,symid,plmid,relbug,keyword)
    cur.execute(sqlcreated)
    conn.commit()
    cur.close()
    conn.close()