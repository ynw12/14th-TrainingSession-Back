from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
def home(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'home.html', {'Posts':posts})

def detail(request, post_id):
    post_detail=get_object_or_404(Post, pk=post_id)
    return render(request, 'detail.html', {'post':post_detail})

def new(request):
    form=PostForm()
    return render (request, 'new.html', {'form':form})

def create(request):
    form=PostForm(request.POST, request.FILES)
    if form.is_valid():
        new_blog=form.save(commit=False)
        new_blog.save()
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
