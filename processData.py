#-*- coding:utf-8 -*-
#此模块为处理数据模块
import post
import re

def processData(postdict,key):
    "按要求处理获得的dict类数据，并返回相应的列表或状态码"
    if key == 'status':
        return postdict[key]['code']
    if key == 'domains':
        return [i['name'] for i in postdict[key]]
    if key == 'domain':
        return postdict[key]['id']
    if key == 'records':
        return postdict[key]
    if key == 'record':
        return postdict[key]

def signin(email,password):
    "验证登录"
    path = '/Info.Version'#通过验证版本信息来验证登录是否成功
    pattern = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$") #验证邮箱的格式的正则表达式
    if email == '':
        return "邮箱不能为空！"
    elif not pattern.match(email):
        return "邮箱格式不正确！"
    elif password == '':
        return "密码不能为空！"
    else:
        postData = post.DNSPodAPI(email,password)
        messageDict = postData.request(path)
        messageCode = processData(messageDict,'status')
        if messageCode == '1':
            return messageCode
        else:
            return "登陆失败，请检查邮箱或密码是否正确！"

def domainList(email,password):
    "获取域名列表并返回相应的域名列表"
    path = "/Domain.List"
    postData = post.DNSPodAPI(email,password)
    domainsDict = postData.request(path)
    statusCode = processData(domainsDict,'status')
    if statusCode == '9':
        return ['没有任何域名记录，请添加！']
    elif statusCode == '6':
        return ['记录开始的偏移无效,请刷新！']
    elif statusCode == '7':
        return ['共要获取的记录的数量无效，请刷新！']
    elif statusCode == '1':
        domainsList = processData(domainsDict,'domains')
        return domainsList

def addDomain(email,password,**kw):
    "添加新的域名，并返回相应的信息"
    path="/Domain.Create"
    postData = post.DNSPodAPI(email,password)
    messageDict = postData.request(path,domain=kw['domain'])
    statusCode = processData(messageDict,'status')
    if statusCode == '1':
        return statusCode
    elif statusCode == '6':
        return '域名无效'
    elif statusCode == '7':
        return '域名已存在'
    elif statusCode == '11':
        return '域名已经存在并且是其它域名的别名'
    elif statusCode == '12':
        return '域名已经存在并且您没有权限管理'
    elif statusCode == '41':
        return '网站内容不符合DNSPod解析服务条款，域名添加失败'
    
def delDomain(email,password,**kw):
    "删除指定域名，并返回"
    path = '/Domain.Remove'
    postData = post.DNSPodAPI(email,password)
    messageDict = postData.request(path,domain=kw['domain'])
    statusCode = processData(messageDict,'status')
    if statusCode == '1':
        return statusCode
    elif statusCode == '-15':
        return '域名已被封禁'
    elif statusCode == '6':
        return '域名ID错误'
    elif statusCode == '7':
        return '域名已锁定'
    elif statusCode == '8':
        return 'VIP域名不可以删除'
    elif statusCode == '9':
        return '非域名所有者'

def domainInfo(email,password,**kw):
    "获取指定域名的信息，并返回域名ID"
    path = "/Domain.Info"
    postData = post.DNSPodAPI(email,password)
    messageDict = postData.request(path,domain=kw['domain'])
    domainId = processData(messageDict,'domain')
    return domainId

def recordList(email,password,**kw):
    "获取指定域名的记录列表，并返回相应的记录列表"
    path = "/Record.List"
    postData = post.DNSPodAPI(email,password)
    messageDict = postData.request(path,domain_id=kw['id'])
    recordList = processData(messageDict,'records')
    return recordList

def delRecord(email,password,**kw):
    "删除指定域名的记录，并返回相应的信息"
    path = "/Record.Remove"
    postData = post.DNSPodAPI(email,password)
    messageDict = postData.request(path,domain_id=kw['did'],record_id=kw['rid'])
    statusCode = processData(messageDict,'status')
    if statusCode == '1':
        return statusCode
    elif statusCode == '-15':
        return '域名已被封禁'
    elif statusCode == '-7':
        return '企业账号的域名需要升级才能设置'
    elif statusCode == '-8':
        return '代理名下用户的域名需要升级才能设置'
    elif statusCode == '6':
        return '域名ID错误'
    elif statusCode == '7':
        return '不是域名所有者或没有权限'
    elif statusCode == '8':
        return '记录ID错误'
    elif statusCode == '21':
        return '域名被锁定'
    elif statusCode == '78':
        return ' 不能删除默认的NS记录！'
    
