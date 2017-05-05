from django.conf.urls import url
from schema import schema

from .views import (
    ApiGraphQLView,
)


urlpatterns = [
    url(r'^graphql', ApiGraphQLView.as_view(graphiql=True, schema=schema)),
]
