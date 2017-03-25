#!/usr/bin/python
# coding=utf-8
import uuid
import hmac
import ujson
import hashlib
import redis

__author__ = "caowanyang"

class SessionData(dict):
    def __init__(self, session_id, hmac_key):
        self.session_id = session_id
        self.hmac_key = hmac_key

class ExceptionHandler(Exception):
    print "Error."

class Session(SessionData):
    def __init__(self, session_manager, request_handler):
        self.session_manager = session_manager
        self.request_handler = request_handler
        try:
            current_session = session_manager.get(request_handler)
        except ExceptionHandler:
            current_session = session_manager.get()
        for key, data in current_session.iteritems():
            self[key] = data
        self.session_id = current_session.session_id
        self.hmac_key = current_session.hmac_key

    def save(self):
        self.session_manager.set(self.request_handler, self)

class SessionManager(object):
    def __init__(self, secret, store_options, session_timeout):
        self.secret = secret
        self.session_timeout = session_timeout
        try:
            self.redis = redis.StrictRedis("localhost", port=6379, db=0)
        except Exception as e:
            print e

    def _fetch(self, session_id):
        try:
            session_data = raw_data = self.redis.get(session_id)
            if raw_data:
                """bind value and set time"""
                self.redis.setex(session_id, self.session_timeout, raw_data)
                session_data = ujson.loads(raw_data)
                if isinstance(session_data, dict):
                    return session_data
                else:
                    return {}
        except IOError:
            return {}

    def _generate_id(self):
        return hashlib.sha256(self.secret + str(uuid.uuid4())).hexdigest()

    def _generate_mac(self, session_id):
        return hmac.new(session_id, self.secret, hashlib.sha256).hexdigest()

    def get(self, request_handle = None):
        session_id = None
        hmac_key = None
        session_exists = False
        if request_handle:
            session_id = request_handle.get_secure_cookie("session_id")
            hmac_key = request_handle.get_secure_cookie("verification")
        if session_id and hmac_key:
            session_exists = True
        else:
            session_id = self._generate_id()
            hmac_key = self._generate_mac(session_id)
        if session_exists:
            session = SessionData(session_id, hmac_key)
            for key , data in self._fetch(session_id).iteritems():
                session[key] = data
            return session

    def set(self, request_handler, session):
        if request_handler and session:
            request_handler.set_secure_cookie("session_id")
            request_handler.set_secure_cookie("verification")
            session_data = ujson.dumps(dict(session.items()))
            self.redis.setex(session.session_id, self.session_timeout, session_data)







