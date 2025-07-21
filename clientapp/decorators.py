from django.http import HttpResponse

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.session.get('role') in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponse(" Access Denied")
        return wrapper
    return decorator
