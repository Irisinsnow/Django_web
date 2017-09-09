class UrlRecordMiddleware(object):
    """
    url记录中间件
    """
    exclude_path = ['/user/login/', '/user/login_check/', '/user/logout/',
                    '/user/register/', '/user/check_user_name_exist/']

    def process_view(self, request, view_func, *view_args,
                     **view_kwargs):
        if request.path not in self.exclude_path:
            request.session['pre_url_path'] = request.get_full_path()  # 记录带有参数的url
