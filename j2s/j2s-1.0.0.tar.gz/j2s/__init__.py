import sys
import json

def json_to_swagger(obj):

    type_table = {
        "unicode": "string",
        "str": "string",
        "int": "integer",
        "float": "float",
        "dict": "object",
        "list": "list",
        "NoneType": None,
        "bool": "boolean"
    }

    types = {}

    for key in obj:
        
        if type(obj[key]) is dict:

            types[key] = json_to_swagger(obj[key])

        elif type(obj[key]) is list:

            types[key] = [json_to_swagger(obj[key][0])] if len(obj[key]) > 0 else []

        else:

            types[key] = {
                "type": type_table[type(obj[key]).__name__],
                "example": obj[key]
            }

    return types

def main():
    
    data = json.loads(sys.stdin.read())

    swagger = json_to_swagger(data)

    sys.stdout.write(json.dumps(swagger, indent=2))
