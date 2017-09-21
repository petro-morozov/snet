from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from fellows.models import Fellows, ShowFellows
from django.db.models import Q
from blog.forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post
from .models import UserPic, UPText
from .forms import UserPicForm, UPTextForm

User = get_user_model()

def user_page(request, user_id):
    user = User.objects.filter(id=user_id).get()
    form = PostForm(request.POST or None, request.FILES or None)
    pic_form = UserPicForm(request.POST or None, request.FILES or None)
    up_text_form = UPTextForm(request.POST or None, auto_id=False)

    try:
        user_already_have_a_pic = UserPic.objects.get(user=user)
    except:
        user_already_have_a_pic = False
    if user_already_have_a_pic:
        pic_form = UserPicForm(request.POST or None, request.FILES or None, instance=user_already_have_a_pic)
    try:
        user_already_have_a_text = UPText.objects.get(user=user)
    except:
        user_already_have_a_text = False
    if user_already_have_a_text:
        up_text_form = UPTextForm(request.POST or None, instance=user_already_have_a_text, auto_id=False)
    context = {'pic_form': pic_form, 'form': form, 'up_text_form':up_text_form}

    if request.method == 'GET':
        user = User.objects.filter(id = user_id).get()
        try:
            s = ShowFellows.objects.get(user=user)
        except:
            s = None
        #user.status = 'logged in' if hasattr(user, 'logged_in_user') else 'not logged in'
        user_fellows = Fellows.objects.filter(first_user = user)
        if request.user.is_authenticated:
            try:
                user_fellows_check = Fellows.objects.get(first_user=request.user, second_user=user)
                not_yet_fellows = False
            except:
                not_yet_fellows = True
        else:
            not_yet_fellows = False
        posts_list = Post.objects.filter(u_page=user_id).order_by('-timestamp')
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
        try:
            user_page_text = UPText.objects.get(user = user)
        except ObjectDoesNotExist:
            user_page_text = False

        context = {'user': user, 'user_fellows': user_fellows,
                   'not_yet_fellows': not_yet_fellows, 's': s, 'posts': posts, 'pic_form': pic_form, 'form': form,
                   'up_text_form':up_text_form, 'user_page_text': user_page_text,}

    if request.method == 'POST' and request.user.is_authenticated:
        if 'user_pic' in request.POST:
            try:
                if user_already_have_a_pic and pic_form.is_valid:
                    pic_form = pic_form.save(commit=False)
                    pic_form.user = request.user
                    pic_form.save()
                    messages.success(request, 'Изменено')
                    return redirect('user_page:user_page', request.user.id)
                elif pic_form.is_valid:
                    pic_form = pic_form.save(commit=False)
                    pic_form.user = request.user
                    pic_form.save()
                    messages.success(request, 'Сохранено')
                    return redirect('user_page:user_page', request.user.id)
            except:
                messages.success(request, 'Некорректный формат, или изображение слишком большое (не больше 1 мб).')
                return redirect('user_page:user_page', request.user.id)
        elif 'user_post' in request.POST:
            try:
                if form.is_valid:
                    post_form = form.save(commit=False)
                    post_form.fk = request.user
                    post_form.u_page = user
                    post_form.save()
                    messages.success(request, 'Запись сохранена')
                    return redirect('user_page:user_page', user_id)
            except:
                messages.success(request, 'Некорректный формат, или изображение слишком большое (не больше 1 мб).')
                return redirect('user_page:user_page', request.user.id)
        elif 'u_p_text' in request.POST:
            if request.user == user:
                if up_text_form.is_valid:
                    text_form = up_text_form.save(commit=False)
                    text_form.user = request.user
                    text_form.save()
                    return redirect('user_page:user_page', user_id)
            else:
                messages.success(request, 'Вы не можете изменять эту запись на чужих страницах')
                return redirect('user_page:user_page', user_id)

    return render(request, 'user_page/page.html', context)

def show_all_users(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request, 'user_page/all_users.html', context)

@login_required(login_url='/soc/login/')
def show_fellows_list(request):
    u = User.objects.get(id = request.user.id)
    try:
        s = ShowFellows.objects.get(user = u)
        if request.is_ajax:
            if s.show == True:
                s.show = False
                s.save()
            elif s.show == False:
                s.show = True
                s.save()
    except ObjectDoesNotExist:
        s = ShowFellows.objects.create(user=u, show=False)
        s.save()
    return render(request, 'user_page/page.html', {})

def fellows_list(request, user_id):
    user=User.objects.get(id = user_id)
    user_fellows = Fellows.objects.filter(first_user=user)
    return render(request, 'user_page/fellows_list.html', {'user_fellows':user_fellows})

