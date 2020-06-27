#!/usr/bin/env python
# coding:utf-8
import os.path
import docker
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import pymysql
define("port", default=8006, help="run on the given port", type=int)

import paramiko


def sshdocker(cmd):
    print("--run--： ",cmd)
    _ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    _ssh.set_missing_host_key_policy(key)
    _ssh.connect('192.168.122.240', '22', 'root', 'docker', timeout=5)
    stdin, stdout, stderr = _ssh.exec_command(cmd)
    ss = ''
    for i in stdout.readlines():
        print("__stdout.readlines():__",i)
        ss = ss + i
    ss = ss.split("\n")
    ss = ss[:-1]
    _ssh.close()
    return ss


def getimages(client):
    images = client.images.list()
    return images


def stopall(clinet):
    for container in clinet.containers.list():
        container.stop()


def stop(clinet, container):
    container.stop()


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        result= self.get_argument("result")
        client = docker.DockerClient(base_url='tcp://192.168.122.240:2375')##############
        divIntroduction=""
        s = "<h2><input type='radio' name='username' value=" + username + " checked>" + " " + username +"<input type='radio' name='password' value=" + password + " checked>" + "后台 " + "</h2>"
        divIntroduction=divIntroduction+s
        db = pymysql.connect(host='172.17.0.3', port=8004, user='root', passwd='123', db='docker', charset='utf8')
        cursor = db.cursor()
        sql = " select * from user where username = '" + username + "' "
        userCount=cursor.execute(sql)
        data = cursor.fetchone()
        cursor.close()
        # self.write(self.get_argument("greeting", "<h2>Docekr</h2>"))
        usertype=data[2]
        if data[1] != password or data[2]!="admin" :
            self.write(self.get_argument("greeting", "<h2>您不是管理员或非法访问</h2>"))
            return
        divImages = ""
        ss = sshdocker("docker images")
        for i in range(len(ss)):
            ss[i]=ss[i].replace("IMAGE ID","IMAGEID")
            ss[i]=ss[i].split()
        divImages= divImages +"<table class='cssImages'>"
        for i in range(len(ss)):
            divImages = divImages +"<tr>"
            #divImages = divImages+"<th><input type='radio' name='id' value="+ss[i][2]+" checked></th>"
            divImages = divImages + "<th><input type='radio' name='id' value=" + ss[i][0]+":"+ss[i][1] + " checked></th>"
            for j in range(len(ss[0])):
                if i==0:
                    divImages = divImages + "<th>"
                    divImages = divImages + ss[i][j]
                    divImages = divImages + "</th>"
                    continue
                divImages = divImages +"<td>"
                divImages = divImages + ss[i][j]
                divImages = divImages + "</td>"
            divImages = divImages + "</tr>"
        divImages = divImages +"</table>"



        divImages = divImages +"<br>参数:<br><input type='text' name='arg'>"
        divImages = divImages +"&nbsp&nbsp<label><input type='radio' name='op' value='rmi -f '>" + "删除" + "</label>"
        divImages = divImages +"&nbsp&nbsp<label><input type='radio' name='op' value='pull'>" + "下载" + "</label>"
        divImages = divImages +"&nbsp&nbsp<label><input type='radio' name='op' value='run -d -it'>" + "创建容器" + "</label>"
        divImages = divImages +"<p><input type='submit' value='submit'></p>"

        # with open('/var/www/py/py/data/data.txt', "r") as f:  ##获取所属信息
        #     data = f.read()
        # data=data.split("\n")
        data=[]
        cursor = db.cursor()
        sql = " select * from containers where username  = '" + username + "' "
        count=cursor.execute(sql)
        for i in range(count):
            data.append(i)
        cursor.close()

        # for i in range(len(data)):
        #     data[i]=data[i].split()
        divContains = ""
        divContains=divContains+"<table class='cssContains'>"
        ss = sshdocker("docker ps -a")

        divContains = divContains + "<tr>"
        divContains+="<th><input type='radio' name='id' value=" +  "CONTAINERID"  + "></th>"
        temp=ss[0].replace("CONTAINER ID","CONTAINERID").split()
        for i in temp:
            divContains +="<th>"+i+"</th>"
        divContains = divContains +"<th>user</th>"
        divContains = divContains + "</tr>"
        # divContains = divContains + ss[0].replace(" ", "&nbsp")+'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp user'
        ss = ss[1:]

        temp = []
        for ss_ in ss:
            f=0
            for data_ in data:
                if data_ != [] and ss_ != [] and ss_.split()[0][0:10]==data_[0][0:10] :
                    temp.append(ss_+"     "+data_[1])
                    f=1
            if f==0 and ss_ != []  :
                    temp.append(ss_+"     "+"unknow")
        ss = temp
        for i in  range(len(ss)):
            ss[i]=ss[i].replace("  ","##").replace(" ","_").replace("#"," ").replace(" _","  ").replace("_ ","  ")
            print("++",ss[i])
            ss[i]=ss[i].split()
            if len(ss[i])==7:#没有port
                ss[i].insert(5,"noport")
        for i in range(len(ss)):
            divContains = divContains +"<tr>"
            divContains = divContains + "<th><input type='radio' name='id' value=" + ss[i][0] + " checked></th>"
            for j in range(len(ss[i])):
                divContains = divContains + "<td>"
                divContains = divContains + ss[i][j]
                divContains = divContains + "</td>"
            divContains = divContains + "</tr>"
        divContains = divContains +"</table>"
        divContains = divContains +"<br>&nbsp&nbsp<label><input type='radio' name='op' value='start'>" + "运行" + "</label>"
        divContains = divContains +"&nbsp&nbsp<label><input type='radio' name='op' value='rm'>" + "删除" + "</label>"
        divContains = divContains +"&nbsp&nbsp<label><input type='radio' name='op' value='logs'>" + "查看日志" + "</label>"

        divContains = divContains +"<p><input type='submit' value='submit'></p>"

        divRun = ""
        divRun+="<table class='cssRun'>"
        divRun+="<tr>"
        divRun+="<th><input type='radio' name='id' value=" +  "CONTAINERID"  + "></th>"
        ss = sshdocker("docker ps")

        temp = ss[0].split()
        for i in temp:
            divRun += "<th>" + i + "</th>"
        divRun = divRun + "</tr>"

        ss = ss[1:]
        ######################################
        temp = []
        for ss_ in ss:
            f = 0
            for data_ in data:
                if data_ != [] and ss_ != [] and ss_.split()[0][0:10] == data_[0][0:10]:
                    temp.append(ss_ + "     " + data_[1])
                    f = 1
            if f == 0 and ss_ != []:
                temp.append(ss_ + "     " + "unknow")
        ss = temp
        ######################################
        for i in  range(len(ss)):
            ss[i]=ss[i].replace("  ","##").replace(" ","_").replace("#"," ").replace(" _","  ").replace("_ ","  ")
            ss[i]=ss[i].split()
            if len(ss[i])==7:#没有port
                ss[i].insert(5,"noport")
        for i in range(len(ss)):
            divRun = divRun +"<tr>"
            divRun = divRun + "<th><input type='radio' name='id' value=" + ss[i][0] + " checked></th>"
            for j in range(len(ss[i])):
                divRun = divRun + "<td>"
                divRun = divRun + ss[i][j]
                divRun = divRun + "</td>"
            divRun = divRun + "</tr>"
        divRun = divRun +"</table>"

        divRun = divRun +"<br>&nbsp&nbsp<label><input type='radio' name='op' value='stop'>" + "停止" + "</label>"
        divRun = divRun + "&nbsp&nbsp<label><input type='radio' name='op' value='stopall'>" + "停止所有" + "</label>"
        divRun = divRun +"<input type='submit' value='submit'>"

        divOthers=""
        divOthers = divOthers + "&nbsp&nbsp<p><input type='radio' name='op' value='top'>" + "高级功能：" + "<input type='text' name='operation'></p>"
        divOthers = divOthers + "<p><input type='submit' value='submit'></p>"
        result=result.split("$$")
        resultresult=""
        for line in result:
            resultresult+="<p>"+line+"</p>"
        db.close()############################################################
        self.render("index.html", divIntroduction=divIntroduction, divImages=divImages, divContains=divContains,
                divRun=divRun, divOthers=divOthers,username=username,password=password,dockerV=sshdocker("docker -v")[0],usertype=usertype,result=resultresult,
                imagesNum=len(getimages(client)),
        )



