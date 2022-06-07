from django.db.models.signals import post_save
from django.contrib.auth.models import Group,User
from .models import customer

def customer_create_profile(sender,instance,created,**kwargs):
    if created:
       group = Group.objects.get(name='customer')
       instance.groups.add(group)
       customer.objects.create(
           user=instance,
           name=instance.username
       )
       print('customer profile created !')

post_save.connect(customer_create_profile,sender=User)