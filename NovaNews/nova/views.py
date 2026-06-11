from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Publisher, Article, Newsletter
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import (LoginForm, RegisterForm, ArticleForm,
                    PublisherForm, NewsletterForm)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.db.models import Q


def login_user(request):
    """
    Authenticate and log in a user.

    This view handles user login by validating the submitted login form.
    If the request method is POST, the form is validated and the user is
    authenticated. On success, the user is logged in and redirected to
    the home page with a success message. On failure, an error message
    is displayed. For GET requests, an empty login form is rendered.

    :param request: The HTTP request object containing method and form data.
    :type request: django.http.HttpRequest

    :returns: An HTTP response rendering the login template or a redirect
              to the home page upon successful login.
    :rtype: django.http.HttpResponse
    """
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("home")
        else:
            messages.error(request, "Invalid login details")
    else:
        form = LoginForm()

    return render(request, "nova/login.html", {"form": form})


def register_user(request):
    """
    Handle user registration by processing the registration form.

    This view manages the registration of a new user. If the request
    method is POST, it validates and saves the submitted form data.
    On success, the user is redirected to the login page with a success
    message. On failure, an error message is displayed. For GET requests,
    an empty registration form is rendered.

    :param request: The HTTP request object containing method and form data.
    :type request: django.http.HttpRequest

    :returns: An HTTP response rendering the registration template or a redirect
              to the login page upon successful registration.
    :rtype: django.http.HttpResponse
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Acount created successfully")
            return redirect("login")
        else:
            messages.error(request, "Register error")
    else:
        form = RegisterForm()

    return render(request, "nova/register.html", {"form": form})


@login_required
def logout_user(request):
    """
    Log out the currently authenticated user.

    This view ends the user's session by calling Django's built-in
    logout function. After logging out, the user is redirected to
    the login page.

    :param request: The HTTP request object containing session information.
    :type request: django.http.HttpRequest

    :returns: An HTTP response that redirects the user to the login page.
    :rtype: django.http.HttpResponseRedirect
    """
    logout(request)
    return redirect("login") # redirect the user back to the log in screen


def is_user_editor(user):
    """
    _summary_
    Check if user is editor
    Args:
        user (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (user.groups.filter(name="Editor").exists() or
            user.role == "editor"
    )


def is_user_journalist(user):
    """
    _summary_
    Check if user is journalist
    Args:
        user (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (user.groups.filter(name="Journalist").exists() or
            getattr(user, "role", None) == "journalist"
    )


def is_user_editor_or_journalist(user):
    """
    _summary_
    Check if user us a editor or a journalist
    Args:
        user (_type_): _description_

    Returns:
        _type_: _description_
    """
    return (
        user.groups.filter(name__in=["Editor", "Journalist"]).exists() or
        getattr(user, "role", None) in ["editor", "journalist"]
    )


@login_required
def home(request):
    """
    _summary_
    Function that takes the user to homepage
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return render(request, "nova/home.html")


def article_list(request):
    """
    _summary_
    List all the articles
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    articles = Article.objects.all()
    return render(request, "nova/article_list.html",
                  {"articles": articles})


@login_required
@user_passes_test(is_user_journalist)
def article_create(request):
    """
    _summary_
    Allow user to create a article
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("article_detail", article_id=article.id)
    else:
        form = ArticleForm()
    return render(request, "nova/article_form.html", {"form": form})


@login_required
@user_passes_test(is_user_editor)
def approve_article(request, article_id):
    """
    _summary_
    Allow Editor to approve a article
    Args:
        request (_type_): _description_
        article_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    article = get_object_or_404(Article, id=article_id)
    article.approved = True
    article.save()

    # Collect subscribers
    recipients = []

    # Journalist subscribers
    recipients += list(
        article.author.subscribed_readers_journalists.values_list("email",
                                                                  flat=True)
        )

    # Publisher subscribers
    if article.publisher:
        recipients += list(
            article.publisher.subscribed_readers.values_list("email",
                                                             flat=True)
            )

    # Deduplicate
    recipient_list = list(set(recipients))

    # Send email once per unique user
    if recipient_list:
        send_mail(
            subject=f"New Article Approved: {article.title}",
            message=article.content,
            from_email="no-reply@novanews.com",
            recipient_list=recipient_list,
        )

        messages.success(request, "Article approved and published!")
    else:
        messages.info(request, "This article is already approved.")

    return redirect("article_detail", article_id=article.id)


def article_detail(request, article_id):
    """
    _summary_
    Give all the information of the article

    Args:
        request (_type_): _description_
        article_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    article = get_object_or_404(Article, id=article_id)
    is_editor = is_user_editor(request.user)
    return render(request, "nova/article_detail.html", {
        "article": article,
        "is_editor": is_editor,
    })


@login_required
@user_passes_test(is_user_editor)
def create_publisher(request):
    """
    _summary_
    Allow Editors to create a new publisher
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            # Automatically assign the editor who created it
            publisher.editors.add(request.user)
            messages.success(
                request, f"Publisher '{publisher.name}' "
                "created successfully!"
                )
            return redirect("publisher_list")
    else:
        form = PublisherForm()
    return render(request, "nova/create_publisher.html", {"form": form})


@login_required
def publisher_list(request):
    """
    _summary_
    List all the publishers in a list
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    publishers = Publisher.objects.all()
    is_editor = is_user_editor(request.user)
    return render(request, "nova/publisher_list.html",
                  {"publishers": publishers, "is_editor": is_editor})


@login_required
def article_edit(request, article_id):
    """
    _summary_
    Allow Editors and Journalists to edit articles
    Args:
        request (_type_): _description_
        article_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    article = get_object_or_404(Article, id=article_id)

    # Rule: Editors can always edit, authors only if not approved
    is_editor = is_user_editor(request.user)
    is_author = article.author == request.user

    if not is_editor and not (is_author and not article.approved):
        messages.error(request,
                       "You do not have permission to edit this article.")
        return redirect("article_detail", article_id=article.id)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect("article_detail", article_id=article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, "nova/article_edit.html", {"form": form,
                                                      "article": article})


@login_required
def article_delete(request, article_id):
    """
    _summary_
    Allow Editors and Journalists to delete articles
    Args:
        request (_type_): _description_
        article_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    article = get_object_or_404(Article, id=article_id)

    # Rule: Editors can always delete, authors only if not approved
    is_editor = is_user_editor(request.user)
    is_author = article.author == request.user

    if not is_editor and not (is_author and not article.approved):
        messages.error(request,
                       "You do not have permission to delete this article.")
        return redirect("article_detail", article_id=article.id)

    if request.method == "POST":
        article.delete()
        messages.success(request, "Article deleted successfully!")
        return redirect("article_list")

    return render(request, "nova/article_confirm_delete.html",
                  {"article": article})


@login_required
@user_passes_test(is_user_editor_or_journalist)
def create_newsletter(request):
    """
    _summary_
    Allow Editors and Journalists to create newsletters
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()  # save selected articles

            # Collect subscribers from both journalist and publisher(s)
            recipients = []

            # Subscribers to the author (journalist)
            recipients += list(
                newsletter.author.subscribed_readers_journalists
                .values_list("email", flat=True)
            )

            # Subscribers to publishers of included articles
            for article in newsletter.articles.all():
                if article.publisher:
                    recipients += list(
                        article.publisher.subscribed_readers
                        .values_list("email", flat=True)
                    )

            # Deduplicate email addresses
            recipient_list = list(set(recipients))

            # Send newsletter email
            if recipient_list:
                send_mail(
                    subject=f"New Newsletter: {newsletter.title}",
                    message=newsletter.description,
                    from_email="no-reply@novanews.com",
                    recipient_list=recipient_list,
                )

            messages.success(request,
                             "Newsletter created and emailed successfully!")
            return redirect("newsletter_list")
    else:
        form = NewsletterForm()
    return render(request, "nova/newsletter_form.html", {"form": form})


@login_required
def newsletter_list(request):
    """
    _summary_
    List all the newsletters in a list for user
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    newsletters = Newsletter.objects.all().order_by("-created_at")
    return render(request, "nova/newsletter_list.html",
                  {"newsletters": newsletters})


@login_required
def newsletter_detail(request, newsletter_id):
    """
    _summary_
    Gives all the information of the newsletter for user
    Args:
        request (_type_): _description_
        newsletter_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    return render(request, "nova/newsletter_detail.html",
                  {"newsletter": newsletter})


@login_required
def newsletter_edit(request, newsletter_id):
    """
    _summary_
    Allow Editors and Journalists to edit newsletters
    Args:
        request (_type_): _description_
        newsletter_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    is_editor = is_user_editor
    is_author = newsletter.author == request.user

    if not (is_editor or is_author):
        messages.error(request,
                       "You do not have permission to edit this newsletter.")
        return redirect("newsletter_detail", newsletter_id=newsletter.id)

    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, "Newsletter updated successfully!")
            return redirect("newsletter_detail", newsletter_id=newsletter.id)
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, "nova/newsletter_form.html",
                  {"form": form, "newsletter": newsletter})


