#!/usr/bin/env python
#coding:utf-8

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import docker 
from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        client = docker.DockerClient(base_url='tcp://192.168.122.240:2375')
        images = client.images.list()
        s=""
        for item in images:
            s = s + str(item)
        #list=' '.join(images)
        print(s)

        gr = self.get_argument('greeting', s)
        self.write("running:"+gr)
        self.write(greeting + ', welcome you to read: www.hiekay.com')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


