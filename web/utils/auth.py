from django.shortcuts import redirect


def login_check(func):
    def inner(self, request, *args, **kwargs):
        if request.session.get('username'):
            return func(self, request, *args, **kwargs)
        else:
            return redirect('web:login')
    return inner
