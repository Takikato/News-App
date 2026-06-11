from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .serializers import ArticleSerializer
from .models import Article
from django.db.models import Q


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing articles with role-based permissions.

    Provides CRUD operations for articles while enforcing role-specific
    access rules:
    - Readers: can only view approved articles and their subscriptions.
    - Journalists: can create new articles and update/delete their own.
    - Editors: can update/delete any article and approve articles.

    :param viewsets.ModelViewSet: Base class providing default CRUD behavior.
    :raises PermissionDenied: Raised when a user attempts an action without
                              sufficient role permissions.
    :returns: Serialized article data or HTTP responses depending on the action.
    :rtype: rest_framework.response.Response
    """
    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer


    def get_permissions(self):
        """
        Determine permissions based on the current action.

        :returns: A list of permission classes appropriate for the action.
        :rtype: list
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
        Create a new article authored by the current user.

        :param serializer: The serializer instance containing validated data.
        :type serializer: ArticleSerializer
        :raises PermissionDenied: If the user is not a journalist.
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
