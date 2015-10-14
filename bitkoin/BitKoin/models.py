# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# from blockchain import exchangerates

class UserPr(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField()

    def __unicode__(self):
        return self.user.username


def creat_user_callback(sender, instance, **kwargs):
    BitKoin, new = UserPr.objects.get_or_create(user=instance)


# post_save.connect(create_user_callback, User)
class Wallet(models.Model):
    wallet_id = models.AutoField(primary_key=True)
    user_wallet = models.ForeignKey('UserPr')
    balance = models.DecimalField(max_digits=19, decimal_places=10)


class Transactions(models.Model):
    trans_id = models.AutoField(primary_key=True)
    trans_type = models.TextField()
    u_trans = models.ForeignKey('UserPr')
    t_time = models.DateTimeField()


class Sending(models.Model):
    wallet_id_send = models.ForeignKey('Wallet')
    send = models.CharField(blank=False, max_length=26)
    trans_id_send = models.ForeignKey('Transactions')
    t_time_send = models.DateTimeField()


class Receiving(models.Model):
    wallet_id_rec = models.ForeignKey('Wallet')
    rec = models.CharField(blank=False, max_length=26)
    trans_id_rec = models.ForeignKey('Transactions')
    t_time_rec = models.DateTimeField()
