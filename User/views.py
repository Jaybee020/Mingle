from django.shortcuts import render,redirect,get_object_or_404,reverse
from .forms import UserCreate,ProfileUpdate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Profile,Post
from django.views.generic import UpdateView
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView,CreateView
from .token_generator import account_activation_token
from django.contrib.auth import login,authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.core.mail import EmailMessage
from chat.views import get_order
from chat.models import Notifications



# Create your views here.

def register(request):
    if request.user.is_authenticated:
        raise PermissionDenied
    
    if request.method =="POST":
        form=UserCreate(request.POST)#posts the user name data inputed into the boxes
        
        if form.is_valid() and form.cleaned_data.get('password')==form.cleaned_data.get('confirm_password'):
            username=form.cleaned_data.get("username")#cleans the data by converting the forms to python files and getting the username
            email=form.cleaned_data.get("email")
            password=form.cleaned_data.get('password')
            
            sex=form.cleaned_data.get('sex')
            dob=form.cleaned_data.get('date_of_birth') 
            location=form.cleaned_data.get('location')
            minimum_age=form.cleaned_data.get('minimum_age')
            maximum_age=form.cleaned_data.get('maximum_age')
            
            sex_in=form.cleaned_data.get('sex_interested_in')
            drinking=form.cleaned_data.get('drinking')
            smoking=form.cleaned_data.get('smoking')
            interested_in=form.cleaned_data.get('interested_in')
            about=form.cleaned_data.get('about')
            
            def validate_password(password):#setting conditions for password
                min_length=8
                if len(password) < min_length:
                    form.add_error('password',"The new password must be at least {min_length} characters long." )

                # At least one letter and one non-letter
                first_isalpha = password[0].isalpha()
                if all(c.isalpha() == first_isalpha for c in password):
                    form.add_error('password',"The new password must contain at least one letter and at least one digit or" \
                                                " punctuation character.")
                
                return password
            
            password=validate_password(password)

            #making sure a username doesn't exist twice
            a=[]
            for i in User.objects.all():
                x=i.username.capitalize()
                a.append(x)

            if username.capitalize()  in a:
                form.add_error('username', 'The Username already exists')
            else:
                if minimum_age>=maximum_age:
                    form.add_error('maximum_age', 'Minimum age field supposed to be lower than maximum age field')
                    
                else:
                    new_user=User.objects.create_user(username=username.capitalize(),email=email,password=password,first_name=username)
                    Profile.objects.create(user=new_user ,gender=sex,date_of_birth=dob,location=location,minimum_age=minimum_age,maximum_age=maximum_age,interested_in=sex_in,drinking=drinking,smoking=smoking,about=about,looking_for=interested_in)
                    new_user.is_active = False #makes the user false so they dont have to login 
                    new_user.save()#saves the changes to the new_user
                    email_subject = 'Activate Your Account'#subject of the email to be sent 
                    current_site = get_current_site(request)
                    message = render_to_string('User/activate_account.html', {
                            'user': new_user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                            'token': account_activation_token.make_token(new_user),
                        })#message class defining the fields to be sent in the message
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(email_subject, message, to=[to_email])#email class to send the message
                    email.send()
                    return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
                    
                    
                    messages.success(request,f'Account Succesfully created for {username}!')#now go to ur base.html to make the messages show
                    return redirect('login')#redirects to the url with the name in the bracket
        elif form.cleaned_data.get('password') != form.cleaned_data.get('confirm_password'):
            form.add_error('confirm_password', 'The passwords do not match')

        
  


    else:
        form=UserCreate()
    
    return render(request,'User/Register.html',{'form':form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,f'Account Succesfully created for {user.username}!')
        return redirect('login')#redirects to the url with the name in the bracket
        
    else:
        return HttpResponse('Activation link is invalid!')



@login_required
def profile(request,username):
    # If no such user exists raise 404
    user = User.objects.get(username=username)
    
    convo=get_order(request)
    involved_user=User.objects.all()
    
    context={'user':user,'convo':convo,'involved_user':involved_user}
    return render(request,'User/confirm_profile.html',context)

@login_required    
def update_profile(request):
    if request.method=='POST':
        p_form=ProfileUpdate(request.POST,request.FILES,instance=request.user.profile)
        if p_form.is_valid():
            min_age=p_form.cleaned_data.get('minimum_age')
            max_age=p_form.cleaned_data.get('maximum_age')
            if min_age>=max_age:
                raise forms.ValidationError("The minimum age is greater than the maximum age")
                
            else:
                p_form.save()#saves the updated
                messages.success(request,f'Your account has been successfully updated!')#now go to ur base.html to make the messages show
                return redirect('profile',request.user.username)#redirects to the url with the name in the bracket

    else:#when the method is not POST i.e the button has not been pressed and it is just at the page
        
        p_form=ProfileUpdate(instance=request.user.profile)
        
    context={'p_form':p_form}  
    return render(request,'User/confirm_profile_update.html',context)


def user_pics(request,username):
    user=User.objects.get(username=username)
    context={'user':user,'post':Post.objects.all}
    return render(request,'User/confirm_user-pics.html',context)




class PostCreateView(LoginRequiredMixin ,CreateView):
    model=Post
    fields=['pictures']#tells us the fields we want to create
    #templates for this is post_form
    widgets={
            'pictures':forms.ClearableFileInput(attrs={'multiple': True})}
    
    
    def form_valid(self, form):#setting the author of the post before validating the form
        form.instance.user=self.request.user
        return super().form_valid(form)


def LikeView(request,pk):
    profile=get_object_or_404(Profile, id=request.POST.get('profile_id'))
    profile.like.add(request.user)
    username=profile.user.username
    Notifications.objects.create(Initiator=request.user,Recipient=profile.user,content=f'{request.user.username} flinged your profile')

    return HttpResponseRedirect(reverse('profile',args=[username]))#reverse is used to map the resposnse to the username and arguements are the variables in your url