from django.shortcuts import render,get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger
# Create your views here.


def post_list(request):
    post_list = Post.published.all()
    # paginate by 3 
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
        # If page_number is not an integer deliver the first page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
        'myapp/post/list.html',
        {'posts': posts})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,slug=post,publish__year=year,
    publish__month=month,
    publish__day=day)
    return render(request,'myapp/post/detail.html',{'post': post})