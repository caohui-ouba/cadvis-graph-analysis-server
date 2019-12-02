import json


class State(object):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


SUCCESS = State(0, "success")
FAILED = State(1, "failed")


class Message(object):

    def __init__(self, code, msg, obj=None):
        self.code = code
        self.msg = msg
        self.obj = obj


class Response(object):

    @classmethod
    def success(cls, obj=None):
        return json.dumps(Message(SUCCESS.code, SUCCESS.msg, obj), default=lambda obj: obj.__dict__)

    @classmethod
    def fail(cls, code=FAILED.code, msg=FAILED.msg):
        return json.dumps(Message(code, msg), default=lambda obj: obj.__dict__)