class UserHandler(tornado.web.RequestHandler):
    def post(self):
        db = pymysql.connect(host='172.17.0.3', port=8004, user='root', passwd='123', db='docker', charset='utf8')
        username = self.get_argument("username")
        password = self.get_argument("password")
        operation = self.get_argument("op")
        client = docker.DockerClient(base_url='tcp://192.168.122.240:2375')  ##############

        id = self.get_argument("id")
        print(id)

        if operation=="pull":
            id=self.get_argument("arg")
        cmd = "docker " + operation + " " + id
        if operation == "run -d -it":
            cmd="docker "+operation+ " " + self.get_argument("arg")+" "+id

        if operation=="top":
            cmd=self.get_argument("operation")
        print(id)


        ss=sshdocker(cmd)
        if operation=="stopall":
            stopall(client)
            ss=["OK"]

        if operation=="run -d -it":
            # with open('/var/www/py/py/data/data.txt', "r") as f:  # 设置文件对象
            #     str = f.read()
            # with open('/var/www/py/py/data/data.txt', 'w') as f:  # 设置文件对象
            #     f.write(str+"\n"+ss[0]+" "+username)
            data = []
            cursor = db.cursor()
            # sql = " select * from containers where username  = '" + username + "' "
            sql = """INSERT INTO containers(id,
                     username , ip)
                     VALUES ("""+ss[0][0:12]+""", """+username+""", "1")"""
            cursor.execute(sql)
            db.commit()
            cursor.close()


        if operation=="rm":
            # with open('/var/www/py/py/data/data.txt', "r") as f:  # 设置文件对象
            #     data = f.read()
            # print(data)
            # temp=""
            # data = data.split("\n")
            # for i in data:
            #     if i!=[] and i.split()!=[] and i.split()[0][:12]!=id[:12]:
            #         temp=temp+i+"\n"
            # with open('/var/www/py/py/data/data.txt', 'w') as f:  # 设置文件对象
            #     f.write(temp)
            cursor = db.cursor()
            sql = "DELETE FROM containers WHERE id = " +id[:12]
            cursor.execute(sql)
            db.commit()
            cursor.close()


        # self.write(self.get_argument("greeting", "<h2>Docker</h2>"))  ################
        # self.write(self.get_argument("greeting", "<h3>运行结果</h3>"))  ################
        # result=""
        # for line in ss:
        #     s = "<p> "+line.replace(' ', '&nbsp') + "</p>"
        #     # greeting = self.get_argument("greeting", s)
        #     # self.write(greeting)
        #     result+=s
        ss="$$".join(ss)
        url="http://10.17.18.101:10046/?username="+username+"&password="+password+"&result="+ss
        self.redirect(url)
        # self.write(self.get_argument("greeting", "<a href='http://10.17.18.101:10046/?username="+username+"&password="+password+"'>返回首页</a>"))



handlers = [
    (r"/", IndexHandler),
    (r"/user", UserHandler)
]
template_path = os.path.join(os.path.dirname(__file__), "template")
if __name__ == "__main__":
    settings = {
        "autoescape": None
    }
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers, template_path,**settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
