#!/usr/bin/python

import tornado.web
import session

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **kwargs):
        super(BaseHandler, self).__init__(*argc, **kwargs)
        self.session = session.Session(self.application.session_manager, self)


