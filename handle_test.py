# coding=utf-8
from base import BaseHandler

class HelloHandler(BaseHandler):
    def get(self):
        l = []
        hello = self.get_argument('non1')
        world = self.get_argument('non2')
        print self.session
        l.append(hello)
        l.append(world)
        l.append(self.session['first_session'])
        self.render("/templates/hello.html", page_object = 1)


class HandlerTest(BaseHandler):
    def get(self):
        test = self.get_argument('test', "")
        self.session['first_session'] = "This is a test."
        self.session.save()
        self.finish()