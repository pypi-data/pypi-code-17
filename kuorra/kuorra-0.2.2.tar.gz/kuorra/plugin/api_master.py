import web
import config
import json

class Api_table_name:
    #http://api_table_name?user_hash=12345
    def GET(self):
        user_data = web.input()
        user_hash = user_data.user_hash
        if user_hash == '12345': #user_hash
            result = config.model.get_all_table_name()
            table_name_json = []
            for row in result:
                t= dict(row)
                table_name_json.append(t)
            web.header('Content-Type', 'application/json')
        else:
            raise web.seeother('/404')
        return json.dumps(table_name_json)
    
    #http://api_table_name?user_hash=12345&primary_key=1
    def POST(self):
        user_data = web.input()
        user_hash = user_data.user_hash
        primary_key = user_data.primary_key

        print user_hash
        print primary_key
        if user_hash == '12345': #user_hash
            try:
                result = config.model.get_product(int(primary_key))
                print result
                table_name_json = []
                table_name_json.append(dict(result))
            except:
                table_name_json = '{}'
        else:
            raise web.seeother('/404')
        return json.dumps(table_name_json)
