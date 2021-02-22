import asyncio
import base64
import secrets
from django.core.files.base import ContentFile
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import  database_sync_to_async
from django.contrib.auth.models import User
from .models import ConversationMessage,Conversations
from django.utils import timezone

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected", event)

        #await asyncio.sleep(10)
        recipient_user=self.scope['url_route']['kwargs']['username']#method of getting the user from the url
        sender=self.scope['user']
        sender_username=sender.username
        conversation= await self.get_thread(sender_username,recipient_user)#the await converts to async
        
        chat_room=f'{conversation}'
        self.chat_room=chat_room
        
        print(conversation)
        
        print(recipient_user,sender_username)

        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })
 

    async def websocket_receive(self,event):
        #print("receive",event)
        #when a message is received from the websocket
        recipient_user=self.scope['url_route']['kwargs']['username']#method of getting the user from the url
        text=event.get('text',None)#getting the data received from the event
        recipient_user=self.scope['url_route']['kwargs']['username']#method of getting the user from the url
        sender=self.scope['user']
        sender_username=sender.username
        conversation= await self.get_thread(sender_username,recipient_user)#
        #changing the json into a dict and unpacking the various variables in the json sent
        loaded_text=json.loads(text)
        msg=loaded_text.get('message')
        attachment=loaded_text.get('file')
        user=self.scope['user']
        username=user.username
         
        
        
        if attachment:
            file_str,file_ext=attachment['data'],attachment['type']#splits into the data and the extension

            #creating a new file after decoding the file string sent and generating a random name using the secrets
            file_data=ContentFile(base64.b64decode(file_str),name=f'{secrets.token_hex(8)}.{file_ext}')

            #modifying the last_message fields and last_contact fields
           
            #creates a new message object
            message_created =await self.create_conversation_message(username,recipient_user,msg,file_data)

            files =await self.get_pictureurl(message_created.pk)#grab the file in the db
            caption="📷 Photo"
            convo= await self.update_last_contact(conversation,caption,timezone.now())

            myResponse={
                'message':msg,
                'username':username,
                'file':files
            }
        else:
            message_created =await self.create_conversation_message_2(username,recipient_user,msg)
            #print(message_created.content)
            convo= await self.update_last_contact(conversation,msg,timezone.now())
            myResponse={
                'message':msg,
                'username':username
                
                }

            
        
        #sends the message to the specific chatroom created
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type":'chat_message',
                "text":json.dumps(myResponse)

            }
        )

    #defines the chat message method 
    async def chat_message(self,event):
        #print('message',event)
        await self.send({
            "type":"websocket.send",
            "text":event['text']
        })
    
    async def websocket_disconnect(self,event):
        print("disconnected",event)

    #essential to convert your db methods to async mode for when you want to call them in an async function
    @database_sync_to_async 
    def get_thread(self,user,other_user):
        convo=Conversations.objects.get_or_new(sender_name=user,receiver_name=other_user)
        convo1=convo.first().pk
        return convo1

    @database_sync_to_async 
    def create_conversation_message(self,username,other_username,text,file):
        convo=Conversations.objects.get_or_new(sender_name=username,receiver_name=other_username)
        user=User.objects.get(username=username)
        other_user=User.objects.get(username=other_username)
        convo1=ConversationMessage.objects.create(Conversation=convo.first(),sender=user,receiver=other_user,content=text,attachment=file)
        return convo1

    @database_sync_to_async 
    def create_conversation_message_2(self,username,other_username,text):
        convo=Conversations.objects.get_or_new(sender_name=username,receiver_name=other_username)
        user=User.objects.get(username=username)
        other_user=User.objects.get(username=other_username)
        convo1=ConversationMessage.objects.create(Conversation=convo.first(),sender=user,receiver=other_user,content=text)
        return convo1


    @database_sync_to_async
    def get_pictureurl(self,message_id):
        message_sent=ConversationMessage.objects.get(pk=message_id)
        picture_url=message_sent.attachment.url
        return picture_url

    @database_sync_to_async
    def update_last_contact(self,convo_id,txt,time):
        convo=Conversations.objects.get(pk=convo_id)
        convo.last_contact=time
        convo.last_message=txt
        convo.save()
        return convo.pk