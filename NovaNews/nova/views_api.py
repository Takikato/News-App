from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .serializers import ArticleSerializer
from .models import Article
from django.db.models import Q


class ArticleViewSet(viewsets.ModelViewSet):
    """
    _summary_

    Args:
        viewsets (_type_): _description_

    Raises:
        PermissionDenied: _description_
        PermissionDenied: _description_
        PermissionDenied: _description_

    Returns:
        _type_: _description_
    """
    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer


    def get_permissions(self):
        """
        _summary_

        Returns:
            _type_: _description_
        """
        if self.action in ["list", "retrieve", "subscribed"]:
            return [permissions.IsAuthenticatedOrReadOnly()]
        elif self.action == "create":
            # Only journalists can POST
            return [permissions.IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            # Editors or authors can edit/delete
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


    def perform_create(self, serializer):
        """
        _summary_

        Args:
            serializer (_type_): _description_

        Raises:
            PermissionDenied: _description_
        """
        user = self.request.user
        if user.role != "journalist":
            raise PermissionDenied("Only journalists can create articles.")
        serializer.save(author=user)


    def perform_update(self, serializer):
        """
        _summary_

        Args:
            serializer (_type_): _description_

        Raises:
            PermissionDenied: _description_
        """
        user = self.request.user
        article = self.get_object()
        if user.role == "editor" or (user.role == "journalist" and
                                     article.author == user):
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission "
            "to update this article.")


    def perform_destroy(self, instance):
        """
        _summary_

        Args:
            instance (_type_): _description_

        Raises:
            PermissionDenied: _description_
        """
        user = self.request.user
        if user.role == "editor" or (user.role == "journalist" and
                                     instance.author == user):
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission "
            "to delete this article.")


    @action(detail=False, methods=["get"], url_path="subscribed")
    def subscribed(self, request):
        """
        Return articles only from the reader's
        subscribed publishers/journalists
        """
        user = request.user
        if user.role != "reader":
            return Response(
                {"detail": "Only readers can access subscribed articles."},
                status=403
                )

        subscribed_publishers = user.subscriptions_publishers.all()
        subscribed_journalists = user.subscriptions_journalists.all()

        articles = Article.objects.filter(
            approved=True
        ).filter(
            (Q(publisher__in=subscribed_publishers) |
             Q(author__in=subscribed_journalists))
        )

        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
