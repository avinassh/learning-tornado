import os.path 
import random

import tornado.httpserver 
import tornado.ioloop 
import tornado.options 
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler): 
    def get(self):
        self.render('index.html')


class MungedPageHandler(tornado.web.RequestHandler): 
    def word_doubler(self, text):
        doubled_words = ''
        for word in text.split():
            doubled_words += 2 * word + ' '
        return doubled_words    


    def post(self):
        source_text = self.get_argument('source')
        #doubled_words = self.word_doubler(source_text)
        self.render('munged.html', source_text=source_text, word_doubler=self.word_doubler)
        #    doubled_words=doubled_words)


if __name__ == '__main__': 
    tornado.options.parse_command_line() 
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/poem', MungedPageHandler)], 
        template_path=os.path.join(os.path.dirname(__file__), "2-4-templates"), 
        static_path=os.path.join(os.path.dirname(__file__), "2-4-static"), 
        debug=True
        )
    # debug mode invokes tornado.autoreload, where tornado will restart the 
    # server for each time main python file is changed and refreshes the 
    # templates as they change

    # static_path can be sent as a paramter to Application class which 
    # specifies the path from where Tornado will serve static files.
    
    # Tornado also provides a module static_url to generate URLs. It is used 
    # in templates.
    # e.g. <link rel="stylesheet" href="{{ static_url("style.css") }}">
    # is converted to something like :
    # <link rel="stylesheet" href="/static/style.css?v=ab12">

    http_server = tornado.httpserver.HTTPServer(app) 
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()        