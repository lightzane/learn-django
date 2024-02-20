# 02 - Applications and Routes

https://www.youtube.com/watch?v=a48xeeo5Vnk&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

**A project can have multiple apps**

## Create Blog App

Make sure you are in the same directory with the `manage.py`

To create our blog app, we need this command:

### Start App Command

```bash
python manage.py startapp <app_name>
```

Actual:

```bash
python manage.py startapp blog
```

#### Start App Command Output

This should now create the following tree structure:

```txt
./
├─  proj_name/
│     ├─  blog/
│     │     ├─  migrations/
│     │     │     └─  __init__.py
│     │     ├─  __init__.py
│     │     ├─  admin.py
│     │     ├─  apps.py
│     │     ├─  models.py
│     │     ├─  tests.py
│     │     └─  views.py
│     └─  proj_name/
```

## Adding and mapping a route

### Edit Views

`views.py` Initial

```py
from django.shortcuts import render

# Create your views here.

```

Define a `home()` function where we will handle the routes

```py
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('<h1>Blog Home</h1>')
```

Next we need to create `urls.py` to map the URL pattern to access this `home()` view function

### Create `urls.py` to map url for `home()` view function

`blog/urls.py`

```py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home')
]
```

This wouldn't work just yet. We need to update our main `urls.py` for the entire project.

### Update main `urls.py` in our project

`proj_name/urls.py`

```diff
 from django.contrib import admin
+from django.urls import path, include

 urlpatterns = [
     path('admin/', admin.site.urls),
+    path('blog/', include('blog.urls'))
 ]
```

### Run development server

```bash
python manage.py runserver
```

And open in browser `http://localhost:8000`

In terminal, you would now get this output:

```bash
Not Found: /
[20/Feb/2024 21:42:37] "GET / HTTP/1.1" 404 2167
```

Once we add **URL patterns**, then it should no longer display the default development site like it did before.

But we can try to access `http://localhost:8000/blog` instead and get our expected result as we defined in our `views.py`.

```html
<h1>Blog Home</h1>
```

## Add and map a new route `About`

DIY ...

Tip:

```py
# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]
```

### Why add a trailing slash `/`?

By default, if it has a trailing slash, then **Django** will redirect routes without a forward or trailing slash to that route that has one,

## Make blog app a homepage

```diff
# proj_name/urls.py
 from django.contrib import admin
 from django.urls import path, include

 urlpatterns = [
     path('admin/', admin.site.urls),
+    path('', include('blog.urls'))
 ]
```

Make the path empty.
