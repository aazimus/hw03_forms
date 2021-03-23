from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
   
    return render(
         request,
         'index.html',
         {'page': page,}
     )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def new_post(request):
    post_form = PostForm(request.POST or None)
    if not post_form.is_valid():
        return render(request, "new.html", {'form': post_form})
    in_new_post = post_form.save(commit=False)
    in_new_post.author = request.user
    in_new_post.save()
    return redirect('index') 

def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author = user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    post_count = post_list.count()
    

    return render(
         request,
         'profile.html',
         {'user':user,'page': page,
         'post_count': post_count,},
     )
    #return render(request, 'profile.html', {})


def post_view(request, username, post_id):
    # тут тело функции
    return render(request, 'post.html', {})


def post_edit(request, username, post_id):
    # тут тело функции. Не забудьте проверить, 
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    return render(request, 'new.html', {}) 