from django import forms

class BlogForm(forms.Form):
    title = forms.CharField()
    slug = forms.CharField()
    content = forms.CharField(widget=forms.Textarea) 
