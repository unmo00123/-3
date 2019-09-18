# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView as cf
from django.urls import reverse_lazy
from .models import Post, LikePost  # Like
from .forms import LoginForm as r
from .forms import PostForm

app_name='blog'


def top_page(request):
    return render(request, 'blog/top_page.html', {})


def page_under_construction(request):
    return render(request, 'blog/page_under_construction.html', {})


class loginView(LoginView):
    form_class = r
    template_name = "blog/login.html"
    reverse_lazy('login')


class logoutView(LoginRequiredMixin, LogoutView):
    template_name = "blog/logout.html"


@login_required
def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            # ここで一気に集計テーブルへもデータを埋め込みます
            s = LikePost.objects.create(post_id=post.id, count=0)
            s.save()
    else:
        form = PostForm()

    """ 
        like_count = LikePost.objects.count() 
        これはレコード数すべてをカウントします。
        方法はいくつかありますが、ここでは集計テーブルとしてLIKEを使用してみましょう。
        LIKEされる都度、集計データを更新します。likeメソッドを確認してください。
        これで、外部結合をしてデータを取ってきます。
        SELECT * FROM `blog_post`AS p LEFT JOIN blog_likepost AS l ON p.id=L.post_id
        
    """
    # like_count = LikePost.objects.count(post__id)
    # posts = Post.objects.order_by('-created_date')[:5]
    posts = Post.objects.select_related('likepost').values('likepost__count',
                                                           'text',
                                                           'created_date',
                                                           'title',
                                                           'id').order_by('-created_date')[:5]
    return render(request,'blog/index.html', {'posts':posts, 'form':form})


class CreateView(cf):
    form_class = UserCreationForm
    template_name = "blog/create.html"
    success_url = reverse_lazy("blog:login")


@login_required
def like(requests):
    if requests.method == 'POST':
        statue = LikePost.objects.filter(post_id=requests.POST['post_id']).first()
        if LikePost.objects.filter(post_id=requests.POST['post_id']).exists():
            statue.count += 1
            statue.save()
        else:
            s = LikePost.objects.create(post_id = requests.POST['post_id'], count=1)
            s.save()
        # LikePost.objects.create()
    return redirect('blog:index')
