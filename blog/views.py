from django.shortcuts import render

# Create your views here.
from blog.models import BlogPost

def create_blog_view(request):
    return render(request,'blog/create_blog.html')