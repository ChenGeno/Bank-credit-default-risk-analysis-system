from django.shortcuts import render, redirect
from staff.models import Staff, Profile, StaffClean, Approval
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
import json
from django.core import serializers

# import predict_model.saved_model
import joblib
import pandas as pd
import numpy as np


# 引入logout模块

# Create your views here.

def apply_loan(request):
    try:
        user_id = request.user.id
        profile = Profile.objects.get(user_id=user_id)
        member_id = profile.member_id
        loan_id = '1064687'
        approver_id = '1'
        approval_obj = Approval(loan_id=loan_id, member_id=member_id, approver_id=approver_id)
        approval_obj.save()
        response_data = {}
    except:
        # 若发生异常
        response_data['code'] = 0
        response_data['msg'] = '提交申请失败，请重试 :)'
    else:
        # 若未发生异常
        response_data['code'] = 1
        response_data['msg'] = '申请成功！'
    return HttpResponse(json.dumps(response_data), content_type='application/json')




def bind_member(request):
    member_id = request.POST.get('member_id')
    loan_info_data = StaffClean.objects.filter(member_id=member_id)
    if len(loan_info_data) > 0:
        user_id = request.user.id
        user_profile = Profile.objects.get(user_id=user_id)
        user_profile.member_id = member_id
        user_profile.save()
        response_data = {'code': 1, 'msg': "绑定会员号成功，所有信息已经自动同步，现在去申请贷款吧~"}
    else:
        response_data = {'code': 0, 'msg': "该会员号不存在，请检查会员号或手动输入所有信息！"}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def dashboard(request):
    if request.method == "POST":
        approval_query = Approval.objects.order_by('update_time')  #[:2] limit 2
        dash_form = []
        for approval in approval_query:
            dash_form.append(approval.get_relevant_loan())
        context = {'dash_form': dash_form}
        print(context)
        print(context['dash_form'])
        print(context['dash_form'][0])
        return HttpResponse(json.dumps(context), content_type='application/json')
    return render(request, 'Staff/dashboard.html')


def landing(request):
    return render(request, 'Staff/landing.html')

def check_result(request):
    user_profile = Profile.objects.filter(user_id=request.user.id)[0]
    member_id = user_profile.member_id
    querySet = StaffClean.objects.filter(member_id=member_id).values()
    data = pd.DataFrame(list(querySet))
    u_d = ['id', 'loan_status', 'member_id']
    for i in u_d:
        del data[i]
    lr2 = joblib.load('static/data_file/rfc.pkl')
    rst = lr2.predict(data)
    print(f'预测结果：{lr2.predict(data)}')
    context = {'predict_rst': rst}
    return render(request, 'Staff/check_result.html', context)

def user_tour(request):
    ongoing_user = request.user  # 存储此时正在使用系统的user对象
    user_profile = Profile.objects.get(user_id=ongoing_user.id)  # 获取该用户的profile
    context = {'is_first_login': user_profile.is_first_login}
    # 若为第一次登录，则记录后将该字段改为false
    if context['is_first_login']:
        user_profile.is_first_login = False
        user_profile.save()
    return render(request, 'Staff/tour.html', context)


def step_info(request):
    if request.method == 'GET':
        return render(request, 'Staff/step_info.html')
    elif request.method == 'POST':
        user_surname = request.POST.get('surname')
        user_name = request.POST.get('name')
        response_data = {}
        try:
            user = request.user
            user.first_name = user_name
            user.last_name = user_surname
            user.save()
            login_user(request, user)  # 将保存后的用户写入session
        except:  # 若发生异常
            response_data['code'] = 0
            response_data['msg'] = '信息录入失败，请重试 :)'
        else:  # 若未发生异常
            response_data['code'] = 1
            response_data['msg'] = f'信息已成功录入，接下来去申请贷款吧{user_surname}{user_name}~'
        # 保存好数据后立即登录并返回主页面
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse("请使用GET或POST请求数据")



def personal_info(request):
    return render(request, 'Staff/personal_info.html')


def application_info(request):
    return render(request, 'Staff/application_info.html')


def basic_info(request):
    return render(request, 'Staff/basic_info.html')


