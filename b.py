import tornado
import tornado.web
import tornado.ioloop
class indexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        #为了博客方便，还是将网页直接写在write里面，这是一个完整的网页，大家可以直接复制出来使用
        self.write('<!DOCTYPE html>\
                    <html lang="en">\
                    <head>\
                        <meta charset="UTF-8">\
                        <title>form</title>\
                    </head>\
                    <body>\
                        <form action="index" method="post">\
                            <input type="text" placeholder="Account" name="account">\
                            <input type="password" placeholder="passwd" name="passwd">\
                            <input type="submit">\
                        </form>\
                    </body>\
                    </html>'
                   )
    def post(self, *args, **kwargs):
        account=self.get_argument('account')
        passwd=self.get_argument('passwd')
        self.write('<h1>welcome '+account+'</h1>')
if __name__ == '__main__':
    app=tornado.web.Application([
        ('/index',indexHandler)
    ]
    )
    app.listen(80)
    tornado.ioloop.IOLoop.instance().start()
