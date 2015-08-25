from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from blockchain import exchangerates

class UserPr(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()
    
    def __unicode__(self):
        return self.user.username
def creat_user_callback(sender, instance ,**kwargs):
    BitKoin , new =UserPr.objects.get_or_create(user = instance)
#post_save.connect(create_user_callback, User) 

    