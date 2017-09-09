from django.shortcuts import redirect


def login_required(view_func):
    """
    用户登陆判断装饰器
    """

    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('is_login'):
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect('/user/login')

    return wrapper
