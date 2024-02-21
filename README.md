# 03 - Templates

https://www.youtube.com/watch?v=qDwdMDQ8oX4&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

`blog/views.py`

```py
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('<h1>Blog Home</h1>')

def about(request):
    return HttpResponse('<h1>Blog About</h1>')
```

Instead of having a hard-code HTML content, let's create **templates**.

## Create Templates

Create a directory `templates` under `blog`. By default, **Django** looks into a _templates_ subdirectory and inside into each of our `INSTALLED_APPS` (see `settings.py`).

Django looks onto this convention:

```txt
<app_name> -> templates -> <app_name> -> *.html
blog -> templates -> blog -> template.html
```

So let's create another `blog` folder inside the _templates_ subdirectory

```txt
proj_name/
  └─  blog/
       └─  templates/
             └─  blog/
                  ├─  about.html
                  └─  home.html
```

`home.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Home</title>
  </head>
  <body>
    <h1>Blog Home</h1>
  </body>
</html>
```

## Add Blog AppConfig in Project Settings

We have `blog/apps.py`, copy its **Class** name, in this case `BlogConfig` and add it into our **Project settings** located in `proj_name/settings.py`

```py
from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
```

`proj_name/settings.py`

```diff
 ...

 # Application definition

 INSTALLED_APPS = [
+    'blog.apps.BlogConfig',
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
 ]

 ...
```

## Update `views.py`

```diff
...

def home(request):
+   return render(request, 'blog/home.html')
-   return HttpResponse('<h1>Blog Home</h1>')

...
```

## Run server and verify

```bash
python manage.py runserver
```

View page source in browser and you'll see this result:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Home</title>
  </head>
  <body>
    <h1>Blog Home</h1>
  </body>
</html>
```

> Repeat the same steps for the `About` page

## Add mock data to Context

The mock data will be accessed via the `key` of the `Context` dict that we'll pass in.

`views.py`

```diff
 from django.shortcuts import render

+posts = [
+    {
+        'author': 'Lightzane',
+        'title': 'Blog Post 1',
+        'content': 'First post content',
+        'date_posted': 'Feb 21, 2024'
+    },
+    {
+        'author': 'Lightzane',
+        'title': 'Blog Post 2',
+        'content': 'Second post content',
+        'date_posted': 'Feb 22, 2024'
+    },
+]

 # Create your views here.
 def home(request):
+    context = {
+        'posts': posts
+    }
+    return render(request, 'blog/home.html', context)
-    return render(request, 'blog/home.html')

...
```

## Access the data in template via code block

Django is using a template engine, and to use a code block in html, we will use the following syntax: `{% ... %}`

### Loop code block

`blog/home.html`

```diff
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Home</title>
  </head>

  <body>
+   {% for post in posts %}
+       <h1>{{ post.title }}</h1>
+       <p>By {{ post.author }} on {{ post.date_posted }}</p>
+       <p>{{ post.content }}</p>
+   {% endfor %}
  </body>
</html>

```

### Conditional code block

`home.html`

```diff
 <head>
     <meta charset="UTF-8" />
     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
+    {% if title %}
+        <title>Django Blog - {{ title }}</title>
+    {% else %}
+        <title>Django Blog</title>
+    {% endif %}
-    <title>Home</title>
 </head>
```

> Do the same for `about.html`

### Template Inheritance

Apply `DRY` (**D**on't **R**epeat **Y**ourself) and reduce duplicate blocks of codes that we can **REUSE**

Create `blog/base.html`

<!-- prettier-ignore -->
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    {% if title %}
        <title>Django Blog - {{ title }}</title>
    {% else %}
        <title>Django Blog</title>
    {% endif %}
  </head>
  <body>
    <!-- 'content' is arbitrary name -->
    {% block content %}{% endblock %}
  </body>
</html>
```

#### `{% extends "..." %}`

Update `home.html` to extend `base.html`

<!-- prettier-ignore -->
```html
{% extends "blog/base.html" %}

<!-- 'content' is defined by the parent we extend -->
{% block content %}
    {% for post in posts %}
        <h1>{{ post.title }}</h1>
        <p>By {{ post.author }} on {{ post.date_posted }}</p>
        <p>{{ post.content }}</p>
    {% endfor %}
{% endblock content %}
```

Note that you can also use `{% endblock %}` instead of `{% endblock content %}`. But if you have multiple blocks, you may lose track of which block would end. So it's recommended to use `{ endblock content }`

> Do the same for `About.html`

## Apply Styles

This project uses `Bootstrap 4` (https://getbootstrap.com/docs/4.0/getting-started/introduction/#starter-template)

`base.html`

<!-- prettier-ignore -->
```diff
<!DOCTYPE html>
<html lang="en">
  <head>
+    <!-- Required meta tags -->
+    <meta charset="utf-8">
+    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
+
+    <!-- Bootstrap CSS -->
+    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    {% if title %}
        <title>Django Blog - {{ title }}</title>
    {% else %}
        <title>Django Blog</title>
    {% endif %}

+   <!-- Optional JavaScript -->
+   <!-- jQuery first, then Popper.js, then Bootstrap JS -->
+   <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
+   <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
+   <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </head>
  <body>
+   <div class="container">
      <!-- 'content' is arbitrary name -->
      {% block content %}{% endblock %}
+   </div>
  </body>
</html>
```

**Snippets** (https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog/snippets)

Copy `navigation.html` snippet here: https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/snippets/navigation.html

Copy `main.html` snippet here: https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/snippets/main.html

## Create `static` directory for CSS and Javascript

Django reads static files from this subdirectory: `<app>/static/<app>`

`blog/static/blog/main.css`

Copy snippet here: https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/snippets/main.css

## Tell Django to load static files

`base.html`

```diff
+{% load static %}
 <!DOCTYPE html>
 <html lang="en">
   <head>
     <!-- Required meta tags -->
     <meta charset="utf-8">

     ...
```

## Import the static `css` file

```html
<link rel="stylesheet" type="text/css" href="{% static 'blog/main.css' %}" />
```

The `static` creates an absolute URL of the static files and accesses that `blog/static/blog/main.css`.

**Replace current html inside loop code block in `home.html` with article snippet**
Copy `article.html` snippet here : https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/snippets/article.html

## NEVER HARD-CODE HREF URLS

```html
<a class="navbar-brand mr-4" href="/">Django Blog</a>
<a class="nav-item nav-link" href="/">Home</a>
<a class="nav-item nav-link" href="/about">About</a>
```

Recall `blog/urls.py`

```py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]
```

We will use the `name` instead of **hard-code urls**.

```html
<a class="navbar-brand mr-4" href="{% url 'blog-home' %}">Django Blog</a>
<a class="nav-item nav-link" href="{% url 'blog-home' %}">Home</a>
<a class="nav-item nav-link" href="{% url 'blog-about' %}">About</a>
```
