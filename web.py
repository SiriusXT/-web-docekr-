import tornado.web
import tornado.ioloop
from tornado.options import define, options
define('port', default=80, help='run on give the give port', type=int)
 
class MainHandler(tornado.web.RequestHandler):
  def get(self, *args, **kwargs):
    personinfodict = {
      'name': 'Jason',
      'age': 20,
      'gender': 'male',
    }
    itemlist = ['name', 'age', 'gender']
    self.render('personinfo.html', itemlist=itemlist, personinfodict=personinfodict, welcome='hello guy!')
 
app = tornado.web.Application([
  (r'/', MainHandler)
])
 
if __name__ == '__main__':
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
