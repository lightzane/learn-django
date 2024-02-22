# 08 - User Profile and Picture

https://www.youtube.com/watch?v=FdVuKt_iuSI&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

## Create custom User model

Extend the built-in User model from Django

`users/models.py`

```py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics') # upload to `profile_pics/` directory

    def __str__(self) -> str:
        return f'{self.user.username} Profile'
```

## Make Migrations

Since we did database model changes, we need to make migrations.

```bash
python manage.py makemigrations
```

**Output**

```bash
SystemCheckError: System check identified some issues:

ERRORS:
users.Profile.image: (fields.E210) Cannot use ImageField because Pillow is not installed.
        HINT: Get Pillow at https://pypi.org/project/Pillow/ or run command "python -m pip install Pillow".
```

`Pillow` is a library for working on images with Python

### Install Pillow

```bash
pip install pillow
```

Rerun the `makemigrations` command

**Output**

```bash
Migrations for 'users':
  users\migrations\0001_initial.py
    - Create model Profile
```

## Apply Migrations

```bash
python manage.py migrate
```

**Output**

```bash
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions, users
Running migrations:
  Applying users.0001_initial... OK
```

## Register model for Admin page

`users/admin.py`

```py
from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(User)

```

Run the server and check **Admin** page and see the `Profile` added under `Users` section.

**Add Profile** then exercise query in the `python manage.py shell`

```bash
(InteractiveConsole)
>>> from django.contrib.auth.models import User
>>> user = User.objects.filter(username='lightzane').first()
>>> user
<User: lightzane>
>>> user.profile
<Profile: lightzane Profile>
>>> user.profile.image
<ImageFieldFile: profile_pics/lightzane.png>
>>> user.profile.image.width
420
>>> user.profile.image.url
'/profile_pics/lightzane.png'
```

### Set image upload location

Currently, we set the image to be uploaded in the `/profile_pics/` path. But if there are multiple users, it will clutter in the project directory - or users app directory.

Let's change it on the `settings.py` and add the following keys:

```py
from pathlib import Path # should already exist in `settings.py`

...

# Store uploaded files here
MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media') # directory URL
MEDIA_URL = '/media/' # public URL
```

This should now create a `profile_pics` directory inside the `media` sub-directory

#### Re-upload image

In admin page, let's delete the profile images. If you notice, it may not delete the actual image file in the directory. Let's manually delete the existing `profile_pics/*.jpg`

Once you upload, you'll be able to see that it's now stored in the `proj_name/media/profile_pics` directory.

> You may want to add `media/` path in `.gitignore`

## Update profile template

Snippet here: https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/snippets/profile.html

`profile.html`

<!-- prettier-ignore -->
```html
{% extends "blog/base.html" %}
{% load crispy_forms_tags %}
{% block content %}
    <!-- `user` variable is built-in within Django -->
    <div class="content-section">
        <div class="media">
            <img class="rounded-circle account-img" src="{{ user.profile.image.url }}">
            <div class="media-body">
            <h2 class="account-heading">{{ user.username }}</h2>
            <p class="text-secondary">{{ user.email }}</p>
            </div>
        </div>
        <!-- FORM HERE -->
    </div>
{% endblock content %}
```

> Note that this uploading of files approach is only for Development. **This is not recommended for Production**.

### Update `urls.py` so we can reference it into templates

Django documentation about serving files uploaded by a user during development:<br>
https://docs.djangoproject.com/en/5.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development

For example, if your `MEDIA_URL` is defined as `media/`, you can do this by adding the following snippet to your `ROOT_URLCONF`:

**Snippet from the documentation site**

```py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

`proj_name/urls.py`

```diff
 from django.contrib import admin
 from django.contrib.auth import views as auth_views
 from django.urls import path, include
 from users import views as user_views

+from django.conf import settings
+from django.conf.urls.static import static

 urlpatterns = [
     ...
 ]

+if settings.DEBUG:
+    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

You can now `runserver` and login to `localhost:8000/profile`

Feel free to upload a `default.jpeg` manually in the `/media/` directory.

## Signals

**Signals** in Django are similar to `events`.

In this scenario, when we register a user, we want to also automatically set the default image for their profile. Since the `user` and `profile` have a `1-1` relationship.

### Create `signals.py` under users subdirectory

```py
from django.db.models.signals import post_save # signal
from django.contrib.auth.models import User # sender
from django.dispatch import receiver # receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```

### Update `users/apps.py`

```diff
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

+   def ready(self) -> None:
+       import users.signals # import here based on documentation as well to prevent side-effects
```

Now try to `runserver` and register a new user. Then verify that there is a default profile created.
