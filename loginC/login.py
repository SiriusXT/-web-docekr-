#!/usr/bin/env python
#coding:utf-8
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import pymysql
define("port", default=8005, help="run on the given port", type=int)
class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("index.html")
class UserHandler(tornado.web.RequestHandler):
  def post(self):
    username = self.get_argument("username")
    password = self.get_argument("password")
    print("当前用户：",username,password)
    db = pymysql.connect(host='172.17.0.3', port=8004, user='root', passwd='123', db='docker', charset='utf8')
    cursor = db.cursor()
    sql = " select * from user where username = '" + username + "' "
    cursor.execute(sql)
    data = cursor.fetchone()
    if data[1] != password:
        self.redirect("http://http://10.17.18.101:10045/")
    if data[2] == 'admin':
        s = "?username=" + username + "&password=" + password
        url = '''http://10.17.18.101:10046/''' + s
        self.redirect(url)
    if data[2] == 'user':
        s = "?username=" + username + "&password=" + password
        url='''http://10.17.18.101:10047/''' + s
        self.redirect(url)
handlers = [
  (r"/", IndexHandler),
  (r"/user", UserHandler)
]
template_path = os.path.join(os.path.dirname(__file__),"template")
if __name__ == "__main__":
  tornado.options.parse_command_line()
  app = tornado.web.Application(handlers, template_path)
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()