from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        
class MyArticleAdminForm(forms.ModelForm):
    def clean_name(self):
        print('GHJDT')
        # do something that validates your data
        return self.cleaned_data["name"]