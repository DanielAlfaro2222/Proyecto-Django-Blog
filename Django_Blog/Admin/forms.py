from django import forms
from Blog.models import Article


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'image', 'resume',
                  'content', 'author', 'category', 'state']
        widgets = {
            'name': forms.TextInput(attrs={
                'autofocus': 'true',
                'class': '',
            }),
            'state': forms.CheckboxInput(attrs={
                'class': '',
                'checked': 'true'
            })
        }
