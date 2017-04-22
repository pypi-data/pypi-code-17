from . import graph

FB_API_HOST = 'https://graph.facebook.com'


class FBAuthMixin:
    def exchange_token(self, app_id, app_secret, short_lived_token):
        data = graph.fb_exchange_token(
            app_id, app_secret, short_lived_token
        )
        return data['access_token'][0]

    def me(self, access_token, fields=('id', 'name')):
        return graph.api(
            '/me', 'GET', {
                'access_token': access_token,
                'fields': ','.join(fields)
            }
        )


class FBAuthAsyncMixin:
    async def exchange_token(self, app_id, app_secret, short_lived_token):
        data = await graph.fb_exchange_token_async(
            app_id, app_secret, short_lived_token
        )
        return data['access_token'][0]

    async def me(self, access_token, fields=('id', 'name')):
        return await graph.api_async(
            '/me', 'GET', {
                'access_token': access_token,
                'fields': ','.join(fields)
            }
        )
