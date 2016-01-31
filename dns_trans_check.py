#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import os
import threading
import urlparse

lock = threading.Lock()

# 从列表中获取乌云厂商域名
domains = []
f = open("corps.txt","r")
reg = re.compile(r'((http://)?(www\.)?)\/?')
for line in f.readlines():
    domain = re.sub(reg,'',line)
    domains.append(domain)
    # print domain
f.close()

# 对域名列表进行检测
index = 0
f1 = open("vul_domain.txt","a")
def dns_check():
    global index
    global f1
    while True:
        lock.acquire()
        if index >= len(domains):
            lock.release()
            break
        domain = domains[index]
        index += 1
        print "Checking " + domain
        lock.release()

        res = os.popen('nslookup -type=ns ' + domain).read()
        nameserver = re.findall(r'nameserver = ([\w\.]+)',res)
        # print nameserver
        for server in nameserver:
            if len(server) < 5:
                server += domain
            res = os.popen('dig axfr @%s %s' % (server,domain)).read()
            print res
            if res.find('Transfer failed.') < 0 and res.find('connection timed out') < 0 and res.find('XFR size') > 0:
                # found vulnerable dns server
                lock.acquire()
                print 'Found vulnerable dns server : ' + server
                f1.write("%s   %s" % (server.ljust(25),domain))
                lock.release()


threads = []
for i in range(10):
    t = threading.Thread(target=dns_check)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

f1.close()
print 'End'