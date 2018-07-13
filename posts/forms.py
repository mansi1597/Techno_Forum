from django import forms
from .models import Posts, Comments


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('project_title', 'project_description', 'skills_required', 'members_required')
        widgets = {'project_title': forms.TextInput(attrs={'class': 'form-control'}),
                   # 'project_description': forms.Textarea(attrs={'class': 'form-control',
                   #                                              'placeholder': 'Write something about your project',
                   #                                              'style': 'height:50px;'},),
                   'skills_required': forms.TextInput(attrs={'class': 'form-control'}),
                   'members_required': forms.TextInput(attrs={'class': 'form-control'}),
                   'project_description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent loader',
                                                                'placeholder': 'Write something about your project',
                                                                'style': 'height:50px;'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment_text',)
        widgets = {'comment_text': forms.Textarea(attrs={'class': 'btn-primary btn-simple text-dark ',
                                                         'placeholder': 'Write a comment..',
                                                         'style': 'height:80px; width:100%;',
                                                         })}
        labels = {'comment_text': ''}



