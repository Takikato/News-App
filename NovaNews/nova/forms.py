from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, Article, Publisher, Newsletter

class LoginForm(AuthenticationForm):
    """
    Custom login form for user authentication.

    Extends Django's built-in AuthenticationForm to provide
    styled input fields for username and password. Includes
    Bootstrap-compatible CSS classes and placeholder text.

    :param AuthenticationForm: Base Django authentication form.
    :type AuthenticationForm: django.contrib.auth.forms.AuthenticationForm
    :returns: A validated login form for user authentication.
    :rtype: LoginForm
    """
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control",
                                       "placeholder": "Enter username"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control",
                                          "placeholder": "Enter password"})
    )


class RegisterForm(UserCreationForm):
    """
    Custom registration form for new users.

    Extends Django's UserCreationForm to include additional
    fields from the CustomUser model, such as email, first name,
    last name, and role. Provides validation and integration
    with Django's authentication system.

    :param UserCreationForm: Base Django user creation form.
    :type UserCreationForm: django.contrib.auth.forms.UserCreationForm
    :returns: A validated registration form for creating new users.
    :rtype: RegisterForm
    """

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name",
                  "last_name", "role", "password1", "password2"]


class ArticleForm(forms.ModelForm):
    """Class that displays the Article form"""
    class Meta:
        model = Article
        fields = ["title", "content", "publisher"]


class PublisherForm(forms.ModelForm):
    """Class that displays the Publisher form"""
    class Meta:
        model = Publisher
        fields = ["name"]


class NewsletterForm(forms.ModelForm):
    """CLass that displays the newsletter form"""
    class Meta:
        model = Newsletter
        fields = ["title", "description", "articles"]
