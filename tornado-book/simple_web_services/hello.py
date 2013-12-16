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
        # takes the string parameter and writes it to HTTP response 
        self.write(greeting + ',  dude!')

        #lets print author here
        self.write('You just accessed the server written by: %s' % options.author)

    def write_error(self, status_code, **kwargs):
        self.write("Damn bitch! You caused a %d error." % status_code)    

if __name__ == "__main__":
    tornado.options.parse_command_line()

    # seperate handlers? looks cool

    # app is an instance of Tornado's Application class is created
    # __init__ method of the Application class takes 'handlers' as a 
    # argument to initiate the object
    # It should be a list of tuples, with each tuple containing a 
    # regular expression to match as its first member and a 
    # RequestHandler class as its second member.
    # now the /cool, /cooldude, /coolwhatever gives the 200 status response
    # Tornado treats these regular expressions as though they contain 
    # beginning-of-line and end-of-line anchors 
    # e.g. the string "/" is assumed to mean "^/$" 
    app = tornado.web.Application(handlers=[(r"/", IndexHandler), (r"/cool.*", IndexHandler)]) 
    http_server = tornado.httpserver.HTTPServer(app)

    # listen on options port 
    http_server.listen(options.port)
    # start it 
    # following creates an instance of IOLoop, now program is ready to listen
    # on the given ports
    # app object is nowhere mentioned here, following seems generic line
    # which will be same in all Tornado apps
    tornado.ioloop.IOLoop.instance().start()
    # below thing won't stop
    tornado.ioloop.IOLoop.instance().stop()