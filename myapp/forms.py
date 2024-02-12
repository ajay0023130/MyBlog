from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-contro','placeholder': 'Enter Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'custom-class','placeholder': 'Enter Your Email'}),
            'body': forms.Textarea(attrs={'class': 'custom-class', 'rows': 5,'placeholder': 'Join the discussion and leave a comment!'}),
        }
        required = {
            'name': True,
            'email': True,
            'body': True,
        }
       

class SearchForm(forms.Form):
    query = forms.CharField()