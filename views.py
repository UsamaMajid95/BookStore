from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from .forms import *
# from .filters import orderfilters
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import usernotLogged , allowedUsers,forAdmins
from django.contrib.auth.models import Group
from django.conf import settings
import requests

@login_required(login_url='login')
# @allowedUsers(allowedgroups=['admin'])
@forAdmins
def home(request):
    customers = customer.objects.all()
    orders = order.objects.all()
    t_order = orders.count()
    p_order = orders.filter(status='Pending').count()
    d_order = orders.filter(status='Delivered').count()
    In_order = orders.filter(status='In progress').count()
    out_order = orders.filter(status='Out of order').count()
    t_customers = customers.count()



    context = {
        'customers':customers,
        'orders':orders,
        't_order':t_order,
        'p_order':p_order,
        'd_order':d_order,
        'In_order':In_order,
        'out_order':out_order,
        't_customers':t_customers,


    }
    return render(request,'about.html',context)

@login_required(login_url='login')
def books(request):
    books = book.objects.all()
    return render(request, 'books.html',{'books':books})


@login_required(login_url='login')
def Customer(request,pk):
    customers = customer.objects.get(pk=pk)
    order_c = customers.order_set.all()
    total_orders = order_c.count()

    context={
        'customers': customers,
        'order_c': order_c,
        'total_orders':total_orders,

    }

    return render(request,'customer.html',context)

def download(request):
    return HttpResponse("download page")

# def Create(request):
#     form = OrderForm()
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     context={'form':form }
#     return render(request, 'create.html',context)
@login_required(login_url='login')
def Create(request,pk):
    orderformset = inlineformset_factory(customer,order,fields=('book','status'))
    customers = customer.objects.get(pk=pk)
    formset = orderformset(queryset=order.objects.none(),instance=customers)
    if request.method == 'POST':
        formset = orderformset(request.POST,instance=customers )
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset }
    return render(request, 'create.html',context)


@login_required(login_url='login')
@allowedUsers(allowedgroups=['admin'])

def Update(request,pk):
    orders = order.objects.get(pk=pk)
    form = OrderForm(instance=orders)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=orders)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={
        'form':form
    }
    return render(request, 'create.html',context)


@login_required(login_url='login')
# @allowedUsers(allowedgroups=['admin'])
@forAdmins
def Delete(request,pk):
    orders = order.objects.get(pk=pk)
    form = OrderForm(instance=orders)
    if request.method == 'POST':
        orders.delete()
        return redirect('/')
    context={
        'orders':orders
    }
    return render(request,'delete.html',context)


@usernotLogged
def Register(request):
        form = CreateNewUser()
        if request.method == 'POST':
            form = CreateNewUser(request.POST)
            if form.is_valid():
                recaptcha_response = request.POST.get('g-recaptcha-response')
                data={
                    'secret':settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response':recaptcha_response
                }
                r=requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                result=r.json()
                if result['success']:
                    user= form.save()
                    username = form.cleaned_data.get('username')
                    messages.success(request, username + "Created successfully")
                    return redirect('login')
                else:
                    messages.error(request,'Invaild recaptcha please try again')

        context = {
            'form':form,

        }
        return render(request, 'register.html', context)

@usernotLogged
def Login(request):

        if request.method == 'POST':
           username=request.POST.get('username')
           password = request.POST.get('password')
           user = authenticate(request,username=username,password=password)
           if user is not None:
                login(request,user)
                return redirect('home')
           else:
                messages.info(request,'Credentials error')
        context = {}
        return render(request,'login.html', context)


def userLogout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowedUsers(allowedgroups=['customer'])
def UserProfile(request):
    orders=request.user.customer.order_set.all()
    t_order = orders.count()
    p_order = orders.filter(status='Pending').count()
    d_order = orders.filter(status='Delivered').count()
    In_order = orders.filter(status='In progress').count()
    out_order = orders.filter(status='Out of order').count()

    context = {
        'orders': orders,
        't_order': t_order,
        'p_order': p_order,
        'd_order': d_order,
        'In_order': In_order,
        'out_order': out_order,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def Profile_Info(request):
    customers=request.user.customer
    form = CustomerForm(instance=customers)
    if request.method == 'POST':
        form=CustomerForm(request.POST,request.FILES,instance=customers)
        if form.is_valid():
           form.save()
    context = {'form':form}
    return render(request, 'profile_info.html', context)