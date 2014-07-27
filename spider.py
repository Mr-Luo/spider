#!/usr/bin/python
#coding=utf8
import urllib2
import os
import re
import pymongo
site = "http://www.dy2018.com"
html = urllib2.urlopen('http://www.dy2018.com').read()
#转编码
html = unicode(html,'gbk').encode('utf-8')
f = open("tmp","w");
f.write(html)
res = open("result","a")

#爬取下载地址
def getDownloadPath(path):
   page =  urllib2.urlopen(path).read()
   content = open("siteTmp","w")
   page = unicode(page,'gbk').encode('utf-8')
   content.write(page)
   regex=r"<a\s+href\s*=\s*[\"']?(ftp{0,1}[^\"'\s]+)[\"']?>([^<]+)</a>"
   for line in open("siteTmp","r"):
       result = re.search(regex,line)
       if result != None:
            return result.group(1)

#连接数据库
def getConn():
    client = pymongo.MongoClient("localhost",27017)
    return client
#用正则模块
prog = re.compile(r"<a.*>");
for line in open("tmp","r")  :
    result =  prog.search(line)
    if result:
        result = re.search(r"<li><a\s+href\s*=\s*[\"']?([^\"'\s]+)[\"']?\s+title=[\"']?[^\"]+[\"']?>([^<]+)</a>",line)
        if result != None:
                downloadPath =  getDownloadPath(site+result.group(1))
                res.write(site + result.group(1) + " ==> "+ result.group(2) + " ===> download: " + downloadPath+"\n")
                name =re.sub(r"\.","_",result.group(2)+"")
                #path =re.sub(r"\.","_",site+result.group(1)+"")
                path =site+result.group(1)+""
                getConn().dy2018.film.insert({name:{"site":path,"downloadPath":downloadPath}})



if __name__ == "__main__":
    pass