@login_required
def newsletter_delete(request, newsletter_id):
    """
    _summary_
    Allow Editors and Journalists to delete newsletters
    Args:
        request (_type_): _description_
        newsletter_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    is_editor = (request.user.groups.filter(name="Editor").exists() or
                 getattr(request.user, "role", None) == "editor")
    is_author = newsletter.author == request.user

    if not (is_editor or is_author):
        messages.error(
            request,
            "You do not have permission to delete this newsletter."
            )
        return redirect("newsletter_detail", newsletter_id=newsletter.id)

    if request.method == "POST":
        newsletter.delete()
        messages.success(request, "Newsletter deleted successfully!")
        return redirect("newsletter_list")

    return render(request, "nova/newsletter_confirm_delete.html",
                  {"newsletter": newsletter})


@login_required
def search_people(request):
    """
    _summary_
    All user to search for Publishers and Journalists
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    query = request.GET.get("q", "")

    # Journalists
    journalists = CustomUser.objects.filter(role="journalist")
    if query:
        journalists = journalists.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    # Publishers
    publishers = Publisher.objects.all()
    if query:
        publishers = publishers.filter(name__icontains=query)

    return render(request, "nova/search_people.html", {
        "query": query,
        "journalists": journalists,
        "publishers": publishers,
    })


