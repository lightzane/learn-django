# 11 - Pagination

https://www.youtube.com/watch?v=acOktTcTVEQ&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

## Add more posts

You can manually add posts. Or you can import this [`posts.json`](./readme_assets/posts.json) file to automatically add posts. (_Requires 2 users_)

If you'll do it this way, we'll do this steps:

Before starting, make sure you have a `posts.json` file into the same directory in which we're going to do the `django python shell`, or anywhere else as long as we specify the correct path. In this project, the file is located in `../readme_assets/posts.json`

### Automatically add posts using shell

```bash
python manage.py shell
```

```bash
Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> import json
>>> from blog.models import Post
>>> with open('../readme_assets/posts.json') as f:
...   posts_json = json.load(f)
...
>>> for post in posts_json:
...   post = Post(title=post['title'], content=post['content'], author_id=post['user_id'])
...   post.save()
...
>>> exit()
```

## Run server and see the data

```bash
python manage.py runserver
```

## Testing Paginator on interactive shell

```bash
python manage.py shell
```

```bash
(InteractiveConsole)
>>> from django.core.paginator import Paginator
>>> posts = ['1', '2', '3', '4', '5']
>>> p = Paginator(posts, 2)
>>> p.num_pages
3
>>> for rng in p.page_range:
...   print(rng)
...
1
2
3
>>> p1 = p.page(1)
>>> p1
<Page 1 of 3>
>>> p1.number
1
>>> p1.object_list
['1', '2']
>>> p1.has_previous()
False
>>> p1.has_next()
True
>>> p1.next_page_number()
2
>>> exit()
```

## Implement Paginator

Without any imports...

`blog/views.py`

```py
...
class PostListView(ListView):
    ...
    paginate_by = 2
```

Test by `runserver` and visit `http://localhost:8000`.

Now try switching page to `http://localhost:8000/?page=2`

## Add next/prev links

`home.html`

```diff
...
{% block content %}
    {% for post in posts %}
        <article class="media content-section">
            ...
        </article>
    {% endfor %}

+   {% if is_paginated %}
+       <!-- Previous -->
+       {% if page_obj.has_previous %}
+           <a class="btn btn-outline-info mb-4" href="?page=1">First</a>
+           <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.previous_page_number }}">Previous</a>
+       {% endif %}
+
+       <!-- Pages -->
+       {% for num in page_obj.paginator.page_range %}
+           {% if page_obj.number == num %}
+               <a class="btn btn-info mb-4" href="?page={{ num }}">{{ num }}</a>
+           {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
+               <a class="btn btn-outline-info mb-4" href="?page={{ num }}">{{ num }}</a>
+           {% endif %}
+       {% endfor %}
+
+       <!-- Next -->
+       {% if page_obj.has_next %}
+       <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.next_page_number }}">Next</a>
+           <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.paginator.num_pages }}">Last</a>
+       {% endif %}
+
+   {% endif %}

{% endblock content %}
```

> **NOTICE**: There should be NO SPACES between the `|` character - `page_obj.number|add:'-3'`

You can now `runserver` and see!

## Display list of posts for a specific user

`views.py`

```diff
+from django.db.models.query import QuerySet
-from django.shortcuts import render
+from django.shortcuts import render, get_object_or_404
+from django.contrib.auth.models import User

 ...

+class UserPostListView(ListView):
+    model = Post
+    template_name = 'blog/user_posts.html' # <app>/<model>_<view_type>.html
+    context_object_name = 'posts'
+    paginate_by = 5
+
+    def get_queryset(self) -> QuerySet[Post]:
+        user = get_object_or_404(User, username=self.kwargs.get('username'))
+        return Post.objects.filter(author=user).order_by('-date_posted')
```

## Add URL

`blog/urls.py`

```py
...

from .views import (
    ...
    UserPostListView
)


urlpatterns = [
    ...
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
]
```

## Create template

`blog/templates/blog/user_posts.html`

<!-- prettier-ignore -->
```html
{% extends "blog/base.html" %}

<!-- 'content' is defined by the parent we extend -->
{% block content %}
    <h1 class="mb-3">Posts by {{ view.kwargs.username }} ({{ page_obj.paginator.count }})</h1>
    
    {% for post in posts %}
        <article class="media content-section">
            <img class="rounded-circle article-img" src="{{ post.author.profile.image.url }}" />
            <div class="media-body">
                <div class="article-metadata">
                <span class="mr-2">{{ post.author }}</span>
                <small class="text-muted">{{ post.date_posted | date:"F d, Y" }}</small>
                </div>
                <h2><a class="article-title" href="{% url 'post-detail' post.id %}">{{ post.title }}</a></h2>
                <p class="article-content">{{ post.content }}</p>
            </div>
        </article>
    {% endfor %}

    {% if is_paginated %}
        <!-- Previous -->
        {% if page_obj.has_previous %}
            <a class="btn btn-outline-info mb-4" href="?page=1">First</a>
            <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.previous_page_number }}">Previous</a>
        {% endif %}

        <!-- Pages -->
        {% for num in page_obj.paginator.page_range %}
            {% if page_obj.number == num %}
                <a class="btn btn-info mb-4" href="?page={{ num }}">{{ num }}</a>
            {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                <a class="btn btn-outline-info mb-4" href="?page={{ num }}">{{ num }}</a>
            {% endif %}
        {% endfor %}

        <!-- Next -->
        {% if page_obj.has_next %}
        <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.next_page_number }}">Next</a>
            <a class="btn btn-outline-info mb-4" href="?page={{ page_obj.paginator.num_pages }}">Last</a>
        {% endif %}

    {% endif %}

{% endblock content %}
```

Update the `home.html` as well to put the author link

```diff
-<a class="mr-2" href="#">{{ post.author }}</a>
+<a class="mr-2" href="{% url 'user-posts' post.author.username %}">{{ post.author }}</a>
```

Update the `post_detail.html` as well to put the author link

```diff
-<a class="mr-2" href="#">{{ object.author }}</a>
+<a class="mr-2" href="{{ url 'user-posts' object.author.username }}">{{ object.author }}</a>
```