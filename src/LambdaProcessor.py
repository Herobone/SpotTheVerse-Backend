class Processor:
    def __init__(self):
        self.REGS = dict()
        pass

    def __call__(self, event, context):
        if event["resource"] in self.REGS:
            func = self.REGS[event["resource"]]
            if event["pathParameters"] != None:
                return func(**event["pathParameters"])
            else:
                return func()

    def register(self, additional):

        def decorator(f):
            self.REGS[additional] = f
            return f
        
        return decorator