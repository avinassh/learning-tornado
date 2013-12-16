#! /bin/python

# To study and understand some of the template fucntions
# escaping, JSONing and squeezing
# url : http://www.tornadoweb.org/en/stable/escape.html

import tornado.escape

# tornado.escape.xhtml_escape(value) replaces &, < and > in the input string
# with their corresponding HTML entities

print tornado.escape.xhtml_escape('<This is a test & it runs?>')
# &lt;This is a test &amp; it runs?&gt;

print tornado.escape.xhtml_unescape('&lt;This is a test &amp; it runs?&gt;')
# <This is a test & it runs?>

# tornado.escape.url_escape(value) returns the input in URL-enocoded format
# it internally uses urllib.quote_plus 
# Default plus = True is sent as parameter to represent spaces as + instead 
# of %20 

print tornado.escape.url_escape('http://example.com/test test test')
# http%3A%2F%2Fexample.com%2Ftest+test+test

print tornado.escape.url_escape('http://example.com/test test test', plus=False)
# http%3A//example.com/test%20test%20test

# tornado.escape.url_unescape() is also available with extra parameter plus