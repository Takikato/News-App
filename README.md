# Note to reviewer
I have had a discussion with Chris Smit one of the mentors and he says
it is fine if I use SQLite instead of a custom SQL such as MariaDB or
MySQL. (It causes a lot of problems to use a custom DB)

# News-App
This is a repository created for my studies, its just a django project.

This project uses MariaDB as a database backend.

This Django project is a news app that user can use to either be a editor,
journalist or just a normal reader. Journalists can create articles and
newsletters. Editors can create publishers, create newsletter and edit
articles. Readers can view these newsletters and articles and will be able
to subscribe to these Journalists and Publishers to receive emails if they
have posted a newsletter or article.

## Requirements
- Python 3.13+
- Django 5.x
- MariaDB Server (must be installed and running)
- mysqlclient (Python package, installed via requirements.txt)

Note: Installing Python dependencies from requirements.txt is not enough.
You must also install MariaDB Server and create the NovaNews database/user
before running migrations(Everything will be explained in the setup below).


# Setting up the project (Windows OS)
First Clone the project.

Create a virtual environment by using the following commands IDE's terminal:

python -m venv .venv

(Optional Windows OS's have scripts disabled, so run this command):
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

.\.venv\Scripts\activate

Or if the previous command did not work

. .venv/bin/activate

To run the project please change the directory to the NovaNews
(Use the following commands below):

cd NovaNews

pip install -r requirements.txt

# Database setup section (if your not using docker)

If you don't have mariaDB installed:
Install MariaDB (https://mariadb.org/download).

Create a database (run this code):

mysql -u root -p
(enter your MariaDB password.)

CREATE DATABASE NovaNews;

CREATE USER 'novanews_user'@'%' IDENTIFIED BY 'securepassword';

GRANT ALL PRIVILEGES ON NovaNews.* TO 'novanews_user'@'%';

FLUSH PRIVILEGES;

Exit;

# end of Database setup section

python manage.py makemigrations

python manage.py migrate

(Optional run test to make sure everything is working):
python manage.py test

To build the project use the following commands:

docker-compose build

docker-compose up

You can then view the docker by going to docker desktop or pressing "v"
in the terminal after running the (docker-compose up) command.

You can access the project on a website by following this link:

http://localhost:8000

Press Ctrl+C in the terminal to stop the docker.

# Troubleshooting

If you get a forbidden error do to CSRF verification failed. It due to the
fact that it does not trust localhost, add the following code to your
settings.py inside of NovaNews folder if the code is not already there.

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "https://localhost:8000",
    "http://127.0.0.1:8000",
]

# Folder Structure

Your folder structure should look close to this example:

C:.
|   gitignore.gitignore
|   README.md
|
\---NovaNews
    |   docker-compose.yml
    |   Dockerfile
    |   manage.py
    |   ReadME.md
    |   requirements.txt
    |
    +---docs
    |   |   conf.py
    |   |   index.rst
    |   |   make.bat
    |   |   Makefile
    |   |   modules.rst
    |   |   nova.migrations.rst
    |   |   nova.rst
    |   |   nova.templatetags.rst
    |   |   nova.tests.rst
    |   |
    |   +---_build
    |   |   +---doctrees
    |   |   |       environment.pickle
    |   |   |       index.doctree
    |   |   |       modules.doctree
    |   |   |       nova.doctree
    |   |   |       nova.migrations.doctree
    |   |   |       nova.templatetags.doctree
    |   |   |       nova.tests.doctree
    |   |   |
    |   |   \---html
    |   |       |   .buildinfo
    |   |       |   genindex.html
    |   |       |   index.html
    |   |       |   modules.html
    |   |       |   nova.html
    |   |       |   nova.migrations.html
    |   |       |   nova.templatetags.html
    |   |       |   nova.tests.html
    |   |       |   objects.inv
    |   |       |   py-modindex.html
    |   |       |   search.html
    |   |       |   searchindex.js
    |   |       |
    |   |       +---_modules
    |   |       |   |   index.html
    |   |       |   |
    |   |       |   \---nova
    |   |       |       |   admin.html
    |   |       |       |   apps.html
    |   |       |       |   forms.html
    |   |       |       |   models.html
    |   |       |       |   serializers.html
    |   |       |       |   views.html
    |   |       |       |   views_api.html
    |   |       |       |
    |   |       |       +---migrations
    |   |       |       |       0001_initial.html
    |   |       |       |       0002_alter_customuser_email_alter_customuser_first_name_and_more.html
    |   |       |       |       0003_alter_publisher_name.html
    |   |       |       |
    |   |       |       +---templatetags
    |   |       |       |       user_groups.html
    |   |       |       |
    |   |       |       \---tests
    |   |       |               test_articles_api.html
    |   |       |
    |   |       +---_sources
    |   |       |       index.rst.txt
    |   |       |       modules.rst.txt
    |   |       |       nova.migrations.rst.txt
    |   |       |       nova.rst.txt
    |   |       |       nova.templatetags.rst.txt
    |   |       |       nova.tests.rst.txt
    |   |       |
    |   |       \---_static
    |   |           |   base-stemmer.js
    |   |           |   basic.css
    |   |           |   doctools.js
    |   |           |   documentation_options.js
    |   |           |   english-stemmer.js
    |   |           |   file.png
    |   |           |   jquery.js
    |   |           |   language_data.js
    |   |           |   minus.png
    |   |           |   plus.png
    |   |           |   pygments.css
    |   |           |   searchtools.js
    |   |           |   sphinx_highlight.js
    |   |           |   _sphinx_javascript_frameworks_compat.js
    |   |           |
    |   |           +---css
    |   |           |   |   badge_only.css
    |   |           |   |   theme.css
    |   |           |   |
    |   |           |   \---fonts
    |   |           |           fontawesome-webfont.eot
    |   |           |           fontawesome-webfont.svg
    |   |           |           fontawesome-webfont.ttf
    |   |           |           fontawesome-webfont.woff
    |   |           |           fontawesome-webfont.woff2
    |   |           |           lato-bold-italic.woff
    |   |           |           lato-bold-italic.woff2
    |   |           |           lato-bold.woff
    |   |           |           lato-bold.woff2
    |   |           |           lato-normal-italic.woff
    |   |           |           lato-normal-italic.woff2
    |   |           |           lato-normal.woff
    |   |           |           lato-normal.woff2
    |   |           |           Roboto-Slab-Bold.woff
    |   |           |           Roboto-Slab-Bold.woff2
    |   |           |           Roboto-Slab-Regular.woff
    |   |           |           Roboto-Slab-Regular.woff2
    |   |           |
    |   |           +---fonts
    |   |           |   +---Lato
    |   |           |   |       lato-bold.eot
    |   |           |   |       lato-bold.ttf
    |   |           |   |       lato-bold.woff
    |   |           |   |       lato-bold.woff2
    |   |           |   |       lato-bolditalic.eot
    |   |           |   |       lato-bolditalic.ttf
    |   |           |   |       lato-bolditalic.woff
    |   |           |   |       lato-bolditalic.woff2
    |   |           |   |       lato-italic.eot
    |   |           |   |       lato-italic.ttf
    |   |           |   |       lato-italic.woff
    |   |           |   |       lato-italic.woff2
    |   |           |   |       lato-regular.eot
    |   |           |   |       lato-regular.ttf
    |   |           |   |       lato-regular.woff
    |   |           |   |       lato-regular.woff2
    |   |           |   |
    |   |           |   \---RobotoSlab
    |   |           |           roboto-slab-v7-bold.eot
    |   |           |           roboto-slab-v7-bold.ttf
    |   |           |           roboto-slab-v7-bold.woff
    |   |           |           roboto-slab-v7-bold.woff2
    |   |           |           roboto-slab-v7-regular.eot
    |   |           |           roboto-slab-v7-regular.ttf
    |   |           |           roboto-slab-v7-regular.woff
    |   |           |           roboto-slab-v7-regular.woff2
    |   |           |
    |   |           \---js
    |   |                   badge_only.js
    |   |                   theme.js
    |   |                   versions.js
    |   |
    |   +---_static
    |   \---_templates
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
    |   +---templates
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
