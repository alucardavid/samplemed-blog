from apps.api.tests.base import BaseAPITestCase
from django.urls import reverse
from rest_framework import status

class ArticleAPITests(BaseAPITestCase):
    def test_list_articles(self):
        """Test retrieving a list of articles"""
        url = reverse('api:v1:article-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_article(self):
        """Test creating a new article"""
        self.authenticate()
        url = reverse('api:v1:article-list')
        data = {
            'title': 'New Article',
            'subtitle': 'New Subtitle',
            'content': 'New Content',
            'type': 0,
            'status': 0,
            'keywords': ['python', 'django']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Article')

    def test_update_article(self):
        """Test updating an existing article"""
        self.authenticate()
        url = reverse('api:v1:article-detail', args=[self.article.id])
        data = {
            'title': 'Updated Article',
            'subtitle': 'Updated Subtitle',
            'content': 'Updated Content',
            'type': 1,
            'status': 1,
            'keywords': ['python', 'django']
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Article')

    def test_delete_article(self):
        """Test deleting an article"""
        self.authenticate()
        url = reverse('api:v1:article-detail', args=[self.article.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify that the article was deleted
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)