#-*- coding:utf-8 -*-
#主函数模块
import web
import post
import re
import processData
import os
import dnsRecord

#url映射
urls = (
        '/','Index',
        '/domain','Domain',
        '/signout','Signout',
        '/deldomain/(.*)','Deldomain',
        '/viewdomain/(.*)','Viewdomain',
        '/addrecord/(.*)','AddRecord',
        '/delrecord/(.*)','Delrecord',
        '/updaterecord/(.*)','UpdateRecord',
        '/viewrecord','Viewrecord',
        '/upload/(.*)','Upload',
        '/download/(.*)','Download',
        '/loaddns/(.*)','Loaddns'
    )

app = web.application(urls,globals())

#模板的公共变量
t_globals = {
        'cookie':web.cookies,
        'status':'',
        'msg':''
    }

#指定模板目录，并设定公共模板
render = web.template.render('templates',base='base',globals=t_globals)

#创建登录表单
signin = web.form.Form(
                    web.form.Textbox('email',
                        class_='input',
                        description='邮箱'
                    ),
                    web.form.Password('password',
                        class_='input',
                        description='密码'
                    ),
                    web.form.Button('',
                        class_='btn_submit',
                        html=''
                    )
)

class Index:
    "首页类"
    def GET(self):
        signin_form = signin()
        return render.index(signin_form,msg="")

    def POST(self):
        signin_form = signin()
        if signin_form.validates():
            email = signin_form.d.email
            password = signin_form.d.password
            #用验证函数，返回“1”则登录成功进入条状页面，返回其他字符串则显示提示信息
            message = processData.signin(email,password)
            if message == '1':
                web.setcookie('email',email)
                web.setcookie('password',password)
                return render.temp(email)#temp为跳转页面，时间为一秒，跳转到‘/domain’页面
            else:
                return render.index(signin_form,message)
        else:
            return web.seeother('/')

class Domain:
    "域名操作界面类"
    def GET(self):
        domainsList = processData.domainList(web.cookies().email,web.cookies().password)
        return render.alldomain(domainsList)

    def POST(self):
        i = web.input()
        add_domain = i.adddomain
        message = processData.addDomain(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=add_domain
                                        )

        if message == '1':
            domainsList = processData.domainList(
                                        web.cookies().email,
                                        web.cookies().password
                                        )

            return render.alldomain(domainsList,msg="域名添加成功！")
        else:
            domainsList = processData.domainList(
                                                web.cookies().email,
                                                web.cookies().password
                                                )

            return render.alldomain(domainsList,msg=message)

class Deldomain:
    "删除指定域名类"
    def GET(self,domain):
        message = processData.delDomain(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=domain
                                        )
        if message == '1':
            domainsList = processData.domainList(
                                        web.cookies().email,
                                        web.cookies().password
                                        )
            return render.alldomain(domainsList,delMsg="域名已删除！")
        else:
            domainsList = processData.domainList(web.cookies().email,web.cookies().password)
            return render.alldomain(domainsList,delMsg=message)
        
class Viewdomain:
    "返回指定域名的记录列表类"
    def GET(self,domain):
        #获取指定域名ID
        domainID = processData.domainInfo(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=domain
                                        )

        recordList = processData.recordList(
                                        web.cookies().email,
                                        web.cookies().password,
                                        id=domainID
                                        )

        return render.record(domain,recordList)

class Delrecord:
    "删除指定记录并返回相关信息类"
    def GET(sef,domain_recordId):
        string = domain_recordId.encode()
        domain = string.split('-')[0]
        recordId = string.split('-')[1]
        domainId = processData.domainInfo(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=domain
                                        )

        message = processData.delRecord(
                                        web.cookies().email,
                                        web.cookies().password,
                                        did=domainId,
                                        rid=recordId
                                        )        
        if message == '1':
            recordList = processData.recordList(
                                                web.cookies().email,
                                                web.cookies().password,
                                                id=domainId
                                                )
            return render.record(domain,recordList,delMsg='删除成功')
        else:
            recordList = processData.recordList(
                                                web.cookies().email,
                                                web.cookies().password,
                                                id=domainId
                                                )
            return render.record(domain,recordList,delMsg=message)

class AddRecord:
    "给域名添加记录类"
    def POST(self,domain):
        domainId = processData.domainInfo(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=domain
                                        )#获取域名ID
        i = web.input()
        message = processData.addRecord(
                                        web.cookies().email,#邮箱
                                        web.cookies().password,#密码
                                        domain_id=domainId,#域名ID
                                        sub_domain = i.hostrecord.encode(),#主机记录        
                                        record_type = i.recordType.encode(),#记录类型
                                        route_line = i.routeType.encode('utf-8'),#线路类型
                                        value = i.recordValue.encode(),#记录值
                                        mx = i.MX.encode(),#MX值
                                        ttl = i.TTL.encode()#TTL
                                        )        
        if message == '1':
            recordList = processData.recordList(
                                        web.cookies().email,
                                        web.cookies().password,
                                        id=domainId
                                        )
            return render.record(domain,recordList,delMsg='添加成功')
        else:
            recordList = processData.recordList(
                                        web.cookies().email,
                                        web.cookies().password,
                                        id=domainId
                                        )
            return render.record(domain,recordList,delMsg=message)

