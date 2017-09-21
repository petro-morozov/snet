from django import forms
from .models import UserPic, UPText
from django.forms import ValidationError

class UserPicForm(forms.ModelForm):
    image = forms.ImageField(label='')
    class Meta:
        model = UserPic
        fields = ['image']
        widgets = {'image': forms.FileInput(attrs={'class': 'myfieldclass'}),}

    def clean_image(self):
        image = self.cleaned_data.get('image',False)
        if image:
            if image._size > 1*1024*1024:
                raise ValidationError("Image file too large ( > 4mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")

class UPTextForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'mytextfieldclass'}), label='')
    class Meta:
        model = UPText
        fields = ['text']