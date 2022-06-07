from django.shortcuts import redirect

def usernotLogged(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func


def allowedUsers(allowedgroups=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group=None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowedgroups:
                return view_func(request,*args,**kwargs)
            else:
                return redirect('userprofile')
        return wrapper_func
    return decorator

def forAdmins(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group == 'admin':
            return view_func(request,*args,**kwargs)
        if group == 'customer':
            return redirect('userprofile')

    return wrapper_func