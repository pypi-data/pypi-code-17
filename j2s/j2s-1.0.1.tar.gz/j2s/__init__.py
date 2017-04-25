import sys
import json

def json_to_swagger(obj):

    type_table = {
        "unicode": "string",
        "str": "string",
        "int": "integer",
        "float": "float",
        "dict": "object",
        "list": "array",
        "NoneType": None,
        "bool": "boolean"
    }

    types = {}

    for key in obj:
        
        if type(obj[key]) is dict:

            types[key] = {
                "type": "object",
                "properties": json_to_swagger(obj[key])
            }

        elif type(obj[key]) is list:

            types[key] = {
                "type": "array",
            }

            if len(obj[key]) > 0:
                types[key]["items"] = json_to_swagger(obj[key][0])

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
