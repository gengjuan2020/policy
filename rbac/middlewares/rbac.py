from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import re
from django.shortcuts import HttpResponse, redirect


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求刚进入时候出发执行
        :param request:
        :return:
        """

        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        """
        current_url = request.path_info
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                # 白名单中的URL无需权限验证即可访问
                return None

        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)

        if not permission_list:
            # return redirect('/login/')
            return HttpResponse('未获取到用户权限信息，请登录！')

        flag = False

        for url in permission_list:
            reg = "^%s$" % url
            if re.match(reg, current_url):
                flag = True
                break

        if not flag:
            return HttpResponse('无权访问')
