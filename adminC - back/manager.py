#!/usr/bin/env python
# coding:utf-8
import os.path
import docker
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
# import pymysql
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

        self.render("index.html"    ,username="1"  ,password="2"  )



class UserHandler(tornado.web.RequestHandler):
    def post(self):
        # Fruit=self.request.arguments['Fruit']
        print("post")
        # # Fruit = self.get_argument("Fruit")
        # print("------------",Fruit)
    def post1(self):
        print("post1")

        # print("------------",Fruit)

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
