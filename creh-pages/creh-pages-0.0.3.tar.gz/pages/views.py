from braces.views import SuperuserRequiredMixin
from graphene_django.views import GraphQLView


class ApiGraphQLView(SuperuserRequiredMixin, GraphQLView):
    pass