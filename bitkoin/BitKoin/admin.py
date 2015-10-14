from django.contrib import admin

from .models import UserPr,Transactions,Wallet,Sending,Receiving

admin.site.register(UserPr)
admin.site.register(Transactions)
admin.site.register(Wallet)
admin.site.register(Sending)
admin.site.register(Receiving)