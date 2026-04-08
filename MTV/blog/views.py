from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Hashtag
from .forms import PostForm, Commentform

def home(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'home.html', {'Posts':posts})

def detail(request, post_id):
    post_detail=get_object_or_404(Post, pk=post_id)
    post_hashtag = post_detail.hashtag.all()
    return render(request, 'detail.html', {'post':post_detail, 'hashtag':post_hashtag})

def new(request):
    form=PostForm()
    return render (request, 'new.html', {'form':form})

def create(request):
    form=PostForm(request.POST, request.FILES)
    if form.is_valid():
        new_blog=form.save(commit=False)
        new_blog.date=timezone.now()
        new_blog.save()
        hashtags = request.POST['hashtags']
        hashtag_list=hashtags.split(',')

        for tag in hashtag_list:
            tag = tag.strip()
            new_hashtag=Hashtag.objects.get_or_create(hashtag=tag)
            new_blog.hashtag.add(new_hashtag[0])
        return redirect('blog:detail', new_blog.id)
    return redirect('blog:home')

def delete(request, post_id):
    delete_blog = get_object_or_404(Post, pk=post_id)
    delete_blog.delete()
    return redirect('blog:home')

def update_page(request, post_id):
    update_blog = get_object_or_404(Post, pk=post_id)
    return render(request, 'update.html',{'update_blog':update_blog})

def update_post(request, post_id):
    update_blog = get_object_or_404(Post, pk=post_id)
    update_blog.title= request.POST['title']
    update_blog.content = request.POST['content']
    update_blog.save()
    return redirect('blog:home')

def add_comment(request, post_id):
    blog = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = Commentform(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog
            comment.save()
            return redirect ('blog:detail', post_id)
    else:
        form = Commentform()
    return render(request, 'add_comment.html', {'form':form})