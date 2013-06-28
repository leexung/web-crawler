import time
import math,re
from cgi import escape
from traceback import format_exc
import codecs
import os
from nltk.corpus import stopwords
from stemming.porter2 import stem
import filterdata
import MySQLdb

pass_database = "123456"
user_database = "root"
database = "database"
def proces(x):
    conn = MySQLdb.connect(user = user_database, db = database, passwd = pass_database, host = "localhost" , port = 3306)
    cur = conn.cursor()
    title =""
    author =""
    affect =""
    note =""
    highlight =""
    description =""
    comment =""
    try:
        query = "SELECT description FROM launchpad where bugidx = %d"%(x)
        cur.execute(query)
        dataTerm = cur.fetchone()
        description = dataTerm[0]
    except:
        print
    try:
        query = "SELECT title FROM launchpad where bugidx = %d"%(x)
        cur.execute(query)
        dataTerm = cur.fetchone()
        title = dataTerm[0]
    except:
        print
    try:
        query = "SELECT author FROM launchpad where bugidx = %d"%(x)
        cur.execute(query)
        dataTerm = cur.fetchone()
        author = dataTerm[0]
    except:
        print
    try:
        query = "SELECT affect FROM launchpad where bugidx = %d"%(x)
        cur.execute(query)
        dataTerm = cur.fetchone()
        affect = dataTerm[0]
    except:
        print
    try:
        query = "SELECT note FROM launchpad where bugidx = %d"%(x)
        cur.execute(query)
        dataTerm = cur.fetchone()
        note = dataTerm[0]
    except:
        print
    try:
        query = "SELECT highlight FROM launchpad where bugidx = %d"%(x)
        cur.execute(query)
        dataTerm = cur.fetchone()
        highlight = dataTerm[0]
    except:
        print
    try:
        query = "SELECT comment FROM launchpad where bugidx = %d"%(x)
        cur.execute(query)
        dataTerm = cur.fetchone()
        comment = dataTerm[0]
    except:
        print
    cur.close()
    conn.close()
    title = filterdata.filter(title)
    author = filterdata.filter(author)
    affect = filterdata.filter(affect)
    note = filterdata.filter(note)
    highlight = filterdata.filter(highlight)
    description = filterdata.filter(description)
    comment = filterdata.filter(comment)
    #------------
    title = re.escape(title)
    author = re.escape(author)
    affect = re.escape(affect)
    note = re.escape(note)
    highlight = re.escape(highlight)
    description = re.escape(description)
    comment = re.escape(comment)
    # updated
    try:
        conn = MySQLdb.connect(user = user_database, db = database, passwd = pass_database, host = "localhost" , port = 3306)
        cur = conn.cursor()
        sql = "UPDATE launchpadFinal SET title = '%s', author ='%s', affect = '%s', note = '%s', highlight ='%s', description = '%s', comment = '%s' where bugidx =%d" % (title, author, affect,note,highlight,description,comment ,x)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except:
        print "error updated"
for x in range (0,8383):
    try:
        proces(x)
        print "ok process ",x
    except:
        print "error process bugid ", x