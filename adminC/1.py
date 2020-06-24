#!/usr/bin/env python
# coding:utf-8
import os.path
import docker
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)

import paramiko


def sshdocker(cmd):
    _ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    _ssh.set_missing_host_key_policy(key)
    _ssh.connect('192.168.122.232', '22', 'root', 'docker', timeout=5)
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
        # self.write(self.get_argument("greeting", "<form method='post' action='/user'>"))################

        # self.write(self.get_argument("greeting", "<h2>存在的镜像</h2>"))  ################
        ss = sshdocker("docker images")
        # greeting = self.get_argument("greeting", ss[0].replace(" ", "&nbsp"))
        # self.write(greeting)
        divImages=""
        divImages=divImages+ ss[0].replace(" ", "&nbsp")
        ss = ss[1:]
        for line in ss:
            s="<p><input type='radio' name='id' value=" + line.split()[2] + ">" + line.replace(" ", "&nbsp") + "</p>"
            divImages = divImages +s
            # greeting = self.get_argument("greeting", s)
            # self.write(greeting)
        divImages = divImages +"<p>参数:<br><input type='text' name='pullname'></p>"+"&nbsp&nbsp<label><input type='radio' name='op' value='rmi'>" + "删除" + "</label>"+"&nbsp&nbsp<label><input type='radio' name='op' value='pull'>" + "下载" + "</label>"+"&nbsp&nbsp<label><input type='radio' name='op' value='run -d -it'>" + "创建容器" + "</label>"+"<input type='submit' value='submit'>"
        # self.write(self.get_argument("greeting",
        #                              "<p>参数:<br><input type='text' name='pullname'></p>"))
        # self.write(self.get_argument("greeting",
        #                              "&nbsp&nbsp<label><input type='radio' name='op' value='rmi'>" + "删除" + "</label>"))
        # self.write(self.get_argument("greeting",
        #                              "&nbsp&nbsp<label><input type='radio' name='op' value='pull'>" + "下载" + "</label>"))
        # self.write(self.get_argument("greeting",
        #                              "&nbsp&nbsp<label><input type='radio' name='op' value='run -d -it'>" + "创建容器" + "</label>"))
        # self.write(self.get_argument("greeting",
        #                              "&nbsp&nbsp<label><input type='radio' name='op' value='run -d -it'>" + "运行" + "</label>"))
        # self.write(self.get_argument("greeting", "<input type='submit' value='submit'>"))



        # self.write(self.get_argument("greeting", "<h2>运行过的容器</h2>"))  ################
        ss = sshdocker("docker ps -a")
        divContains=""
        divContains=divContains+ss[0].replace(" ", "&nbsp")
        # greeting = self.get_argument("greeting", ss[0].replace(" ", "&nbsp"))
        # self.write(greeting)
        ss = ss[1:]
        for line in ss:
            s = "<p><input type='radio' name='id' value=" +  line.split()[0]  + ">" + line.replace(" ", "&nbsp") + "</p>"
            divContains = divContains +s
            # greeting = self.get_argument("greeting", s)
            # self.write(greeting)
        divContains = divContains +"&nbsp&nbsp<label><input type='radio' name='op' value='start'>" + "运行" + "</label>"+"&nbsp&nbsp<label><input type='radio' name='op' value='rm '>" + "删除" + "</label>"+"&nbsp&nbsp<label><input type='radio' name='op' value='logs '>" + "查看日志" + "</label>"+"<input type='submit' value='submit'>"
        # self.write(self.get_argument("greeting",
        #                              "&nbsp&nbsp<label><input type='radio' name='op' value='start'>" + "运行" + "</label>"))
        # self.write(self.get_argument("greeting",
        #                              "&nbsp&nbsp<label><input type='radio' name='op' value='rm '>" + "删除" + "</label>"))
        # self.write(self.get_argument("greeting",
        #                              "&nbsp&nbsp<label><input type='radio' name='op' value='logs '>" + "查看日志" + "</label>"))
        # self.write(self.get_argument("greeting", "<input type='submit' value='submit'>"))

        divRun=""

        # self.write(self.get_argument("greeting", "<h2>运行中的容器</h2>"))  ################
        ss = sshdocker("docker ps")
        divRun = divRun +ss[0].replace(" ", "&nbsp")
        # greeting = self.get_argument("greeting", ss[0].replace(" ", "&nbsp"))
        # self.write(greeting)
        ss = ss[1:]
        for line in ss:
            s = "<p><input type='radio' name='id' value=" +  line.split()[0]  + ">" + line.replace(" ", "&nbsp") + "</p>"
            divRun = divRun+s
            # greeting = self.get_argument("greeting", s)
            # self.write(greeting)
        divRun = divRun+"&nbsp&nbsp<label><input type='radio' name='op' value='stop'>" + "停止" + "</label>"+"<input type='submit' value='submit'>"
        # self.write(self.get_argument("greeting",
        #                              "&nbsp&nbsp<label><input type='radio' name='op' value='stop'>" + "停止" + "</label>"))
        #
        # self.write(self.get_argument("greeting", "<input type='submit' value='submit'>"))






        # self.write(self.get_argument("greeting", "<p>下载:<br><input type='text' name='operation'></p>"))
        # self.write(self.get_argument("sub", "<input type='submit' value='submit'>"))
        # self.write(self.get_argument("greeting", "</form>"))
        self.render("index.html",divIntroduction="divIntroduction",divImages=divImages,divContains=divContains,divRun=divRun,divOthers="divOthers")
    client = docker.DockerClient(base_url='tcp://192.168.122.240:2375')


class UserHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        print(username)
        print(password)

        operation = self.get_argument("op")
        id = self.get_argument("id")

        if operation=="pull":
            id=self.get_argument("pullname")

        cmd = "docker " + operation + " " + id
        print(cmd)


        ss=sshdocker(cmd)

        self.write(self.get_argument("greeting", "<h2>Docker</h2>"))  ################
        self.write(self.get_argument("greeting", "<h3>运行结果</h3>"))  ################
        for line in ss:
            s = "<p> "+line.replace(' ', '&nbsp') + "</p>"
            greeting = self.get_argument("greeting", s)
            self.write(greeting)

        self.write(self.get_argument("greeting", "<a href='http://10.17.18.101:10048/'>返回首页</a>"))



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
