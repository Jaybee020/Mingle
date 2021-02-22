from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .models import Profile


YEARS= [x for x in range(1900,2000)]
YESNO_CHOICES = (('male', 'male'), ('female', 'female'),('binary','binary'))

SEX_CHOICE= (('Men', 'Men'), ('Women', 'Women'),("Both","Both"))
BEHAVIOUR_CHOICE=(('Yes', 'Yes'), ('No', 'No'),("Doesn't matter","Doesn't matter"))
RELATIONSHIP_CHOICE=(('Serious Relationship', 'Serious Relationship'), ('Sexual Partner', 'Sexual Partner'),("Sugar Daddy","Sugar Daddy"),('Any','Any'))

class UserCreate(forms.Form):#specifies the fields we want in our forms 
    username =  forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))#represents html form of name input
    
    email = forms.EmailField(max_length=254,widget=forms.EmailInput(attrs={'class': 'form-control'}))#represent html form of input type email
    password=forms.CharField(strip=True,min_length=8,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    date_of_birth=forms.DateField(widget=forms.SelectDateWidget(years=YEARS),initial='2000-01-01')
    sex = forms.ChoiceField(choices=YESNO_CHOICES, initial='male', widget=forms.RadioSelect(attrs={'class':'form-check-input'}))
    date_joined=models.DateTimeField(default=timezone.now)
    location=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
    minimum_age=forms.IntegerField(min_value=18,max_value=99, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    maximum_age=forms.IntegerField(min_value=18,max_value=99, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    sex_interested_in= forms.ChoiceField(choices=SEX_CHOICE, initial='both', widget=forms.RadioSelect(attrs={'class':'form-check-input'}))
    drinking=forms.ChoiceField(choices=BEHAVIOUR_CHOICE, initial="Doesn't matter", widget=forms.RadioSelect(attrs={'class':'form-check-input'}))
    smoking=forms.ChoiceField(choices=BEHAVIOUR_CHOICE, initial="Doesn't matter", widget=forms.RadioSelect(attrs={'class':'form-check-input'}))
    interested_in=forms.ChoiceField(choices=RELATIONSHIP_CHOICE, initial="Any", widget=forms.RadioSelect(attrs={'class':'form-check-input'}))
    about=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta():
        model=User
        fields=['username','email','password','sex','date of birth','Confirm Password']


class ProfileUpdate(forms.ModelForm):
    

    class Meta():
        model=Profile#defines the model we want to modify
        #fields we would like to create for our forms
        fields=['image','about','minimum_age','maximum_age','location','interested_in','drinking','smoking','looking_for'] #tells us the data 
        widgets={
            'about':forms.Textarea(attrs={'class': 'form-control'}),
            'gender':forms.RadioSelect(attrs={'class':'form-check-input'}),
            'interested_in':forms.RadioSelect(attrs={'class':'form-check-input'}),
            'drinking':forms.RadioSelect(attrs={'class':'form-check-input'}),
            'smoking':forms.RadioSelect(attrs={'class':'form-check-input'}),
            'looking_for':forms.RadioSelect(attrs={'class':'form-check-input'})
        }
    

        