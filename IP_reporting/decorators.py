# ip_reporting/decorators.py
from functools import wraps
from django.core.exceptions import PermissionDenied

def custom_permission_required(permission_codename):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.has_perm(f'ip_reporting.{permission_codename}'):
                print("denied")
                raise PermissionDenied
            print("ok")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
