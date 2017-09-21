from django import forms
from django.contrib.auth import authenticate, get_user_model, logout
from django.core.validators import EmailValidator

User = get_user_model()

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'myinputclass'}), label='Логин')
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'myinputclass'}), label='E-mail',
                             error_messages={'invalid': 'Попробуйте еще раз, только с нормальным mail-ом'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'myinputclass'}), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'myinputclass'}), label='Повторите пароль')
    class Meta:
        model = User
        fields = ['username', 'email', 'password','password2']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        if len(username) >= 15 :
            raise forms.ValidationError('Логин не должен быть длиннее 15 символов')
        if password != password2:
            raise forms.ValidationError('Пароли должны совпадать')
        email_qs = User.objects.filter(email=email)
        if email_qs:
            raise forms.ValidationError('Такой e-mail уже зарегестрирован')
        return super(UserRegisterForm, self).clean()



class UserLogForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'myinputclass'}),label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'myinputclass'}),label='Пароль')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Неверный логин или пароль')
            if not user.is_active:
                raise forms.ValidationError('User not active')
        return super(UserLogForm, self).clean()
