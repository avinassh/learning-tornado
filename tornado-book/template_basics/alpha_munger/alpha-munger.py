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
        self.render('munged.html', source_text=source_text, 
            word_doubler=self.word_doubler)


if __name__ == '__main__': 
    tornado.options.parse_command_line() 
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/poem', MungedPageHandler)], 
        template_path=os.path.join(os.path.dirname(__file__), "templates"), 
        static_path=os.path.join(os.path.dirname(__file__), "static"), 
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

    # Comments with python expressions cannot be added in templates? 
    # Seems so!

    # tornado was trying to excute the follwing line even though it was
    # commented
    # <!--h1>Your text</h1>
    #     <p>
    #         {% for line in change_lines %}
    #             {% for word in line.split(' ') %}
    #                 {% if len(word) > 0 and word[0] in source_map %}
    #                     <span class="replaced"
    #                         title="{{word}}">{{ choice(source_map[word[0]]) }}</span>
    #                 {% else %}
    #                     <span class="unchanged" title="unchanged">{{word}}</span>
    #                 {% end %}
    #             {% end %}
    #         <br>
    #         {% end %}
    #     </p-->

    http_server = tornado.httpserver.HTTPServer(app) 
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()        