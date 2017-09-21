from django import forms
from .models import Message

class MsgForm(forms.ModelForm):
    msg = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Message
        fields = ['msg']
