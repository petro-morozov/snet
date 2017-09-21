from django import forms
from django.forms import ValidationError
from .models import Post, Comments

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'post_textarea_class'}), label='')
    image = forms.ImageField(required = False, label='', widget=forms.FileInput(attrs={'class':'post_image_class'}))
    class Meta:
        model = Post
        fields = ['text', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image',False)
        if image:
            if image._size > 1*1024*1024:
                raise ValidationError("Image file too large ( > 4mb )")
            return image
        else:
            raise ValidationError("Couldn't read uploaded image")


class CommentsForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'post_textarea_class'}), label='')
    class Meta:
        model = Comments
        fields = ['text']