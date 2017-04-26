from django.test import TestCase
from django.test.utils import override_settings

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp_users.models import User
from ovp_users.models.profile import get_profile_model

from ovp_testimonials.models import Testimonial

import json



"""
Helpers
"""
def create_sample_users():
  user1 = User(name="user one", email="testmail1@test.com", password="test_returned")
  user1.save()

  UserProfile = get_profile_model()
  profile1 = UserProfile(user=user1, full_name="user one", about="about one")
  profile1.save()

  return user1

"""
Tests
"""
class TestimonialTestCase(TestCase):
  data = {
      "content": "body content",
      "rating": 8.5
      }
  def setUp(self):
    self.user = create_sample_users()
    self.client = APIClient()

  def test_can_create_testimonial(self):
    """ Assert it's possible to POST to testimonial resource """
    self.client.force_authenticate(user=self.user)

    response = self.client.post(reverse("testimonial-list"), data=self.data, format="json")
    self.assertTrue(response.status_code == 201)
    self.assertTrue(response.data["content"] == self.data["content"])
    self.assertTrue(response.data["rating"] == self.data["rating"])

  def test_testimonial_creation_requires_authentication_by_default(self):
    """ Assert testimonial creation requires authentication """
    response = self.client.post(reverse("testimonial-list"), data=self.data, format="json")
    self.assertTrue(response.status_code == 401)

  @override_settings(OVP_TESTIMONIALS={"CAN_CREATE_TESTIMONIAL_UNAUTHENTICATED": True})
  def test_can_create_unauthenticated_testimonial(self):
    """ Assert can create testimonial unauthenticated if configured """
    response = self.client.post(reverse("testimonial-list"), data=self.data, format="json")
    self.assertTrue(response.status_code == 201)
    self.assertTrue(response.data["content"] == self.data["content"])
    self.assertTrue(response.data["rating"] == self.data["rating"])

  def test_rating_validation(self):
    """ Assert rating value is between 0 and 10 """
    self.client.force_authenticate(user=self.user)
    data = self.data

    data["rating"] = 11
    response = self.client.post(reverse("testimonial-list"), data=self.data, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["rating"] == ["Ensure this value is less than or equal to 10."])

    data["rating"] = -1
    response = self.client.post(reverse("testimonial-list"), data=self.data, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["rating"] == ["Ensure this value is greater than or equal to 0."])

  def test_can_retrieve_testimonials(self):
    """ Assert can retrieve testimonials list """
    self.test_can_create_testimonial()
    self.test_can_create_unauthenticated_testimonial()

    response = self.client.get(reverse("testimonial-list"), format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["count"] == 0)

    Testimonial.objects.all().update(published=True)

    response = self.client.get(reverse("testimonial-list"), format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["count"] == 2)
    self.assertTrue(len(response.data["results"]) == 2)
