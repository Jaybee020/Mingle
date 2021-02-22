from django.db import models
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from PIL import Image

#managers help to manage your models,you can define new mehtods in them
class ConversationManager(models.Manager):
    #Helps gets conversations considering the user as either initiator or intiator
    def by_user(self,user):
        query1=Q(Initiator=user)|Q(Recipient=user)
        query2=Q(Initiator=user)&Q(Recipient=user)
        returned_query=self.get_queryset().filter(query1).exclude(query2).distinct()
        return returned_query

    #Helps gets conversations between two users or creates a new if it doesn't exist 
    def get_or_new(self,sender_name,receiver_name):
        if sender_name==receiver_name:
            return None
        sender=User.objects.get(username=sender_name)
        receiver=User.objects.get(username=receiver_name)
        query1=Q(Initiator=sender)&Q(Recipient=receiver)
        query2=Q(Initiator=receiver)&Q(Recipient=sender)
        query =self.get_queryset().filter(query1|query2).distinct()
        if query.count()==1:
            return query
        elif query.count()>1:
            return query.order_by("date_created").first()
        else:
            if sender != receiver:
                obj=self.model(Initiator=sender,Recipient=receiver)
                obj.save()
                return obj
            return None

class Conversations(models.Model):
    Initiator=models.ForeignKey(User,on_delete=models.PROTECT,related_name="Initiator")
    Recipient=models.ForeignKey(User,on_delete=models.PROTECT,related_name="Recipient")
    date_created=models.DateTimeField(auto_now_add=True)
    last_contact=models.DateTimeField(default=timezone.now)
    last_message=models.TextField(default="",blank=True)

    objects=ConversationManager()

    def __str__(self):
        return f'{self.Initiator}-{self.Recipient}'


    


    class Meta():
        ordering=['-last_contact']






class ConversationMessage(models.Model):
    Conversation=models.ForeignKey(Conversations,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.PROTECT,related_name="sender")
    receiver=models.ForeignKey(User,on_delete=models.PROTECT,related_name="receiver")
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    attachment=models.ImageField(upload_to="attachments",blank=True)#the blank makes it optional 
    vocie_record=models.FileField(upload_to="voice record",blank=True)


    def __str__(self):
        return f'{self.sender}-{self.receiver}'

     


    class Meta():
        ordering=['-timestamp']


    #resizing the images when they are about to be saved
    def save(self,*args, **kwargs):

        super(ConversationMessage, self).save(*args, **kwargs)

        #making sure that if there is an attachment field it should do this before saving
        if self.attachment:
            image = Image.open(self.attachment)
            (width, height) = image.size
            
            "Max width and height 800"        
            if ( width>=height):
                factor = width/ height
                width=550
                height=width/factor
            else:
                factor = height / width
                height=550
                width=height/factor

            size = (int(width  / factor), int(height / factor))
            image=image.resize(size, Image.ANTIALIAS)
            image.save(self.attachment.path)
            


class Notifications(models.Model):
    Initiator=models.ForeignKey(User,on_delete=models.PROTECT,related_name="Notification_Initiator")
    Recipient=models.ForeignKey(User,on_delete=models.PROTECT,related_name="Notification_Recipient")
    content=models.TextField()
    date_notified=models.DateTimeField
