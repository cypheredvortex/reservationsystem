from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def proprietaire_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.userprofile.role != 'proprietaire':
            messages.error(request, 'Access denied. Property owner privileges required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.userprofile.role != 'client':
            messages.error(request, 'Access denied. Client privileges required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view