from django import forms
from .models import Message


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'class': 'btn-primary btn-simple text-dark ',
                                                          'placeholder': 'Write a message..',
                                                          'style': 'height:80px; width:100%;',
                                                          })}
        labels = {'text': ''}
