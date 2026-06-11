from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    This model replaces the default Django User model and adds
    role-based functionality. It supports three roles:
    - Reader: can subscribe to publishers and journalists.
    - Editor: can manage publishers and approve articles.
    - Journalist: can author articles and be followed by readers.

    Reader-specific subscription fields allow users to follow
    publishers and journalists directly. The `save` method ensures
    that each user is automatically assigned to a Django group
    corresponding to their role.

    :param AbstractUser: Base Django user model with authentication fields.
    :type AbstractUser: django.contrib.auth.models.AbstractUser
    """
    ROLE_CHOICES = [
        ("reader", "Reader"),
        ("editor", "Editor"),
        ("journalist", "Journalist"),
    ]
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=30, unique=True, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=False)

    # Reader-specific fields
    subscriptions_publishers = models.ManyToManyField(
        "Publisher", blank=True, related_name="subscribed_readers"
    )
    subscriptions_journalists = models.ManyToManyField(
        "CustomUser", blank=True,
        related_name="subscribed_readers_journalists"
    )

    def save(self, *args, **kwargs):
        """
        Save the user instance and assign a group based on role.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :raises Group.DoesNotExist: If the group for the role cannot be created.
        """
        super().save(*args, **kwargs)
        # Assign group based on role
        group, _ = Group.objects.get_or_create(name=self.role.capitalize())
        self.groups.clear()
        self.groups.add(group)


class Publisher(models.Model):
    """
    Publisher model representing organizations that produce articles.

    A publisher can have multiple editors and journalists associated
    with it. Editors manage the publisher, while journalists contribute
    articles under the publisher's name.

    :param models.Model: Base Django model class.
    :type models.Model: django.db.models.Model
    :returns: String representation of the publisher (its name).
    :rtype: str
    """
    name = models.CharField(max_length=100, unique=True)
    editors = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name="editor_publishers"
    )
    journalists = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name="journalist_publishers"
    )

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    _summary_
    Class for articles
    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name="authored_articles")
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                  null=True, blank=True,
                                    related_name="published_articles")

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """
    _summary_
    Class for newsletters
    Returns:
        _type_: _description_
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name="author_newsletters")
    articles = models.ManyToManyField(Article,
                                      related_name="articles_newsletters")

    def __str__(self):
        return self.title
