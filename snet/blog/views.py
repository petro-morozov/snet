from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from .forms import PostForm, CommentsForm
from .models import Post, Comments
from django.contrib.auth.decorators import login_required

def post_view(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            if form.is_valid:
                post_form = form.save(commit=False)
                post_form.fk = request.user
                post_form.is_main = True
                post_form.save()
                messages.success(request, 'Запись сохранена')
                return redirect('blog:post_view')
        except:
            messages.success(request, 'Некорректный формат, или изображение слишком большое (не больше 1 мб).')
            return redirect('blog:post_view')
    try:
        posts_list = Post.objects.filter(is_main = True).order_by('-timestamp')
        query = request.GET.get('q')
        if query:
            posts_list = posts_list.filter(Q(text__icontains=query) | Q(fk__username__icontains=query)).distinct()
        paginator = Paginator(posts_list, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context = {'form':form, 'posts':posts}
    except:
        context = {}
    return render(request, 'blog/blog_page.html', context)

def detail(request, post_id):
    post_detail = Post.objects.get(id = post_id)
    form = CommentsForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and request.user.is_authenticated:
        if form.is_valid:
            comment_form = form.save(commit=False)
            comment_form.fk = request.user
            comment_form.post = post_detail
            comment_form.save()
            messages.success(request, 'Запись сохранена')
            return redirect('blog:detail', post_id)
    comments_list = Comments.objects.filter(post = post_detail).order_by('-timestamp')
    paginator = Paginator(comments_list, 5)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    context = {'post_detail':post_detail, 'form':form, 'comments':comments}
    return render(request, 'blog/detail.html', context)

@login_required(login_url='/soc/login/')
def update(request, post_id):
    post_detail = Post.objects.get(id = post_id)
    form = PostForm(request.POST or None, instance=post_detail)
    if request.method == 'POST':
        if form.is_valid:
            post_form = form.save(commit=False)
            #post_form.fk = request.user
            post_form.save()
            messages.success(request, 'Изменено')
            return redirect('blog:post_view')
    context = {'post_detail':post_detail, 'form':form}
    return render(request, 'blog/post_form.html', context)


def delete(request, post_id):
    post_detail = Post.objects.get(id=post_id)
    post_detail.delete()
    messages.success(request, 'Запись удалена')
    return redirect('blog:post_view')