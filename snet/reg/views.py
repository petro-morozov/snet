from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLogForm, UserRegisterForm

def register(request):
    current_user = request.user
    if current_user.is_active:
        return redirect('/reg/logout')
    title = 'Зарегистрироваться'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('user_page:user_page', user_id=request.user.id)
    context = {'form':form, 'title':title,}
    return render(request, 'reg/form.html', context)

def login_form(request):
    title = 'Логин'
    form = UserLogForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('user_page:user_page', user_id=request.user.id)
    return render(request, 'reg/form.html', {'form':form, 'title':title,})

def logout_form(request):
    logout(request)
    return redirect('reg:login')

def user_settings(request):
    context = {}
    return render(request, 'reg/user_settings.html', context)