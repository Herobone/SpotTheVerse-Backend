import Util
import json

class Request:
    def __init__(self, event):
        self.headers = event["headers"]
        self.method = event["httpMethod"]
        self.isBase64 = event["isBase64Encoded"]
        self.getParams = event["queryStringParameters"]
        self.path = event["path"]
        self.pathParams = event["pathParameters"]
        self.json = json.loads(event["body"])

class Processor:
    def __init__(self):
        self.REGS = dict()

    def __call__(self, event, context):
        request = Request(event)
        
        if event["resource"] in self.REGS:
            func = self.REGS[event["resource"]]
            if event["pathParameters"] != None:
                return func(request, **event["pathParameters"])
            else:
                return func(request)
    

    def register(self, additional):

        def decorator(f):
            self.REGS[additional] = f
            return f
        
        return decorator