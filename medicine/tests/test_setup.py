import uuid
from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

"""
Setup the test base class.
It will inherit the TestCase
"""
class TestBaseSetup(TestCase):

    def setUp(self):
        self.url = reverse("product:product-list")
        self.client = APIClient()
        try:
            self.user = User.objects.get(username='test_username')
        except:
            self.user = User.objects.create(
                username='test_username',
                email='test@email.com',
            )
        refresh = RefreshToken.for_user(self.user)
        self.prId = '21'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
