from rest_framework.test import APITestCase
from rest_framework import status
from .models import Message
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class MessagesAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User(username="testUser1", password="Aa123456")
        self.user1.save()
        self.user2 = User(username="testUser2", password="Bb123456")
        self.user2.save()
        self.user3 = User(username="testUser3", password="Cc123456")
        self.user3.save()
        self.tokenUser1 = Token.objects.create(user=self.user1)
        self.tokenUser3 = Token.objects.create(user=self.user3)
        self.new_message = Message.objects.create(
            sender=self.user1,
            subject="this message created for testing porpuses",
            message="",
            receiver=self.user2)
        self.new_message.save()

    # user setup testing
    def test_user_counter(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 3)

    # message setup testing
    def test_messages_counter(self):
        msg_count = Message.objects.count()
        self.assertEqual(msg_count, 1)

    # Unauthorized get call for messages list
    def test_get_messages_list_unauthorized(self):
        data = {}
        url = reverse("messages-api:messages")
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Authorized get call for messages list
    def test_get_messages_list_authorized(self):
        data = {}
        url = reverse("messages-api:messages")
        response = self.client.get(
            url, data, HTTP_AUTHORIZATION='Token {}'.format(self.tokenUser1), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # POST message with authorized user
    def test_post_message_authorized(self):
        data = {"sender": 1,
                "subject": "checking random message posting.",
                "message": "",
                "receiver": self.user3.pk}
        url = reverse("messages-api:messages")
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION='Token {}'.format(self.tokenUser3), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Read single message
    def test_get_single_message_authorized(self):
        data = {}
        url = reverse("messages-api:single-message",
                      kwargs={"pk": self.new_message.pk})
        response = self.client.get(
            url, data, HTTP_AUTHORIZATION='Token {}'.format(self.tokenUser1), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Read single message Unauthorized
    def test_get_message_Unauthorized(self):
        data = {}
        url = reverse("messages-api:single-message",
                      kwargs={"pk": self.new_message.pk})
        response = self.client.get(
            url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Read single message as not seceiver / sender of the message
    def test_get_single_message_as_not_the_owener(self):
        data = {}
        url = reverse("messages-api:single-message",
                      kwargs={"pk": self.new_message.pk})
        response = self.client.get(
            url, data, HTTP_AUTHORIZATION='Token {}'.format(self.tokenUser3), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
