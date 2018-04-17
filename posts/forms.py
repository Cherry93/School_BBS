from django import forms

from .models import Post,User



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [ 'title','content_html','category','tags']


class AvaForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

class UsrForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class SigForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['signature']

class QqForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['qq_num']

class MaForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['major']

class PhForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone']