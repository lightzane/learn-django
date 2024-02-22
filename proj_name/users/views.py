from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest # for typings
from .forms import UserRegistrationForm

def register(request: HttpRequest):

    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save() # save to database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please login.') # F-strings from Python 3.6+
            return redirect('login') # url pattern for our Blog home page
        # * Remember to pass the success message (i.e. in `base.html` template)

    else:
        # form = UserCreationForm()
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {
        'form': form
    })

@login_required
def profile(request):
    return render(request, 'users/profile.html')
