import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo
from bson import Binary, Code
#from bson.json_util import dumps
from bson import json_util

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

# put your mongodb username and password 
# "mongodb://username:password@staff.mongohq.com:someport/mongodb_name"
# following is obtained from https://app.mongohq.com/username/mongo/mongodbname/admin
MONGOHQ_URL = "mongodb://avi:test@paulo.mongohq.com:10065/testme"

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r"/(\w+)", WordHandler)]
		# pymongo Connection object is instantiated
		# in the __init__ method of the Application object.
		#conn = pymongo.Connection("localhost", 27017)
		#self.db = conn["example"]
		conn = pymongo.Connection(MONGOHQ_URL)
		self.db = conn.testme
		#self.db = conn.testme.words
		tornado.web.Application.__init__(self, handlers, debug=True)

class WordHandler(tornado.web.RequestHandler):
	def get(self, word):
		coll = self.application.db.words
		word_doc = coll.find_one({"word": word})
		#word_doc = self.application.db.find_one({"word": word})
		if word_doc:
			del word_doc["_id"]
			#self.write(json_util.dumps (word_doc))
			self.write(word_doc)
		else:
			self.set_status(404)
			self.write({"error": "word not found"})

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
