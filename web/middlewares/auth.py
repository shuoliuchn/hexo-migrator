import re

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse


class AuthMiddleware(MiddlewareMixin):
    white_list = [reverse('web:login'), '/admin.*']

    def process_request(self, request):
        current_path = request.path
        for re_path in self.white_list:
            reg = r"^%s$" % re_path
            # 登录认证
            if re.search(reg, current_path):
                break
        else:
            username = request.session.get('username')
            if not username:
                return redirect('web:login')
