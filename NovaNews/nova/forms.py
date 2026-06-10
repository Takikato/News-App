from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, Article, Publisher, Newsletter

class LoginForm(AuthenticationForm):
    """Class that will create and display the Login form"""
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
    """Class that will display the register from"""

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
