from rest_framework.test import APITestCase, APIClient, APIRequestFactory, override_settings
from core.models import User, Bookmark

from rest_framework import status

from django.urls import reverse
from rest_framework.authtoken.models import Token

# Create your tests here.


class BookmarkAPITests(APITestCase):
    fixtures = ['core/fixtures/data.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.first()
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(self.user, token=self.token)

    def test_create(self):
        URL = reverse('bookmarks-list')
        payload = {
            "title": "twitter.com",
            "url": "https://www.twitter.com",
            "user": self.user.id,
            "public": False
        }
        res = self.client.post(URL, payload, format='json', headers={'Authorization': self.token})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        URL = reverse('bookmarks-list')
        res = self.client.get(URL)
        self.assertEqual(len(res.data), len(Bookmark.objects.filter(user=self.user)))


    def test_retrieve(self):
        arg = 4
        URL = reverse('bookmarks-detail', args=[ arg ])
        res = self.client.get(URL, kwargs={ 'pk': arg }, headers={'Authorization': self.token})
        self.assertEqual(res.data['title'], Bookmark.objects.filter(pk=arg, user=self.user.id).first().title)

    def test_destroy(self):
        arg = 7
        URL = reverse('bookmarks-detail', args=[ arg ])
        self.client.delete(URL, kwargs={ 'pk': arg }, headers={'Authorization': self.token})
        self.assertFalse(Bookmark.objects.filter(pk=arg, user=self.user.id).exists())

    def test_partial_patch(self):
        arg = 4
        URL = reverse('bookmarks-detail', args=[ arg ])
        self.client.patch(URL, kwargs={ 'pk': arg }, data={"title": "instagram.com"}, headers={'Authorization': self.token})
        self.assertEqual(Bookmark.objects.filter(pk=arg, user=self.user.id).first().title, "instagram.com")


    def test_update(self):
        arg = 4
        URL = reverse('bookmarks-detail', args=[ arg ])
        self.client.patch(URL, kwargs={ 'pk': arg }, data={"title": "instagram.com", "user": 1, "url": "https://www.instagram.com"}, headers={'Authorization': self.token})
        self.assertEqual(Bookmark.objects.filter(pk=arg, user=self.user.id).first().title, "instagram.com")


