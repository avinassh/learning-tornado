import urllib
import json
import datetime
import time

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen

from oauth import oauth

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	# decorator is used to leave the connection open till the callback is
    # executed. 
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		query = self.get_argument('q')
		client = tornado.httpclient.AsyncHTTPClient()
		url = "https://api.twitter.com/1.1/search/tweets.json?" + \
				urllib.urlencode({"q": query, "result_type": "recent", "count": 100})
		# here an object of tornado.gen.Task is created to which the function
		# to be called and the parameters are sent.
		# here yield gives the control back to Tornado so that it can perform
		# other tasks or receive new request while the HTTP request is still
		# in progress
		# When the HTTP request is finished, the RequestHandler method 
		# resumes where it left off
		# There is no performance difference using tornado.gen, it is done for
		# readability of the code		
		response = yield tornado.gen.Task(client.fetch, url, 
				headers={'Authorization': oauth(url)})
		body = json.loads(response.body)
		result_count = len(body['statuses'])
		now = datetime.datetime.utcnow()
		raw_oldest_tweet_at = body['statuses'][-1]['created_at']
		oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
				"%a %b %d %H:%M:%S +0000 %Y")
		seconds_diff = time.mktime(now.timetuple()) - \
				time.mktime(oldest_tweet_at.timetuple())
		tweets_per_second = float(result_count) / seconds_diff
		self.write("""
<div style="text-align: center">
	<div style="font-size: 72px">%s</div>
	<div style="font-size: 144px">%.02f</div>
	<div style="font-size: 24px">tweets per second</div>
</div>""" % (query, tweets_per_second))
		self.finish()

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()