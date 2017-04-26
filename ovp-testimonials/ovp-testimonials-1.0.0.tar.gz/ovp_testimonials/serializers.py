from ovp_testimonials import models
from ovp_users.serializers import ShortUserPublicRetrieveSerializer
from rest_framework import serializers

class TestimonialCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Testimonial
    fields = ["content", "rating", "user", "created_date"]
    read_only_fields = ["created_date"]

class TestimonialRetrieveSerializer(serializers.ModelSerializer):
  user = ShortUserPublicRetrieveSerializer

  class Meta:
    model = models.Testimonial
    fields = ["content", "rating", "user", "created_date"]
