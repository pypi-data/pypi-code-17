import web
from urlparse import parse_qs
from facepy import GraphAPI

urls = ('/', 'index')
class index:
    def GET(self):
        app_id = '190191088163549'
        app_secret = '830886c7f6d51dceea255f8b258a339b'
        post_login_url = 'http://0.0.0.0:8080/'
        
        user_data = web.input(code=None)
        
        if not user_data.code:
            dialog_url = ( 'http://www.facebook.com/v2.8/dialog/oauth?' +
                           'client_id=' + app_id +
                           '&redirect_uri=' + post_login_url)
            return '<script>top.location.href="' + dialog_url + '"</script>'
        else:
            graph = GraphAPI()
            response = graph.get(
                path='oauth/access_token',
                client_id=app_id,
                client_secret=app_secret,
                redirect_uri=post_login_url,
                code=user_data.code
            )
            graph = GraphAPI(response['access_token'])
            return graph.get('me/posts')

    def POST(self):
        return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
