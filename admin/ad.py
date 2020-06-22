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
        db = pymysql.connect(host='172.17.0.3', port=8004, user='root', passwd='123', db='docker', charset='utf8')
        cursor = db.cursor()
        sql = " select * from user where username = '" + username + "' "
        cursor.execute(sql)
        data = cursor.fetchone()
        self.write(self.get_argument("greeting", "<h2>Docekr</h2>"))

        if data[1] != password or data[2]!="admin" :
            self.write(self.get_argument("greeting", "<h2>您不是管理员或非法访问</h2>"))
            return
            ################

        self.write(self.get_argument("greeting", "<form method='post' action='/user'>"))################

        s = "<h2><input type='radio' name='username' value=" + username + " checked>" + "Welcome " + username +"<input type='radio' name='password' value=" + password + " checked>" + "后台 " + "</h2>"
        self.write(self.get_argument("greeting", s))

        self.write(self.get_argument("greeting", "<h2>存在的镜像</h2>"))  ################
        ss = sshdocker("docker images")
        greeting = self.get_argument("greeting", ss[0].replace(" ", "&nbsp"))
        self.write(greeting)
        ss = ss[1:]
        for line in ss:
            s="<p><input type='radio' name='id' value=" + line.split()[2] + " checked>" + line.replace(" ", "&nbsp") + "</p>"

            greeting = self.get_argument("greeting", s)
            self.write(greeting)
        self.write(self.get_argument("greeting",
                                     "<p>参数:<br><input type='text' name='arg'></p>"))
        self.write(self.get_argument("greeting",
                                     "&nbsp&nbsp<label><input type='radio' name='op' value='rmi'>" + "删除" + "</label>"))
        self.write(self.get_argument("greeting",
                                     "&nbsp&nbsp<label><input type='radio' name='op' value='pull'>" + "下载" + "</label>"))
        self.write(self.get_argument("greeting",
                                     "&nbsp&nbsp<label><input type='radio' name='op' value='run -d -it'>" + "创建容器" + "</label>"))
        # self.write(self.get_argument("greeting",
        #                              "&nbsp&nbsp<label><input type='radio' name='op' value='run -d -it'>" + "运行" + "</label>"))
        self.write(self.get_argument("greeting", "<input type='submit' value='submit'>"))

        with open('/var/www/py/py/data/data.txt', "r") as f:  ##获取所属信息
            data = f.read()
        data=data.split("\n")
        for i in range(len(data)):
            data[i]=data[i].split()

        self.write(self.get_argument("greeting", "<h2>运行过的容器</h2>"))  ################
        ss = sshdocker("docker ps -a")
        greeting = self.get_argument("greeting", ss[0].replace(" ", "&nbsp")+'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp user')
        self.write(greeting)
        ss = ss[1:]
        ######################################
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
        ######################################


        for line in ss:
            s = "<p><input type='radio' name='id' value=" +  line.split()[0]  + ">" + line.replace(" ", "&nbsp") + "</p>"

            greeting = self.get_argument("greeting", s)
            self.write(greeting)
        self.write(self.get_argument("greeting",
                                     "&nbsp&nbsp<label><input type='radio' name='op' value='start'>" + "运行" + "</label>"))
        self.write(self.get_argument("greeting",
                                     "&nbsp&nbsp<label><input type='radio' name='op' value='rm '>" + "删除" + "</label>"))
        self.write(self.get_argument("greeting",
                                     "&nbsp&nbsp<label><input type='radio' name='op' value='logs '>" + "查看日志" + "</label>"))
        self.write(self.get_argument("greeting", "<input type='submit' value='submit'>"))


        self.write(self.get_argument("greeting", "<h2>运行中的容器</h2>"))  ################
        ss = sshdocker("docker ps")
        greeting = self.get_argument("greeting", ss[0].replace(" ", "&nbsp")+'&nbsp&nbsp&nbsp&nbsp user')
        self.write(greeting)
        ss = ss[1:]
        ######################################
        temp = []
        for ss_ in ss:
            for data_ in data:
                if data_ != [] and ss_ != [] and ss_.split()[0][0:10] == data_[0][0:10] :
                    temp.append(ss_ + "     " + data_[1])
                if f == 0 and ss_ != []:
                    temp.append(ss_ + "     " + "unknow")
        ss = temp

        ######################################

        for line in ss:
            s = "<p><input type='radio' name='id' value=" +  line.split()[0]  + ">" + line.replace(" ", "&nbsp") + "</p>"
            greeting = self.get_argument("greeting", s)
            self.write(greeting)
        self.write(self.get_argument("greeting",
                                     "&nbsp&nbsp<label><input type='radio' name='op' value='stop'>" + "停止" + "</label>"))

        self.write(self.get_argument("greeting", "<input type='submit' value='submit'>"))

        self.write(self.get_argument("greeting",
                                     "&nbsp&nbsp<p><input type='radio' name='op' value='top'>" + "高级功能：" + "<input type='text' name='operation'></p>"))
        # self.write(self.get_argument("greeting", "<p>高级功能:<br><input type='text' name='operation'></p>"))
        self.write(self.get_argument("sub", "<input type='submit' value='submit'>"))
        self.write(self.get_argument("greeting", "</form>"))

    client = docker.DockerClient(base_url='tcp://192.168.122.240:2375')


class UserHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        operation = self.get_argument("op")

        id = self.get_argument("id")
        print(id)
        if operation=="pull":
            id=self.get_argument("arg")
        if operation == "run -d -it":
            cmd="docker "+operation+ " " + self.get_argument("arg")+" "+id
        cmd = "docker " + operation + " " + id
        if operation=="top":
            cmd=self.get_argument("operation")
        print(id)
        print(cmd)

        ss=sshdocker(cmd)

        if operation=="run -d -it":
            with open('/var/www/py/py/data/data.txt', "r") as f:  # 设置文件对象
                str = f.read()
            with open('/var/www/py/py/data/data.txt', 'w') as f:  # 设置文件对象
                f.write(str+"\n"+ss[0]+" "+username)
        if operation=="rm":
            with open('/var/www/py/py/data/data.txt', "r") as f:  # 设置文件对象
                data = f.read()
            print(data)
            temp=""
            data = data.split("\n")
            for i in data:
                if i!=[] and i.split()!=[] and i.split()[0][:12]!=id[:12]:
                    temp=temp+i+"\n"
            with open('/var/www/py/py/data/data.txt', 'w') as f:  # 设置文件对象
                f.write(temp)

        self.write(self.get_argument("greeting", "<h2>Docker</h2>"))  ################
        self.write(self.get_argument("greeting", "<h3>运行结果</h3>"))  ################
        for line in ss:
            s = "<p> "+line.replace(' ', '&nbsp') + "</p>"
            greeting = self.get_argument("greeting", s)
            self.write(greeting)

        self.write(self.get_argument("greeting", "<a href='http://10.17.18.101:10046/?username="+username+"&password="+password+"'>返回首页</a>"))



handlers = [
    (r"/", IndexHandler),
    (r"/user", UserHandler)
]
template_path = os.path.join(os.path.dirname(__file__), "template")
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers, template_path)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
