dnspod
======

DNSPod第三方python web客户端<br>
此版本在ubuntu12.04下开发， 运用python2.7和web.py进行构建，调用DNSPod官方API实现域名和记录的增删改查.<br>
使用时取保安装了python2.7 和 web.py， dnspod.py是主文件，执行python dnspod.py即可进入主界面.<br>
界面对浏览器的兼容做的不好，最好用chrome打开测试。<br>
<br>
4月8号更新
=
进一步完善了域名和记录的增删改查功能，同时添加了域名记录的导入、导出功能。<br>
导入功能介绍：<br>
可以用两种方法导入：1、自动扫描导入；2、上传文件导入。<br>
实现自动扫描导入需要导入PyDNS第三方python DNS查询包，由于个人能力问题做的程序只能扫描到‘A’和‘MX’记录类型的DNS记录。<br>
上传文件导入，只需要按照提示给出的文件格式上传相应的TXT文件即可。<br>
<br>
导出功能介绍：<br>
只要点击页面上的导出按钮，就可以把对应的域名的所有记录以TXT的文件格式下载到本地。<br>
