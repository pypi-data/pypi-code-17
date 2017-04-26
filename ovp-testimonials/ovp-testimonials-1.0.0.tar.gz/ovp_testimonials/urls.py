from django.conf.urls import url, include
from rest_framework import routers
from ovp_testimonials import views


testimonials = routers.SimpleRouter()
testimonials.register(r'testimonials', views.TestimonialResource, 'testimonial')

urlpatterns = [
  url(r'^testimonials/', include(testimonials.urls)),
]
