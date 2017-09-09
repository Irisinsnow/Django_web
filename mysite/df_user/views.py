from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from df_goods.models import BrowseHistory
from df_orders.models import OrderBasic
from utils.decorators import login_required
from .tasks import register_success_send_email
from df_user.models import Passport, Address
from utils.get_hash import get_hash


@require_http_methods(['GET', 'POST'])
def register(request):
    """
    显示注册页面 并进行存入数据库 跳转
    """

    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        Passport.objects.add_one_passport(username=username, password=get_hash(password), email=email)
        # 发送邮件
        register_success_send_email.delay(username=username, password=password, email=email)
        # t跳转到登陆页面
        return redirect('/user/login/')


def check_user_name_exist(request):
    """
    检验用户名是否存在i
    """
    username = request.GET.get('username')
    passport = Passport.objects.get_one_passport(username=username)
    if passport is None:
        # 没有通行证 可以注册
        return JsonResponse({'res': 1})
    else:
        # 有通行证  不可以注册
        return JsonResponse({'res': 0})


def login(request):
    """
    显示登陆页面
    """
    if "username" in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''
    return render(request, 'login.html', {'username': username})


def login_check(request):
    """
    进行用户登录验证
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    passport = Passport.objects.get_one_passport(username=username, password=get_hash(password))
    if passport is None:
        # 没有通行证 不可以登陆
        return JsonResponse({'res': 0})
    else:
        # 登陆成功写入passport_id 读取pre_url_path
        next = request.session.get('pre_url_path', '/')
        jres = JsonResponse({'res': 1, 'next':next})
        remember = request.POST.get('remember')
        if remember == 'true':
            # 记住用户名,写入cookie
            jres.set_cookie('username', username, expires=24 * 60 * 60)
        request.session['is_login'] = True
        request.session['passport_id'] = passport.id
        request.session['username'] = username
        return jres


def logout(request):
    """
    退出登陆
    """
    request.session.flush()  # 请控股session信息
    return redirect('/')


@require_http_methods(["GET", "POST"])
@login_required
def address(request):
    """
    用户中心地址页面
    """
    passport_id = request.session.get('passport_id')
    if request.method == "POST":
        recipient_name = request.POST.get('uname')
        recipient_addr = request.POST.get('addr')
        recipient_phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        # 添加收货地址信息
        Address.objects.add_one_address(passport_id=passport_id, recipient_name=recipient_name,
                                        recipient_addr=recipient_addr, recipient_phone=recipient_phone,
                                        zip_code=zip_code)
    # 查询用户的默认收货地址信息
    addr = Address.objects.get_default_addr(passport_id=passport_id)
    # 刷新页面
    return render(request, 'user_center_site.html', {'addr': addr, 'page': 'addr'})


# /user/
@login_required
def user(request):
    """
    个人信息 页面
    """
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_addr(passport_id=passport_id)

    browse_li = BrowseHistory.objects_logic.get_browse_list_by_passport(passport_id=passport_id,
                                                                        limit=5)
    return render(request, 'user_center_info.html', {'addr':addr, 'page':'user',
                                                     'browse_li':browse_li})


# /user/order/
@login_required
def order(request, page_index):
    '''
    用户中心-订单页
    '''
    passport_id = request.session.get('passport_id')
    # 1.查询用户的订单信息 passport_id get_order_basic_info_by_passport(passport_id)
    order_basic_list = OrderBasic.objects_logic.get_order_basic_list_by_passport(passport_id=passport_id)

    # 分页
    panginator = Paginator(order_basic_list, 1)  # Paginator类的对象 page_range
    # 获取页码的列表
    pages = panginator.page_range
    # 获取总页数
    num_pages = panginator.num_pages
    # 当前页转化为数字
    page_index = int(page_index)

    # 1.如果总页数<=5
    # 2.如果当前页是前3页
    # 3.如果当前页是后3页,
    # 4.既不是前3页，也不是后3页
    if num_pages <= 5:
        pages = range(1, num_pages + 1)
    elif page_index <= 3:
        pages = range(1, 6)
    elif num_pages - page_index <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page_index - 2, page_index + 3)

    # 取第page_index页的内容 has_previous has_next number
    order_basic_list = panginator.page(int(page_index))  # Page类的对象 good_li.object_list Goods

    return render(request, 'user_center_order.html', {'page': 'order',
                                                      'order_basic_list': order_basic_list,
                                                        'pages':pages})
