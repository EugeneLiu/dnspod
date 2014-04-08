#-*- coding:utf-8 -*-
#此模块是按照请求，调用DNSPodAPI返回相应的数据字典
import urllib,urllib2
import httplib
import json

class DNSPodAPI:
    "运用DNSPod官方API实现基本操作"
    def __init__(self,email,password,**kw):
        self.base_url = 'dnsapi.cn'

        self.postdata = dict(
            login_email = email,
            login_password = password,
            format = "json"
        )

        self.postdata.update(kw)

    def request(self,path,**kw):
        self.path = path
        conn = httplib.HTTPSConnection(self.base_url)
        headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/json",
                "User-Agent": "dnspod-pythonweb/0.2 (liujingguozhi@gmail.com)"
            }
        
        if path == '/Record.Create':
            self.postdata.update(kw['d'])
            #s = '&'.join(['%s=%s'%(k,str(v))for k,v in self.postdata.items() if k != 'record_line'])
            #一直线路错误，只好用这种笨办法。无奈之举
            s = 'login_email=%s&login_password=%s&format=%s&domain_id=%s&sub_domain=%s&record_type=%s&record_line=%s&value=%s&ttl=%s&mx=%s'%(str(self.postdata['login_email']),str(self.postdata['login_password']),str(self.postdata['format']),str(self.postdata['domain_id']),str(self.postdata['sub_domain']),str(self.postdata['record_type']),self.postdata['route_line'],str(self.postdata['value']),str(self.postdata['ttl']),str(self.postdata['mx']))
            conn.request("POST",path,s,headers)
        elif path == '/Record.Modify':
            self.postdata.update(kw['d'])
            
            s = 'login_email=%s&login_password=%s&format=%s&domain_id=%s&record_id=%s&sub_domain=%s&record_type=%s&record_line=%s&value=%s&ttl=%s&mx=%s'%(str(self.postdata['login_email']),str(self.postdata['login_password']),str(self.postdata['format']),str(self.postdata['domain_id']),str(self.postdata['record_id']),str(self.postdata['sub_domain']),str(self.postdata['record_type']),self.postdata['route_line'],str(self.postdata['value']),str(self.postdata['ttl']),str(self.postdata['mx']))
            conn.request("POST",path,s,headers)
        else:
            self.postdata.update(kw)
            conn.request("POST",path,urllib.urlencode(self.postdata),headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        ret = json.loads(data)
        return ret
