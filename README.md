# 10 - Create, Update and Delete Posts

https://www.youtube.com/watch?v=-s7e_Fy6NRU&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

Before moving to the main topic about `CRUD` for posts, we'll first go through what is a `Class-based` view

# Class-based view

- [`ListView`](#listview)
- [`DetailView`](#detailview)
- [`CreateView`](#createview)
- [`UpdateView`](#updateview)
- [`DeleteView`](#deleteview)

# `ListView`

`blog/views.py`

```py
from django.views.generic import ListView
from .models import Post

class PostListView(ListView):
    model = Post
```

## Use the class-based view urls

`blog/urls.py`

```diff
 from django.urls import path
+from .views import PostListView
 from . import views

 urlpatterns = [
-    path('', views.home, name='blog-home'),
+    path('', PostListView.as_view(), name='blog-home'),
     path('about/', views.about, name='blog-about'),
 ]
```

Try to `runserver`...

### Class-based default template naming pattern

**We would get an error that a template does not exist.**

By default, **class-based** views search for a certain naming pattern (i.e. `blog/post_list.html`)

**Naming Pattern**: `<app>/<model>_<view_type>.html`

#### Specifying a `template_name`

We can specify a template on class-based views,

```diff
class PostListView(ListView):
    model = Post
+   template_name = 'blog/home.html' # <app>/<model>_<view_type>.html
```

But we are still mising the `posts` in the context

#### Passing the variable to the tempalte

```diff
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<view_type>.html
+   context_object_name = 'posts'
```

#### Sorting the posts

```diff
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<view_type>.html
    context_object_name = 'posts'
+   ordering = ['-date_posted'] # post.date_posted, sort by latest
```

# `DetailView`

Update `views.py` to add a new class `PostDetailView`

```py
from django.views.generic import ListView, DetailView

...

class PostDetailView(DetailView):
    model = Post
```

## Update URL

```diff
 from django.urls import path
+from .views import PostListView, PostDetailView
 from . import views

 urlpatterns = [
     path('', PostListView.as_view(), name='blog-home'),
+    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
     path('about/', views.about, name='blog-about'),
 ]
```

`pk` = primary key

### Create template

Remember the default naming pattern: `<app>/<model>_<view_type>.html`

- app= `blog`
- model= `post`
- view_type= `detail`

`blog/templates/blog/post_detail.html`

<!-- prettier-ignore -->
```html
{% extends "blog/base.html" %}

<!-- 'content' is defined by the parent we extend -->
{% block content %}
    <article class="media content-section">
        <img class="rounded-circle article-img" src="{{ object.author.profile.image.url }}" />
        <div class="media-body">
            <div class="article-metadata">
                <a class="mr-2" href="#">{{ object.author }}</a>
                <small class="text-muted">{{ object.date_posted | date:"F d, Y" }}</small>
            </div>
            <h2 class="article-title">{{ object.title }}</h2>
            <p class="article-content">{{ object.content }}</p>
        </div>
    </article>
{% endblock content %}
```

Notice that the variable used is `object` instead of `post`. In this way, we would reduce the amount of code that we don't have to set the `context_object_name = 'post'`

Now try `runserver` and manually type-in the url `localhost:8000/post/1`

`home.html`

```diff
-<h2><a class="article-title" href="#">{{ post.title }}</a></h2>
+<h2><a class="article-title" href="{% url 'post-detail' post.id %}">{{ post.title }}</a></h2>
```

The `href` value will hold the name of the **PostDetail** page which is `post-detail` and as well as the parameter value. Then it will be passed as the `<int:pk>`

# `CreateView`

`views.py`

```py
...

from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)

...

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
```

## Update URL

`urls.py`

```py
...

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView
)

urlpatterns = [
    ...
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    ...
]
```

## Create template

This time, it has a different naming pattern, since `create` and `update` share similar pattern.

Create `blog/templates/blog/post_form.html`

`post_form.html`

<!-- prettier-ignore -->
```html
{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
    <div class="content-section">
        <form method="post">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Blog Post</legend>
                {{ form | crispy }}
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-info" type="submit">Post</button>
            </div>
        </form>
    </div>
{% endblock content %}
```

If we test now, and submit, we'll get an error that the **author id** is null. So every post needs to have an author.

Let's update `views.py`

```diff
class PostCreateView(CreateView):
    ...

+   def form_valid(self, form: BaseModelForm) -> HttpResponse:
+       form.instance.author = self.request.user
+       return super().form_valid(form)
```

When you test it now, it will create the post BUT will still give an error that it does not know where to **redirect**.

But this time, instead of redirect, we'll provide an **absolute path** so that the view itself would be the one to handle for us.

## URL `reverse`

`blog/models.py`

```diff
 ...
+from django.urls import reverse

 # Create your models here.
 class Post(models.Model):

     ...

+    def get_absolute_url(self):
+        return reverse('post-detail', kwargs={'pk': self.pk})
```

## Add login required for Post Detail

For function-based views, we just simple add a `@login_required` decorator.

But for **class-based** views, we will do it differently.

`blog/views.py`

```diff
+from django.contrib.auth.mixins import LoginRequiredMixin

 ...

-class PostCreateView(CreateView):
+class PostCreateView(LoginRequiredMixin, CreateView):
     model = Post
```

Now when you try to access **Post Detail** page without logging in, it will redirect to login page, with a `next=/post/new/`.

# `UpdateView`

`blog/views.py`

```py
...
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)
```

## Update URL

`blog/urls.py`

```py
...

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView
)

urlpatterns = [
    ...
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    ...
]
```

## Same Template

Like the `post/new/` The `post/<int:pk>/update/` will use the same template `post_form.html` by default.

You can now `runserver` and test your changes.

## Authorization

But wait, other users can also update some other posts that they do not own! Let's fix that.

`blog/views.py`

```py
...
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
...

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    ...

    def test_func(self) -> bool:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
```

> Observe the order of the inheritance and mind that **ALL** the `LoginRequiredMixin`, `UserPassesTestMixin` should always be first in line before the view type (i.e. `UpdateView`, `DeleteView`)

# `DeleteView`

`blog/views.py`

```py
...

from django.views.generic import (
    ...
    DeleteView
)

...
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # fallback to Home page

    def test_func(self) -> bool:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
```

## Update URLs

```py
...
from .views import (
    ...
    PostDeleteView
)

...

urlpatterns = [
    ...
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    ...
]
```

## Create template

By default, it will look into the `post_confirm_delete.html` template.

<!-- prettier-ignore -->
```html
{% extends "blog/base.html" %}

{% block content %}
    <div class="content-section">
        <form method="post">
            {% csrf_token %}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Delete Post</legend>
                <h2>Are you sure you want to delete the post "{{ object.title }}"?</h2>
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-danger" type="submit">Yes, Delete</button>
                <a class="btn btn-outline-secondary" href="{% url 'post-detail' object.id %}">Cancel</a>
            </div>
        </form>
    </div>
{% endblock content %}
```

## Creating navigation links to our CRUD

`base.html`

```diff
...
{% if user.is_authenticated %}
+   <a class="nav-item nav-link" href="{% url 'post-create' %}">New Post</a>
    <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
...
```

`post_detail.html`

```diff
<div class="article-metadata">
    <a class="mr-2" href="#">{{ object.author }}</a>
    <small class="text-muted">{{ object.date_posted | date:"F d, Y" }}</small>

+   {% if object.author == user %}
+       <div>
+           <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{% url 'post-update' object.id %}">Update</a>
+           <a class="btn btn-danger btn-sm mt-1 mb-1" href="{% url 'post-delete' object.id %}">Delete</a>
+       </div>
+   {% endif %}
</div>
```
