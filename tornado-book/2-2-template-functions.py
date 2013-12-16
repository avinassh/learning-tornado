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

