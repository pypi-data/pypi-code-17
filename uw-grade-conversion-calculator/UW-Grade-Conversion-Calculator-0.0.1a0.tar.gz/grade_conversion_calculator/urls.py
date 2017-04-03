from django.conf.urls import include, url


urlpatterns = [
    url(r'^calculator-demo/?$', 'grade_conversion_calculator.views.demo'),
]
