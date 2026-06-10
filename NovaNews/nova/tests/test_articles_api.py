from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from nova.models import Article, Publisher


User = get_user_model()

User = get_user_model()

class ArticleViewSetTests(APITestCase):
    def setUp(self):
        """
        Setup the users and article that will be used for testing
        """
        # Create users
        self.reader = User.objects.create_user(
            username="reader1",
            email="reader1@gmail.com",
            password="pass",
            role="reader"
            )

        self.journalist = User.objects.create_user(
            username="journalist1",
            email="journalist1@gmail.com",
            password="pass",
            role="journalist")

        self.editor = User.objects.create_user(
            username="editor1",
            email="editor1@gmail.com",
            password="pass",
            role="editor")

        # Create publisher
        self.publisher = Publisher.objects.create(name="Tech Daily")

        # Create article
        self.article = Article.objects.create(
            title="Breaking News",
            content="Some content",
            author=self.journalist,
            publisher=self.publisher,
            approved=True
        )

        # Authenticated clients
        self.reader_client = APIClient()
        self.reader_client.force_authenticate(user=self.reader)

        self.journalist_client = APIClient()
        self.journalist_client.force_authenticate(user=self.journalist)

        self.editor_client = APIClient()
        self.editor_client.force_authenticate(user=self.editor)


    def test_reader_can_list_articles(self):
        """Test to see if all articles are displayed"""
        response = self.reader_client.get("/api/articles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_reader_subscribed_articles_only(self):
        """Test if only readers can see subscribed articles"""
        self.reader.subscriptions_publishers.add(self.publisher)
        response = self.reader_client.get("/api/articles/subscribed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            any(a["title"] == "Breaking News" for a in response.data)
            )


    def test_journalist_can_create_article(self):
        """Test if journalists can create articles"""
        data = {
            "title": "New Article",
            "content": "Journalist content",
            "publisher": self.publisher.id
            }
        response = self.journalist_client.post("/api/articles/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_journalist_can_delete_own_article(self):
        """Test if journalist can delete their own articles"""
        article = Article.objects.create(
            title="Own Article",
            content="Owned content",
            author=self.journalist,
            publisher=self.publisher,
            approved=True
        )
        response = self.journalist_client.delete(
            f"/api/articles/{article.id}/"
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_journalist_cannot_delete_other_articles(self):
        """Test if journalist cannot delete their own articles"""
        other_journalist = User.objects.create_user(
            username="journalist2",
            email="journalist2@example.com",
            password="pass",
            role="journalist"
        )
        article = Article.objects.create(
            title="Other Article",
            content="Other content",
            author=other_journalist,
            publisher=self.publisher,
            approved=True
        )
        response = self.journalist_client.delete(
            f"/api/articles/{article.id}/"
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_editor_can_update_article(self):
        """
        Test that an editor can successfully update an existing article.
        """
        data = {
            "title": "Updated Title",
            "content": "Updated content",
            "publisher": self.publisher.id
            }
        response = self.editor_client.put(
            f"/api/articles/{self.article.id}/", data
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_editor_can_delete_article(self):
        """
        Test that an editor can successfully delete an existing article.
        """
        response = self.editor_client.delete(
            f"/api/articles/{self.article.id}/"
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
