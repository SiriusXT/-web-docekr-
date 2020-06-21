#!/usr/bin/env python
# coding:utf-8
import os.path
import docker
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=8889, help="run on the given port", type=int)

import paramiko

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_argument('user')
        print(user)
        self.write(self.get_argument("greeting", "<form method='post' action='/user'>"))  ################
        self.write(self.get_argument("greeting", "<h2>Docker</h2>"))  ################
        self.write(self.get_argument("submit", "<input type='submit' value='submit'>"))
        self.write(self.get_argument("greeting", "</form>"))


class UserHandler(tornado.web.RequestHandler):
    def post(self):
        self.write(self.get_argument("greeting", "<h3>运行结果</h3>"))  ################



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
