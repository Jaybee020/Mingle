from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils import timezone
from django.urls import reverse
from PIL import Image


YESNO_CHOICES = (('male', 'male'), ('female', 'female'),('binary','binary'))
SEX_CHOICE= (('Men', 'Men'), ('Women', 'Women'),("Both","Both"))
BEHAVIOUR_CHOICE=(('Yes', 'Yes'), ('No', 'No'),("Doesn't matter","Doesn't matter"))
RELATIONSHIP_CHOICE=(('Serious Relationship', 'Serious Relationship'), ('Sexual Partner', 'Sexual Partner'),("Sugar Daddy","Sugar Daddy"),('Any','Any'))

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender= models.CharField(max_length=20)
    date_of_birth= models.DateField()
    location=models.CharField(max_length=50,default="")
    about=models.TextField(default="")
    interested_in=models.CharField(max_length=30,default="",choices=SEX_CHOICE )
    drinking=models.CharField(choices=BEHAVIOUR_CHOICE,default="",max_length=30)
    smoking=models.CharField(max_length=30,default="",choices=BEHAVIOUR_CHOICE)
    looking_for=models.CharField(max_length=30,default="",choices=RELATIONSHIP_CHOICE)
    minimum_age=models.PositiveIntegerField(default=18,validators=[MinValueValidator(18),MaxValueValidator(99)])
    maximum_age=models.PositiveIntegerField(default=99,validators=[MinValueValidator(18),MaxValueValidator(99)])
    image=models.ImageField(default='download.png',upload_to='profile_pics')#helps to create an image field
    like=models.ManyToManyField(User,related_name='profile_pages')


    def total_likes(self):
        return self.like.count()


    
    def __str__(self):
        return (self.user.username)



    def save(self,*args, **kwargs):#method called when your model gets saved
        super(Profile, self).save(*args, **kwargs)

        img=Image.open(self.image.path)#opens the image 
        if img.height > 320 or img.width >320 :#conditionto reshape the image
            output_size=(320,320) # 
            img.thumbnail(output_size)#helps to resize the image
            img.save(self.image.path) # overwrites the previous image
        


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)#allows you to post multiple as a single user
    pictures=models.ImageField(upload_to="profile_pics")
    date_posted=models.DateTimeField(default=timezone.now)


    def __str__(self):
        return (self.user.username)

    def get_absolute_url(self):#returns the url as a string for the create new stuff
        return reverse('user-pics',kwargs={'username': self.user.username})

    def save(self,*args, **kwargs):

        if not self.id and not self.pictures:
            return            

        super(Post, self).save(*args, **kwargs)

        image = Image.open(self.pictures)
        (width, height) = image.size
        if ( width>=height):
            factor = width/ height
            width=320
            height=width/factor
        else:
            factor = height / width
            height=298
            width=height/factor

       

        size = ( int(width ), int(height))
        image=image.resize(size,Image.ANTIALIAS)
        image.save(self.pictures.path)
        