def homepage(request):
    return render(request, 'Staff/homepage.html')


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.first_name = (user_register_form.cleaned_data['first_name'])
            new_user.last_name = (user_register_form.cleaned_data['last_name'])
            # 存储用户时，profile中的is_first_login默认为1
            new_user.save()


            response_data = {}
            response_data['code'] = 1
            response_data['msg'] = '恭喜您，注册成功！'
            # 保存好数据后立即登录并返回主页面
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            response_data = {}
            response_data['code'] = 0
            response_data['msg'] = '注册失败，请重试 :)'
            return HttpResponse(json.dumps(response_data), content_type='application/json')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'Staff/register.html')
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_login(request):
    if request.method == "POST":
        print("post")
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            print("valid")
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            print(data['username'], data['password'])
            # 检验账号、密码是否正确匹配数据库中的某个账户
            # 若均匹配则返回这个Staff对象
            staff = authenticate(username=data['username'], password=data['password'])
            response_data = {}
            if staff:
                # 将用户数据保存在 session 中, 实现了登录动作
                login_user(request, staff)
                # 获取关联表内容
                user_profile = Profile.objects.get(user_id=staff.id)

                if user_profile.is_first_login:
                    # 如果是第一次登录, 则跳转到向导页
                    response_data['code'] = 2  # 代表用户第一次登录
                    response_data['msg'] = f"亲爱的{data['username']}，欢迎加入速要贷！"
                else:
                    # 否则跳转到欢迎页
                    response_data['code'] = 1  # 代表老用户成功登录
                    response_data['msg'] = f"欢迎回来，{data['username']}。"
            else:
                response_data['code'] = 0  # 代表老用户成功登录
                response_data['msg'] = "用户名或密码错误。"
            return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        print("i am not post")
        return render(request, 'Staff/login_a.html')


def logout(request):
    logout_user(request)
    return redirect("/bc_gate/login/")


def index(request):
    return render(request, 'Staff/index.html')


def model_query(request):
    """
    # 添加表记录
    # 方式1 返回一个生成记录的对象
    staff_obj = Staff(id=1, sno="1370", password="1370", sname="chen", email="123@qq.com", sex="1")
    print(type(staff_obj))
    staff_obj.save()

    # 方式2 每一个模型表下都有一个叫object的模型管理器，可以对该表进行增删改查操作
    # create的返回值就是当前生成记录的对象
    staff_obj2 = Staff.objects.create(id=2, sno="1371", password="1371", sname="hao", email="123@qq.com", sex="1")
    print(str(staff_obj2))
    """

    # 查询
    # all方法
    staff_list = Staff.objects.all()  # 返回值为QuerySet类型
    print(staff_list, type(staff_list))

    # first, last方法(等同于直接取QuerySet的第一个或最后一个对象
    staff_obj = Staff.objects.first()  # 返回QuerySet的第一个对象, 调用者就是QuerySet对象
    staff_obj2 = Staff.objects.all()[0]
    print(staff_obj, type(staff_obj), staff_obj2)

    # filter()方法 过滤器方法查询符合条件的结果集 返回值:QuerySet对象
    staff_list2 = Staff.objects.filter(id=1)
    print(staff_list2)
    """
    # get()  有且只有一个查询结果时才有意义(若查到多条结果或无结果均报错), 返回值为model对象
    staff_obj3 = Staff.objects.get(id=1, sname='chen')

    # exclude(): 排除
    # order_by("id"): 按id排序,  order_by("a", "b"): 先按a字段排序，若a字段相等，按b字段排序  (调用者是QuerySet,返回值同)
    # reverse(): 对查询结果反向排序
    # count():返回数据库中匹配查询(QuerySet)的对象数量。
    # exists(): 如果QuerySet包含数据，就返回True，否则返回False 
    """

    """
    # values() 由QuerySet调用， 返回一个QuerySet，但QuerySet的内容是字典，key统一为字段名，值为每条检所记录对应该字段名的值
    all_name = Staff.objects.all().values("sname")
    print(all_name)  # 打印<QuerySet [{'sname': 'chen'}, {'sname': 'hao'}]>

    # value_list()  调用者为QuerySet, 但返回的QuerySet内容为元祖（仅保留值）
    all_name_tuple = Staff.objects.all().values_list("sno", "sex")
    print(all_name_tuple)  # 打印<QuerySet [('1370', 1), ('1371', 1)]>

    # distinct()  用于对QuerySet内的所有对象去重(去掉完全一样的QuerySet元素）
    only_email = Staff.objects.all().values_list("email").distinct()
    print(only_email)
    """
    return HttpResponse("ok，i will git you")


def predict_single_risk():
    querySet = StaffClean.objects.filter(member_id='1311441').values()
    data = pd.DataFrame(list(querySet))
    u_d = ['id', 'loan_status', 'member_id']
    for i in u_d:
        del data[i]
    lr2 = joblib.load('saved_model/rfc.pkl')
    print(lr2.predict(data))
    return 0
