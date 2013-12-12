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

class IndexHandler(tornado.web.RequestHandler): 
    def get(self):
        # get_argument seems a dictionary and it tries to get 
        # value for key 'greeting' ?
        greeting = self.get_argument('greeting', 'Hola!')

        # No self.wfile.write, then how about self.rfile ? 
        self.write(greeting + ',  dude!')

        #lets print author here
        self.write('You just accessed the server written by: ', options.author)

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