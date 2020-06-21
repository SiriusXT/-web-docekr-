#!/usr/bin/env python
#coding:utf-8
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
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    ssh.connect('192.168.122.240','22','root','docker',timeout=5)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    s='\n'
    for i in stdout.readlines():
        s=s+i
    return s
    #return stdout


def getimages(client):
  images = client.images.list()
  return images
def stopall(clinet):
  for container in client.containers.list():
    container.stop()
def stop(clinet,container):
  container.stop()

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
      ss=ssh("docker images")
      print(ss)
      print("---------------")
      i=0
      ss=ss.split("\n")
      print(ss)
      print("---------------")
      for line in ss():

          if i==0:
              greeting = self.get_argument("greeting", line)
              self.write(greeting)
              continue
          i=i+1
          s="<p><input type='checkbox' name='category' value="+str(i)+"/>"+line+"</p>"
          greeting = self.get_argument("greeting", s)
          self.write(greeting)

    #client = docker.DockerClient(base_url='tcp://192.168.122.240:2375')
    #images=getimages(client)
    #print(images)
    #for i in range(len(images)):
        
            #print("---------"+str(images[i]))
    #ss=ssh("docker images")
    #print(ss)
    #for i in ss.readlines():
        #print (i)
    #for j in ss:
     #   print ("------",i)
      #  s="<p><input type='checkbox' name='category' value="+str(1)+"/>"+i+"</p>"
       # greeting = self.get_argument("greeting", s)
        #self.write(greeting)
    #greeting = self.get_argument('greeting', '<p><input type="checkbox" name="category" value="今日话题" />今日话题 </p> ')
    #self.write(greeting)
 	
    #self.render("index.html",dockerps=client.containers.list(),dockerimages=ssh("docker images"))

class UserHandler(tornado.web.RequestHandler):
  def post(self):
    _operation= self.get_argument("operation")
    print(_operation)
    client = docker.DockerClient(base_url='tcp://192.168.122.240:2375')
    #client = docker.DockerClient(base_url='tcp://192.168.122.242:5555')
    images = client.images.list()
    #self.render("user.html",username=images[0],email=user_email,website=user_website,language=user_language)

    s=''
    for i in images:
        s=s+str(i)+"\n"

    self.render("user.html",username=user_name,dockerpsnum=len(images),dockerps=s)



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
