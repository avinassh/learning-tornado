
#!/bin/python

import textwrap

# bunch of tornado imports
import tornado.httpserver 
import tornado.ioloop 
import tornado.options 
import tornado.web


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define("author", default='avi', help="the author of this server", type=str)


class ReverseHandler(tornado.web.RequestHandler):
    # here the input varible is content of capture group
    # /reverse/string, string is sent as an parameter whenever there is 
    # GET request 
    def get(self, input):
        self.write(input[::-1])


class WrapHandler(tornado.web.RequestHandler): 
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40) 
        self.write(textwrap.fill(text, width))


if __name__ == "__main__": 
    tornado.options.parse_command_line()
    # Here regex has a capture group (i.e., a portion of the regex is
    # enclosed in parentheses), the matching contents of that group will be 
    # passed to the RequestHandler object as parameters to the method 
    # corresponding to the HTTP request. 
    # e.g. (\w+)
    # so /reverse/anystring is sent to ReverseHandler 
    app = tornado.web.Application(
        handlers=[
            (r"/reverse/(\w+)", ReverseHandler), 
            (r"/wrap", WrapHandler)
        ])
    http_server = tornado.httpserver.HTTPServer(app) 
    http_server.listen(options.port) 
    tornado.ioloop.IOLoop.instance().start()