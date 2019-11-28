import json


class Message(object):

    def __init__(self, code, msg, obj=None):
        self.code = code
        self.msg = msg
        self.obj = obj


class Response(object):

    @classmethod
    def success(cls, code, msg, obj=None):
        return json.dumps(Message(code, msg, obj), default=lambda obj: obj.__dict__)

    @classmethod
    def fail(cls, code, msg):
        return json.dumps(Message(code, msg), default=lambda obj: obj.__dict__)
