from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Conversations,ConversationMessage,Notifications
from .forms import MessageInput
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.core import serializers
import json
from django.utils import dateformat

# Create your views here.
def get_order(request):
    convo=Conversations.objects.filter(Q(Initiator=request.user)|Q(Recipient=request.user))
    return convo

@login_required
def chat(request,username):
    receiver_username=username
    involved_users=User.objects.all()
    sender_username=request.user.username
    target_user=User.objects.get(username=receiver_username)
    if request.user != target_user :
        conversation=Conversations.objects.get_or_new(sender_username,receiver_username)
        print(conversation)
        if request.method =='POST':
            m_form=MessageInput(request.POST,request.FILES)
            if m_form.is_valid():
                text=m_form.cleaned_data.get('message_input')
                file=m_form.cleaned_data.get('attachment')
                ConversationMessage.objects.create(Conversation=conversation.first(),sender=request.user,receiver=target_user,content=text,attachment=file)
                
        else:
            m_form=MessageInput()
    else:
        return HttpResponse("Are you mad why will you want to send yourself a message")
    
    
    convo=Conversations.objects.filter(Q(Initiator=request.user)|Q(Recipient=request.user))
    
    #helps to filter the messages database for messages only between only the requested user and traget user 
    total_messages=ConversationMessage.objects.filter(Q(sender=request.user ,receiver=target_user) | Q(sender=target_user,receiver=request.user ))
   
   
    
    return render(request,'chat/chat_room.html',{'user':target_user,'message':total_messages,'form':m_form,'convo':convo,'involved_user':involved_users})


def messages_db(request):
    convo=Conversations.objects.filter(Q(Initiator=request.user)|Q(Recipient=request.user))
    dataset=[]
    for convos in convo:
        data={'user':"",'last_message':'','last_contact':"","user_img_path":""}
        if convos.Recipient != request.user:
            user=convos.Recipient.username
            last_message=convos.last_message
            last_contact= convos.last_contact
            
            user_img=convos.Recipient.profile.image.url
            data['user']=user
            data['last_message']=last_message
            data["last_contact"]=str(last_contact)[0:16]
            data["user_img_path"]=user_img
            dataset.append(data)
        else:
            user=convos.Initiator.username
            last_message=convos.last_message
            last_contact=convos.last_contact
            
            user_img=convos.Initiator.profile.image.url
            data['user']=user
            data['last_message']=last_message
            data["last_contact"]=str(last_contact)[0:16]
            data["user_img_path"]=user_img
            dataset.append(data)
            print(last_contact)
           

   
    

    return JsonResponse(dataset,safe=False)

def notifications(request):
    notify=Notifications.objects.filter(Recipient=request.user).all()
    convo=Conversations.objects.filter(Q(Initiator=request.user)|Q(Recipient=request.user))
    
    if notify.count()==1:
        notify=notify.first()
        return render(request,'chat/notification_for_one.html',{'notify':notify,'convo':convo})
    
    elif notify.count()==0:
        return render(request,'chat/notification_for_none.html',{'notify':notify,'convo':convo})

    else:
        return render(request,'chat/notification.html',{'notify':notify,'convo':convo})
    

def ajax(request):
    return render(request,'chat/ajax.html')