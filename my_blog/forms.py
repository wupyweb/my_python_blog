from .models import Comment
from django import forms

from mdeditor.fields import MDTextFormField


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


# class CommentForm(forms.Form):
#     name = forms.CharField(label='y_name', max_length=100)
#     email = forms.EmailField()
#     body = MDTextFormField()
