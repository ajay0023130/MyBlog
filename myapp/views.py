from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage,\
PageNotAnInteger

from django.contrib.postgres.search import SearchVector
from .forms import CommentForm, SearchForm
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

from taggit.models import Tag # taging 
from django.db.models import Count
# Create your views here.


# for serching
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
            search=SearchVector('title', 'body'),).filter(search=query)
    return render(request,'myapp/post/search.html',{'form': form,'query': query,'results': results})

# this is Post List
def post_list(request, tag_slug=None):
    form = SearchForm()
    post_list = Post.published.all()
        
    query = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            post_list = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # paginate by 3 
    paginator = Paginator(post_list, 4)
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
        {'posts': posts,'tag': tag,'form':form})


#  this is Blog Detail page
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED,slug=post,publish__year=year,
    publish__month=month,
    publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request,'myapp/post/detail.html',{'post': post,
    'comments': comments,
    'form': form,'similar_posts': similar_posts })


# #class based View
# from django.views.generic import ListView
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 4
#     template_name = 'myapp/post/list.html'


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comments = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comments = form.save(commit=False)
        comments.post = post
        comments.save()

    return redirect('/')
    # return render(request, 'myapp/comment/comment.html',{'post': post,'comments': comments})