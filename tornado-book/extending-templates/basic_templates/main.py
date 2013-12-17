#!/usr/bin/env python
import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"index.html",
			header_text = "Hi! I am the header",
			footer_text = "the copyright stuff"
		)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", IndexHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			debug=True,
			autoescape=None
			)
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	# an instance of Application is created and sent as an parameter.

	# earlier this was done by following : 
	# app = tornado.web.Application(
 #        handlers=[(r'/', IndexHandler)], 
 #        template_path=os.path.join(os.path.dirname(__file__), "templates"),  
 #        debug=True,
 #        autoescape=None
 #        )
	# http_server = tornado.httpserver.HTTPServer(app)

	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
