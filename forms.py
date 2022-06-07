from django.forms import ModelForm
from.models import order,customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = order
        fields='__all__'

class CustomerForm(ModelForm):
    class Meta:
        model = customer
        fields='__all__'
        exclude=['user']


class CreateNewUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']