class UpdateRecord:
    "修改域名的指定记录类"
    def GET(self,domain_recordId):
        string = domain_recordId.encode()
        domain = string.split('-')[0]
        recordId = string.split('-')[1]
        domainId = processData.domainInfo(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=domain
                                        )#获取域名Id
        recordDict = processData.InfoRecord(
                                        web.cookies().email,
                                        web.cookies().password,
                                        did=domainId,
                                        rid=recordId
                                        )
        return render.update(recordDict,domain)

    def POST(self,domain_recordId):
        "保存修改后的记录类"
        string = domain_recordId.encode()
        domain = string.split('-')[0]
        recordId = string.split('-')[1]
        domainId = processData.domainInfo(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=domain
                                        )
        recordDict = processData.InfoRecord(
                                        web.cookies().email,
                                        web.cookies().password,
                                        did=domainId,
                                        rid=recordId
                                        )
        i = web.input()
        message = processData.updateRecord(
                                        web.cookies().email,#邮箱
                                        web.cookies().password,#密码
                                        domain_id=domainId,#域名ID
                                        record_id=recordId,#记录ID
                                        sub_domain = i.hostName.encode(),#主机记录        
                                        record_type = i.recordType.encode(),#记录类型
                                        route_line = i.routeType.encode('utf-8'),#线路类型
                                        value = i.recordValue.encode(),#记录值
                                        mx = i.MX.encode(),#MX值
                                        ttl = i.TTL.encode()#TTL
                                        )        
        if message == '1':
            return render.update(recordDict,domain,msg = "修改成功，点击域名进行查看。")
        else:
            return render.update(recordDict,domain,msg = message)

class Upload:
    "导入对应域名的DNS记录类"
    def GET(self,domain):
        global domain_g 
        domain_g = domain
        return render.upload(domain_g)

    def POST(self,balabala):
        domainId = processData.domainInfo(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=domain_g
                                        )#获取域名ID
        x = web.input(myfile={})
        count = 0
        k = 0
        for line in x['myfile'].file:
            line = line.split('\t')
            count += 1
            if count == 1 or line[3] == 'f1g1ns1.dnspod.net.' or line[3] == 'f1g1ns2.dnspod.net.':
                k += 1   
                continue
            message = processData.addRecord(
                                        web.cookies().email,#邮箱
                                        web.cookies().password,#密码
                                        domain_id=domainId,#域名ID
                                        sub_domain = line[0],#主机记录        
                                        record_type = line[1],#记录类型
                                        route_line = line[2],#线路类型
                                        value = line[3],#记录值
                                        mx = line[4],#MX值
                                        ttl = line[5][:-1]#TTL
                                        )        
        count -= k
        return render.upload(domain_g,msg='成功导入'+str(count)+'条记录，请点击左上角的域名进行查看！')
        
class Loaddns:
    "自动导入对应域名的NDS记录类"
    def GET(self,domain):
        domainId = processData.domainInfo(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=domain_g
                                        )#获取域名ID
        count = 0
        answers = dnsRecord.dnsRecord(domain)
        if not answers:
            return render.upload(domain,ans='没有扫描到任何记录！')
        else:
            for item in answers:
                if item['typename'] == 'NS':
                    message = processData.addRecord(
                                        web.cookies().email,#邮箱
                                        web.cookies().password,#密码
                                        domain_id=domainId,#域名ID
                                        sub_domain = '@',#主机记录        
                                        record_type = item['typename'],#记录类型
                                        route_line = '默认',#线路类型
                                        value = item['data'],#记录值
                                        mx = '',#MX值
                                        ttl = '600'#TTL
                                        )   
                    if message == '1':count += 1
                if item['typename'] == 'A':
                    message = processData.addRecord(
                                        web.cookies().email,#邮箱
                                        web.cookies().password,#密码
                                        domain_id=domainId,#域名ID
                                        sub_domain = 'www',#主机记录        
                                        record_type = item['typename'],#记录类型
                                        route_line = '默认',#线路类型
                                        value = item['data'],#记录值
                                        mx = '',#MX值
                                        ttl = '600'#TTL
                                        )        
                    if message == '1':count += 1
                if item['typename'] == 'MX':
                    message = processData.addRecord(
                                        web.cookies().email,#邮箱
                                        web.cookies().password,#密码
                                        domain_id=domainId,#域名ID
                                        sub_domain = 'mail',#主机记录        
                                        record_type = item['typename'],#记录类型
                                        route_line = '默认',#线路类型
                                        value = item['data'][1]+'.',#记录值
                                        mx = '1',#MX值#不知为什么，mx为空时，发生了mx错误，只好暂时设置为1。
                                        ttl = '600'#TTL
                                        )        
                    if message == '1':count += 1

        return render.upload(domain,ans='成功导入'+
                                    str(count)+
                                    '条记录，点击左上角的域名进行查看。如果有遗漏，请手动添加或上传文件导入。')

class Download:
    "导出对应域名的DNS记录"
    def GET(self,domain):
        domainId = processData.domainInfo(
                                        web.cookies().email,
                                        web.cookies().password,
                                        domain=domain
                                        )#获取域名ID
        
        recordList = processData.recordList(
                                        web.cookies().email,
                                        web.cookies().password,
                                        id=domainId
                                        )#获取记录列表
        fileHead = '主机|类型|线路|记录值|MX优先级|TTL'#导出文件的头部
        s = ''
        s += fileHead + '\n'
        for i in recordList:
            s += i['name'].encode() + '\t'
            s += str(i['type']) + '\t'
            s += i['line'].encode('utf-8') + '\t'
            s += str(i['value']) + '\t'
            s += str(i['mx']) + '\t'
            s += str(i['ttl']) + '\n'
        web.header('Content-Type','static/txt')
        web.header('Content-Disposition',"attachment;filename="+domain+".txt")
        return s

class Signout:
    "退出"
    def GET(self):
        web.setcookie('email','', expires=-1)
        raise web.seeother('/')
#主程序
if __name__ == "__main__":
    app.run()
