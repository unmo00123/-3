from django.contrib.auth import forms as auth_forms
from django import forms
from .models import Post


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text',)