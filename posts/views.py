from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import Post, Group
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def index(request):
    latest = Post.objects.all()[:11]
    return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        postform = PostForm(request.POST)
        if postform.is_valid():
            in_new_post = postform.save(commit=False)
            in_new_post.author = request.user
            in_new_post.save()
            return redirect('index')
        return render(request, "new.html", {'form': postform})
    postform = PostForm()
    return render(request, "new.html", {'form': postform})
