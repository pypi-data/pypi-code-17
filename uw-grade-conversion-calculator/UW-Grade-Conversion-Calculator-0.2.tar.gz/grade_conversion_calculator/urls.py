from django.conf.urls import url
from grade_conversion_calculator.views import demo


urlpatterns = [
    url(r'^calculator-demo/?$', demo, name='calculator_demo'),
]