def addRecord(email,password,**kw):
    "给指定域名添加记录，返回记录值"
    path = "/Record.Create"
    postData = post.DNSPodAPI(email,password)
    messageDict = postData.request(path,d = kw)
    statusCode = processData(messageDict,'status')
    if statusCode == '1':
        return statusCode
    elif statusCode == '-15':
        return '域名已被封禁'
    elif statusCode == '-7':
        return '企业账号的域名需要升级才能设置'
    elif statusCode == '-8':
        return '代理名下用户的域名需要升级才能设置'
    elif statusCode == '6':
        return '缺少参数或者参数错误'
    elif statusCode == '7':
        return '不是域名所有者或没有权限'
    elif statusCode == '21':
        return '域名被锁定'
    elif statusCode == '22':
        return '子域名不合法'
    elif statusCode == '23':
        return '子域名级数超出限制'
    elif statusCode == '24':
        return '泛解析子域名错误'
    elif statusCode == '25':
        return '轮循记录数量超出限制'
    elif statusCode == '26':
        return '记录线路错误'
    elif statusCode == '27':
        return '记录类型错误'
    elif statusCode == '30':
        return 'MX 值错误，1-20'
    elif statusCode == '31':
        return 'URL记录数超出限制'
    elif statusCode == '32':
        return 'NS 记录数超出限制'
    elif statusCode == '33':
        return 'AAAA 记录数超出限制'
    elif statusCode == '34':
        return '记录值非法'
    elif statusCode == '36':
        return '@主机的NS纪录只能添加默认线路'
    else:
        return '未知错误！'

def InfoRecord(email,password,**kw):
    "获取指定记录的详细信息"
    path = '/Record.Info'
    postData = post.DNSPodAPI(email,password)
    messageDict = postData.request(path,domain_id=kw['did'],record_id=kw['rid'])
    recordDict = processData(messageDict,'record')
    return recordDict

def updateRecord(email,password,**kw):
    "修改域名的指定记录信息"
    path = "/Record.Modify"
    postData = post.DNSPodAPI(email,password)
    messageDict = postData.request(path,d = kw)
    statusCode = processData(messageDict,'status')
    if statusCode == '1':
        return statusCode
    elif statusCode == '-15':
        return '域名已被封禁'
    elif statusCode == '-7':
        return '企业账号的域名需要升级才能设置'
    elif statusCode == '-8':
        return '代理名下用户的域名需要升级才能设置'
    elif statusCode == '6':
        return '缺少参数或者参数错误'
    elif statusCode == '7':
        return '不是域名所有者或没有权限'
    elif statusCode == '8':
        return '记录ID错误'
    elif statusCode == '21':
        return '域名被锁定'
    elif statusCode == '22':
        return '子域名不合法'
    elif statusCode == '23':
        return '子域名级数超出限制'
    elif statusCode == '24':
        return '泛解析子域名错误'
    elif statusCode == '25':
        return '轮循记录数量超出限制'
    elif statusCode == '26':
        return '记录线路错误'
    elif statusCode == '27':
        return '记录类型错误'
    elif statusCode == '29':
        return 'TTL值太小'
    elif statusCode == '30':
        return 'MX 值错误，1-20'
    elif statusCode == '31':
        return 'URL记录数超出限制'
    elif statusCode == '32':
        return 'NS 记录数超出限制'
    elif statusCode == '33':
        return 'AAAA 记录数超出限制'
    elif statusCode == '34':
        return '记录值非法'
    elif statusCode == '35':
        return '添加的IP不允许'
    elif statusCode == '36':
        return '@主机的NS纪录只能添加默认线路'

