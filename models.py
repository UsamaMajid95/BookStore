from django.db import models
from django.contrib.auth.models import User

class customer(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True )
    email = models.CharField(max_length=200,null=True )
    phone = models.CharField(max_length=200,null=True )
    age = models.CharField(max_length=200,null=True )
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    avatar = models.ImageField(blank=True,null=True,default="person.png")

    def __str__(self):
        return self.name

class tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class book(models.Model):
    CATEGORY = (
        ('Classic', 'Classic'),
        ('Comic book', 'Comic book'),
        ('Fantasy', 'Fantasy'),
        ('Horror', 'Horror'),
    )
    name = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    tags = models.ManyToManyField(tag)
    category = models.CharField(max_length=200, null=True,choices= CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name



class order(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Delivered','Delivered'),
        ('In progress','In progress'),
        ('Out of order','Out of order'),
    )
    customer=models.ForeignKey(customer,null=True,on_delete=models.SET_NULL)
    book = models.ForeignKey(book,null=True,on_delete=models.SET_NULL)
    tags = models.ManyToManyField(tag)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS)
