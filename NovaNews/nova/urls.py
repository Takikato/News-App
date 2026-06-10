from django.urls import path
from . import views

urlpatterns = [
    # Default URL to make user sign in
    path("login/", views.login_user, name="login"),

    # URL to allow user to register
    path("register/", views.register_user, name="register"),

    # URL to logout the current user
    path("logout/", views.logout_user, name="logout"),

    # URL to go to the home page
    path("", views.home, name="home"),

    # URL for listing all the articles
    path("articles/", views.article_list, name="article_list"),

    # URl for creating a article
    path("articles/create/", views.article_create, name="article_create"),

    # URL for approving articles
    path("articles/<int:article_id>/approve/", views.approve_article, name="approve_article"),

    # URL for specific articles
    path("articles/<int:article_id>/", views.article_detail, name="article_detail"),

    # URL to view all the publishers
    path("publishers/", views.publisher_list, name="publisher_list"),

    # URL to create a new publisher
    path("publishers/create/", views.create_publisher, name="create_publisher"),

    # URL to edit a article
    path("articles/<int:article_id>/edit/", views.article_edit, name="article_edit"),

    # URL to delete a article confirmation page
    path("articles/<int:article_id>/delete/", views.article_delete, name="article_delete"),

    # URL to view all newsletters
    path("newsletters/", views.newsletter_list, name="newsletter_list"),

    # URL for creating a new newsletter
    path("newsletters/create/", views.create_newsletter, name="create_newsletter"),

    # URL to view specific newsletter
    path("newsletters/<int:newsletter_id>/", views.newsletter_detail, name="newsletter_detail"),

    # URL to edit a news letter
    path("newsletters/<int:newsletter_id>/edit/", views.newsletter_edit, name="newsletter_edit"),

    # URL to delete a newsletter
    path("newsletters/<int:newsletter_id>/delete/", views.newsletter_delete, name="newsletter_delete"),

    # URL to search for publishers or journalists
    path("search/", views.search_people, name="search_people"),

    # URL to subscribe to a publisher
    path("publishers/<int:publisher_id>/subscribe/", views.subscribe_publisher, name="subscribe_publisher"),

    # URL to unsubscribe to a publisher
    path("publishers/<int:publisher_id>/unsubscribe/", views.unsubscribe_publisher, name="unsubscribe_publisher"),

    # URL to subscribe to a journalist
    path("journalists/<int:journalist_id>/subscribe/", views.subscribe_journalist, name="subscribe_journalist"),

    # URL to unsubscribe to a journalist
    path("journalists/<int:journalist_id>/unsubscribe/", views.unsubscribe_journalist, name="unsubscribe_journalist"),

]