@login_required
def subscribe_publisher(request, publisher_id):
    """
    _summary_
    Allow user to subscribe to a publisher
    Args:
        request (_type_): _description_
        publisher_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    publisher = get_object_or_404(Publisher, id=publisher_id)
    request.user.subscriptions_publishers.add(publisher)
    messages.success(request, f"You subscribed to {publisher.name}.")
    return redirect("search_people")


@login_required
def unsubscribe_publisher(request, publisher_id):
    """
    _summary_
    Allow user to unsubscribe to a publisher
    Args:
        request (_type_): _description_
        publisher_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    publisher = get_object_or_404(Publisher, id=publisher_id)
    request.user.subscriptions_publishers.remove(publisher)
    messages.info(request, f"You unsubscribed from {publisher.name}.")
    return redirect("search_people")


@login_required
def subscribe_journalist(request, journalist_id):
    """
    _summary_
    Allow user to subscribe to a journalist
    Args:
        request (_type_): _description_
        journalist_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    journalist = get_object_or_404(CustomUser,
                                   id=journalist_id, role="journalist")
    request.user.subscriptions_journalists.add(journalist)
    messages.success(request, f"You subscribed to {journalist.username}.")
    return redirect("search_people")


@login_required
def unsubscribe_journalist(request, journalist_id):
    """
    _summary_
    Allow user to subscribe to a journalist
    Args:
        request (_type_): _description_
        journalist_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    journalist = get_object_or_404(CustomUser, id=journalist_id,
                                   role="journalist")
    request.user.subscriptions_journalists.remove(journalist)
    messages.info(request, f"You unsubscribed from {journalist.username}.")
    return redirect("search_people")
