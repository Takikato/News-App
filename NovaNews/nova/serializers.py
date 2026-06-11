from rest_framework import serializers
from .models import Article, Publisher, Newsletter, CustomUser

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.

    Converts Article instances to and from JSON representations.
    Ensures that certain fields are read-only, such as the ID,
    author, approval status, and creation timestamp.

    :returns: Serialized Article data.
    :rtype: dict
    """
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "author",
            "publisher",
            "approved",
            "created_at"
            ]
        read_only_fields = ["id", "author", "approved", "created_at"]


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializer for the Publisher model.

    Provides JSON representation of Publisher instances.
    The ID field is read-only.

    :returns: Serialized Publisher data.
    :rtype: dict
    """
    class Meta:
        model = Publisher
        fields = ["id", "name"]
        read_only_fields = ["id"]


class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Newsletter model.

    Includes nested serialization of related articles.
    Ensures that ID, author, articles, and creation timestamp
    are read-only fields.

    :returns: Serialized Newsletter data including related articles.
    :rtype: dict
    """
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Newsletter
        fields = [
            "id",
            "title",
            "description",
            "author",
            "articles",
            "created_at"
            ]
        read_only_fields = ["id", "author", "articles", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser class"""
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role"]
        read_only_fields = ["id", "role"]

