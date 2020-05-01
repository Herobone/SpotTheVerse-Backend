from LambdaProcessor import Processor
import json

proc = Processor()

@proc.register("/analyse/{id}")
def test1(id):
    print("Test 1")
    print(f"ID is {id}")
    return standard()

@proc.register("/analyse")
def test2():
    print("Test 2")
    return standard()

@proc.register("/")
def test3():
    print("Test 3")
    return standard()

print(proc.REGS)

def standard():
    return json_response({"data": "standard"})

def json_response(data, response_code=200):
    return {
        'statusCode': response_code,
        'body': json.dumps(data),
        'headers': {'Content-Type': 'application/json'}
    }