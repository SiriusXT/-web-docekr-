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


def ssh(cmd):
    _ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    _ssh.set_missing_host_key_policy(key)
    _ssh.connect('192.168.122.240', '22', 'root', 'docker', timeout=5)
    stdin, stdout, stderr = _ssh.exec_command(cmd)
    ss = ''
    for i in stdout.readlines():
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
        self.write(self.get_argument("greeting", "<form method='post' action='/user'>"))################

        self.write(self.get_argument("greeting", "<h2>docker images</h2>"))  ################
        ss = ssh("docker images")
        print(ss)
        greeting = self.get_argument("greeting", ss[0].replace(" ", "&nbsp"))
        self.write(greeting)
        ss = ss[1:]
        for line in ss:
            print("---", line)
            s="<p><input type='radio' name='images' value=" + line.split()[2] + ">" + line.replace(" ", "&nbsp") + "</p>"

            greeting = self.get_argument("greeting", s)
            self.write(greeting)
        self.write(self.get_argument("greeting",
                                     "<label><input type='radio' name='imagesOperation' value='del'>" + "删除" + "</label>"))
        self.write(self.get_argument("greeting",
                                     "<label><input type='radio' name='imagesOperation' value='download'>" + "下载" + "</label>"))
        self.write(self.get_argument("sub", "<input type='submit' value='images'>"))



        self.write(self.get_argument("greeting", "<h2>docker ps -a</h2>"))  ################
        ss = ssh("docker ps -a")
        print(ss)
        greeting = self.get_argument("greeting", ss[0].replace(" ", "&nbsp"))
        self.write(greeting)
        ss = ss[1:]
        for line in ss:
            print("---", line)
            s = "<p><input type='radio' name='containers' value=" +  line.split()[0]  + ">" + line.replace(" ", "&nbsp") + "</p>"

            greeting = self.get_argument("greeting", s)
            self.write(greeting)
        self.write(self.get_argument("greeting",
                                     "<label><input type='radio' name='containersOperation' value='start'>" + "运行" + "</label>"))
        self.write(self.get_argument("greeting",
                                     "<label><input type='radio' name='containersOperation' value='del'>" + "删除" + "</label>"))
        self.write(self.get_argument("sub", "<input type='submit' value='containers'>"))


        self.write(self.get_argument("greeting", "<h2>docker ps</h2>"))  ################
        ss = ssh("docker ps")
        print(ss)
        greeting = self.get_argument("greeting", ss[0].replace(" ", "&nbsp"))
        self.write(greeting)
        ss = ss[1:]
        for line in ss:
            print("---", line)
            s = "<p><input type='radio' name='containers' value=" +  line.split()[0]  + ">" + line.replace(" ", "&nbsp") + "</p>"

            greeting = self.get_argument("greeting", s)
            self.write(greeting)
        self.write(self.get_argument("greeting",
                                     "<label><input type='radio' name='containersOperation' value='stop'>" + "停止" + "</label>"))

        self.write(self.get_argument("sub", "<input type='submit' value='containers'>"))






        self.write(self.get_argument("greeting", "<p>下载:<br><input type='text' name='operation'></p>"))
        self.write(self.get_argument("sub", "<input type='submit' value='submit'>"))
        self.write(self.get_argument("greeting", "</form>"))



    # client = docker.DockerClient(base_url='tcp://192.168.122.240:2375')
    # images=getimages(client)
    # print(images)
    # for i in range(len(images)):

    # print("---------"+str(images[i]))
    # ss=ssh("docker images")
    # print(ss)
    # for i in ss.readlines():
    # print (i)
    # for j in ss:
    #   print ("------",i)
    #  s="<p><input type='checkbox' name='category' value="+str(1)+"/>"+i+"</p>"
    # greeting = self.get_argument("greeting", s)
    # self.write(greeting)
    # greeting = self.get_argument('greeting', '<p><input type="checkbox" name="category" value="今日话题" />今日话题 </p> ')
    # self.write(greeting)

    # self.render("index.html",dockerps=client.containers.list(),dockerimages=ssh("docker images"))


class UserHandler(tornado.web.RequestHandler):
    def post(self):
        _operation = self.get_argument("submit")
        if _operation=="images":

        _operation = self.get_argument("images")
        print(_operation)
        # for i in range(4):
        #     _operation = self.get_argument(str(i))
        #     print(_operation)

        self.render("user.html",  result=_operation)


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
