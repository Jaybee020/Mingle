from django import forms

class MessageInput(forms.Form):
    message_input=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'message_sent '}))
    attachment=forms.ImageField(required=False ,widget=forms.FileInput(attrs={'class':'hidden','onchange':'previewfile()'}))