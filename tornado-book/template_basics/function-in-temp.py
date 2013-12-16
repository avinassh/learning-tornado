#! /bin/python

# to use any function in a template, just send it as a parameter. Thats all!

from tornado.template import Template

def laugh(ha):
    return 5 * ha

print Template("Why so serious? {{laugh('ha')}}").generate(laugh=laugh)
# Why so serious? hahahahaha

#print Template("Why so serious? {{l('ha')}}").generate(l=laugh)