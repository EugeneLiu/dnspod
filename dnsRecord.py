#-*-coding:utf-8 -*-
#自动搜索DNS记录模块

import sys,DNS

def hierquery(qstring,qtype):
    reqobj = DNS.Request()
    try:
        answerobj = reqobj.req(name = qstring,qtype = qtype)
        answers = [x['data'] for x in answerobj.answers if x['type'] == qtype]
    except DNS.Base.DNSError:
        answers = []
    if len(answers):
        return answers
    else:
        remainder = qstring.split(".",1)
        if len(remainder) == 1:
            return None
        else:
            return hierquery(remainder[1],qtype)

def findnameservers(hostname):
    return hierquery(hostname,DNS.Type.NS)

def getrecordsfromnameserver(qstring,qtype,nslist):
    for ns in nslist:
        reqobj = DNS.Request(server = ns)
        try:
            answers = reqobj.req(name = qstring,qtype = qtype).answers
            if len(answers):
                return answers
        except DNS.Base.DNSError:
            pass
    return []

def nslookup(qstring,qtype,verbose = 1):
    nslist = findnameservers(qstring)
    if nslist == None:
        raise RuntimeError,'Could not find nameserver to use.'
    if verbose:
        print "Using nameservers:",",".join(nslist)
    return getrecordsfromnameserver(qstring,qtype,nslist)

def dnsRecord(domain):
    DNS.DiscoverNameServers()

    answers = nslookup(domain,DNS.Type.ANY)
    if not len(answers):
        return -1
    else:
        return answers
