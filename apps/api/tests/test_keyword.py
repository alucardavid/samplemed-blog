from apps.api.models.keyword import Keyword
from apps.api.tests.base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status

class KeywordAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('api:v1:keyword-list')
        self.authenticate()

    def test_create_keyword(self):
        data = {'name': 'new_keyword'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'new_keyword')

    def test_list_keywords(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('test', [keyword['name'] for keyword in response.data['results']]) 

    def test_update_keyword(self):
        keyword = Keyword.objects.create(name='update_keyword')
        url = reverse('api:v1:keyword-detail', args=[keyword.id])
        data = {'name': 'updated_keyword'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'updated_keyword')

    def test_delete_keyword(self):
        keyword = Keyword.objects.create(name='delete_keyword')
        url = reverse('api:v1:keyword-detail', args=[keyword.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Keyword.objects.filter(id=keyword.id).exists())