This is a Django project that only has one main app which is called nova.

Before you begin make sure you have created a virtual environment and to activate it, make sure you have installed all the required programs form requirements.txt through pip install.

All emails are sent through the terminal and wont actually be sent through Gmail.

**Update database credentials in `NovaCart/settings.py`** if your MySQL username or password differ:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'NovaNews',
           'USER': 'root',
           'PASSWORD': 'your_mysql_password',
           'HOST': 'localhost',
           'PORT': '',
       }
   }
   ```

===How to use API's===

POST /api/token/
This API allows you to login and het your token for authorization.
{
    "username": "your username",
    "password": "your password"
}


GET /api/articles/
This API gets all the approved articles


POST /api/articles/
This API allows you to create a unapproved article
{
  "title": "Breaking News: Django REST API Launched",
  "content": "This is the full article content...",
  "publisher": 1
}


GET /api/articles/<id>/
This API uses the ID if the article to display only that approved article


PUT /api/articles/<id>/
This API allows Editors and Journalists to edit approved article by using its ID
{
  "title": "Updated Article Title",
  "content": "Revised content goes here...",
  "publisher": 1
}


DELETE /api/articles/<id>/
This API allows Editors and Journalist to delete approved article by its ID


GET /api/articles/subscribed/
This API allow Readers to view all their approved article that they are subscribed to


1. **Apply migrations:**

   Run the following commands to create the necessary database tables:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create a superuser** (for admin access):

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to create a user with admin privileges.

3. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

4. **Access the application:**

   * Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   * You can login, register new users, browse articles.


## Troubleshooting

* **MySQL Client Missing Error:**

  If you get `ModuleNotFoundError: No module named 'mysqlclient'`, install it with:

  ```bash
  pip install mysqlclient
  ```

* **SMTP Authentication Error:**

Make sure you use correct email and password. For Gmail, you might need to use App Passwords instead of your regular password.

* **Static files not loading:**

  During development, Django serves static files automatically. For production, you need to configure static files properly.

---

## Project Structure
Should looks like something like this:

```
Folder PATH listing for volume OS
Volume serial number is 0000002C CAC9:3811
C:.
|   FOLDER_STRUCTURE.txt
|   manage.py
|   ReadME.md
|   requirements.txt
|
+---nova
|   |   admin.py
|   |   apps.py
|   |   forms.py
|   |   models.py
|   |   serializers.py
|   |   tests_nova.py
|   |   urls.py
|   |   views.py
|   |   views_api.py
|   |   __init__.py
|   |
|   +---migrations
|   |   |   0001_initial.py
|   |   |   0002_alter_customuser_email_alter_customuser_first_name_and_more.py
|   |   |   0003_alter_publisher_name.py
|   |   |   __init__.py
|   |   |
|   |   \---__pycache__
|   |           0001_initial.cpython-313.pyc
|   |           0002_alter_customuser_email_alter_customuser_first_name_and_more.cpython-313.pyc
|   |           0003_alter_publisher_name.cpython-313.pyc
|   |           __init__.cpython-313.pyc
|   |
|   +---static
|   |   \---nova
|   |           styles.css
|   |
|   +---Templates
|   |   |   base.html
|   |   |
|   |   \---nova
|   |           article_confirm_delete.html
|   |           article_detail.html
|   |           article_edit.html
|   |           article_form.html
|   |           article_list.html
|   |           create_publisher.html
|   |           home.html
|   |           login.html
|   |           newsletter_confirm_delete.html
|   |           newsletter_detail.html
|   |           newsletter_form.html
|   |           newsletter_list.html
|   |           publisher_list.html
|   |           register.html
|   |           search_people.html
|   |
|   +---templatetags
|   |   |   user_groups.py
|   |   |   __init__.py
|   |   |
|   |   \---__pycache__
|   |           user_groups.cpython-313.pyc
|   |           __init__.cpython-313.pyc
|   |
|   +---tests
|   |   |   test_articles_api.py
|   |   |   __init__.py
|   |   |
|   |   \---__pycache__
|   |           test_articles_api.cpython-313.pyc
|   |           __init__.cpython-313.pyc
|   |
|   \---__pycache__
|           admin.cpython-313.pyc
|           apps.cpython-313.pyc
|           forms.cpython-313.pyc
|           models.cpython-313.pyc
|           serializers.cpython-313.pyc
|           tests_nova.cpython-313.pyc
|           urls.cpython-313.pyc
|           views.cpython-313.pyc
|           views_api.cpython-313.pyc
|           __init__.cpython-313.pyc
|
\---NovaNews
    |   asgi.py
    |   settings.py
    |   urls.py
    |   wsgi.py
    |   __init__.py
    |
    \---__pycache__
            settings.cpython-313.pyc
            urls.cpython-313.pyc
            wsgi.cpython-313.pyc
            __init__.cpython-313.pyc

```
(everything worked on my end before I shared the project)