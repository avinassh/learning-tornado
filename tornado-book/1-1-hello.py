#!/bin/python

# bunch of tornado imports
import tornado.httpserver 
import tornado.ioloop 
import tornado.options 
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
# how define takes port input from command line?

# tornado.options parses the inputs 

# the options within define are available as global when it is same as
# one of command line arugment, here it is 'port'. cool.

#let me define one more global
define("author", default='avi', help="the author of this server", type=str)

# type specifies what kind of type of argument it should be
# and it converts it to according to that
# eg. --author = 5 will be converted to str(5)
# eg. --port = abc will throw an error becuse of int(abc)

class IndexHandler(tornado.web.RequestHandler): 
    def get(self):
        # get_argument seems a dictionary and it tries to get 
        # value for key 'greeting' ?
        # it may not be a dictionary, but it sure gets the value of
        # 'greeting' from query string
        # eg. http://localhost:8089/?greeting=Hello
        # if no argument given, then second argument is considered
        # here it is 'Hola!' 
        greeting = self.get_argument('greeting', 'Hola!')

        # No self.wfile.write, then how about self.rfile ? 
        self.write(greeting + ',  dude!')

        #lets print author here
        self.write('You just accessed the server written by: %s' % options.author)

if __name__ == "__main__":
    tornado.options.parse_command_line()

    # seperate handlers? looks cool
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)]) 
    http_server = tornado.httpserver.HTTPServer(app)

    # listen on options port 
    http_server.listen(options.port)
    # start it 
    tornado.ioloop.IOLoop.instance().start()
    # below thing won't stop
    tornado.ioloop.IOLoop.instance().stop()