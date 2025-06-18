from django.shortcuts import render


posts = [
    {
        "author": "BenG",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "June 17, 2025"
    },
    {
        "author": "Jane Doe",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "June 18, 2025"
    }
]

# Create your views here.
def home(request):
    context = {
        "posts": posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {"title": "About"})