
#!/bin/python

# Sample POST request : curl http://localhost:8000/wrap -d text=Lorem+ipsum+dolor+sit+amet,+consectetuer+adipiscing+elit
# Output : Lorem ipsum dolor sit amet, consectetuer
# 
# Sample GET request : curl http://localhost:8000/reverse/helbhelb
# Output : blehbleh
#
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
    # /reverse/(\w+)
    # /reverse/string, string is sent as an parameter whenever there is 
    # GET request 
    def get(self, input):
        self.write(input[::-1])

    def write_error(self, status_code, **kwargs):
        self.write("Damn bitch! You caused a %d error." % status_code) 


class WrapHandler(tornado.web.RequestHandler): 
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40) 
        self.write(textwrap.fill(text, width))

    def write_error(self, status_code, **kwargs):
        self.write("Damn bitch! You caused a %d error." % status_code)     


class WrapHandlerWithInput(tornado.web.RequestHandler):
    # This handler is to test whether POST request can also make use of
    # capture group. And when the ulr is /wrap/sometsring the request will
    # be handled by this method. 
    # The content of capture group is sent as parameter to this method
    def post(self, input):
        text = self.get_argument('text')
        width = self.get_argument('width', 40) 
        response = 'You have given this: %s in input group\n\
        and the Output is %s' % (input, textwrap.fill(text, width))
        self.write(response)

    def write_error(self, status_code, **kwargs):
        self.write("Damn bitch! You caused a %d error." % status_code)

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
            (r"/wrap", WrapHandler),
            (r"/wrap/(\w+)", WrapHandlerWithInput)
        ])
    http_server = tornado.httpserver.HTTPServer(app) 
    http_server.listen(options.port) 
    tornado.ioloop.IOLoop.instance().start()