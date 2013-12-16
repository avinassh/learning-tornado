#! /bin/python

# To understand how templating is done with Tornado. You can specify a folder
# where all templates/html files are store and ask tornado do render them
#
#

# os.path library is used to specify where to look for templates
import os.path

# bunch of tornado imports
import tornado.httpserver 
import tornado.ioloop 
import tornado.options 
import tornado.web

# to have global port variable, accesible under options.port
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


# This is index file handler. Here the render functions displays the HTML
# 2-1-index.html on the browser when GET request is made on root
# GET on http://localhost:8000/
class IndexHandler(tornado.web.RequestHandler): 
    def get(self):
        self.render('2-1-index.html')


# This is to handle POST
# In the GET request, index page with a form is rendered on the browser.
# When user fills it and submits, this handler will handle that POST request
# i.e. the POST request is sent from index.html page
# The values in the POST request can be accessed by get_argument friendly 
# function which is provided by tornado.web.RequestHandler
class PoemPageHandler(tornado.web.RequestHandler): 
    def post(self):
        # use get_argument to get values by name
        # i.e. in the form whose name is 'noun1' is returned when get_argument
        # is called and stored in noun1 variable 
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        # render function takes the html to render and also the arguments
        # to replace the placeholders in the template
        self.render('2-1-poem.html', roads=noun1, wood=noun2, made=verb,
            difference=noun3)

# It seems the render function makes of generate function internally
# generate module is present within Template class
# here is one fine example :
# 
# >>> from tornado.template import Template
# >>> content = Template("<html><body><h1>{{ header }}</h1></body></html>") 
# >>> print content.generate(header="Welcome!") 
# <html><body><h1>Welcome!</h1></body></html>

# Interestingly, we can put Python expressions within these placeholders
# the tornado will evaluate and render it on browser. We can also use control
# statements like if, for, while, and try. sweet.
#
# >>> from tornado.template import Template
# >>> print Template("{{ 1+1 }}").generate()
# 2

# e.g. use of control statements in templates.
# if 'books' is a list, then below template will create a HTML list and 
# the list contents will be list items
#
# <ul>
#   {% for book in books %}
#       <li>{{ book }}</li> 
#    {% end %}
# </ul>
#
# caller: 
# self.render( "book.html", books=[ "Learning Python",
# "Programming Collective Intelligence", "Restful Web Services" ] )
#
# Output:
# <ul>
# <li>Learning Python</li>
# <li>Programming Collective Intelligence</li> 
# <li>Restful Web Services</li>
# </ul>

# In Tornado there are no restrictions about what expressions you can 
# run within within if and for blocks. So you can run full python code within
# this.

# whoa even you can run {% set foo = 'bar' %} in control blocks


if __name__ == '__main__':
    # to parse command line 
    tornado.options.parse_command_line()
    # Instantiate the app object 
    # it has a handler and also template_path
    # handler specifies the methods to call when requests are made on 
    # / and /poem
    # template_path specifies where to look for templates 
    # render function makes use of template_path
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler),(r'/poem', PoemPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "2-1-templates"))
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()