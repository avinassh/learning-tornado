#!/usr/bin/env python
import os.path

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import pymongo

define("port", default=8000, help="run on the given port", type=int)

# put your mongodb username and password 
# "mongodb://username:password@staff.mongohq.com:someport/mongodb_name"
# following is obtained from https://app.mongohq.com/username/mongo/mongodbname/admin
MONGOHQ_URL = "mongodb://avi:test@paulo.mongohq.com:10065/testme"

# following commands were run to insert in mongodbhq
# >>> conn = pymongo.Connection("mongodb://avi:test@paulo.mongohq.com:10065/testme")
# >>> db = conn.testme
# >>> db.collection_names()
# [u'system.indexes', u'system.users', u'widgets', u'words']
# >>> db.burt
# Collection(Database(Connection('paulo.mongohq.com', 10065), u'testme'), u'burt')
# >>> burt = db.burt
# >>> print burt
# Collection(Database(Connection('paulo.mongohq.com', 10065), u'testme'), u'burt')
# >>> burt.books.insert({ "title":"Programming Collective Intelligence", "subtitle": "Building Smart Web 2.0 Applications", "image":"/static/images/collective_intelligence.gif", "author": "Toby Segaran", "date_added":1310248056, "date_released": "August 2007", "isbn":"978-0-596-52932-1", "description":"<p>[...]</p>"})
# ObjectId('52b03937a760360832e15983')
# >>> burt.books.insert({ "title":"RESTful Web Services", "subtitle": "Web services for the real world", "image":"/static/images/restful_web_services.gif", "author": "Leonard Richardson, Sam Ruby", "date_added":1311148056, "date_released": "May 2007", "isbn":"978-0-596-52926-0", "description":"<p>[...]</p>"})
# ObjectId('52b0398ba760360832e15984')

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/recommended/", RecommendedHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			ui_modules={"Book": BookModule},
			debug=True,
			)
		#conn = pymongo.Connection("localhost", 27017)
		#self.db = conn["bookstore"]
		conn = pymongo.Connection(MONGOHQ_URL)
		self.db = conn["testme"]
		tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):

		self.render(
			"index.html",
			page_title = "Burt's Books | Home",
			header_text = "Welcome to Burt's Books!",
		)

class RecommendedHandler(tornado.web.RequestHandler):
	def get(self):
		coll = self.application.db.burt.books
		books = coll.find()
		self.render(
			"recommended.html",
			page_title = "Burt's Books | Recommended Reading",
			header_text = "Recommended Reading",
			books = books
		)
		
class BookModule(tornado.web.UIModule):
	def render(self, book):
		return self.render_string(
			"modules/book.html", 
			book=book,
		)
	
	def css_files(self):
		return "/static/css/recommended.css"
	
	def javascript_files(self):
		return "/static/js/recommended.js"


def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()
