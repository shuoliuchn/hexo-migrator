import os
from django import forms
from django.core.exceptions import ValidationError


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
