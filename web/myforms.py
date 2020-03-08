import os

from django import forms
from django.core.exceptions import ValidationError

from . import models


def check_path(value):
    if not os.path.isdir(value):
        raise ValidationError('路径不存在！')


class ImportOldForm(forms.Form):
    old_blog_path = forms.CharField(
        max_length=1000,
        required=True,
        label='现有路径',
        help_text='请输入现有博客的路径',
        validators=[check_path],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    target_blog_path = forms.CharField(
        max_length=1000,
        required=True,
        label='目标路径',
        help_text='请输入要保存到的路径',
        validators=[check_path],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class BlogModelForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = models.BlogModel
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'path': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'layout': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateField(widget=forms.widgets.TextInput(attrs={'type': 'date', 'class': 'form-control'})),
            'update': forms.DateField(widget=forms.widgets.TextInput(attrs={'type': 'date', 'class': 'form-control'})),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CategoriesModelForm(forms.ModelForm):
    class Meta:
        fields = ['wrapper_folder', 'category_name']
        model = models.CategoriesModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  # Bootstrap 表单样式
            })


class TagsModelForm(forms.ModelForm):
    class Meta:
        fields = ['tag_name']
        model = models.TagsModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  # Bootstrap 表单样式
            })
