from django.shortcuts import render
# from django.http import HttpResponse

posts = [
    {
        'author': 'Lightzane',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Feb 21, 2024'
    },
    {
        'author': 'Lightzane',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Feb 22, 2024'
    },
]

# Create your views here.
def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {
        'title': 'About'
    })