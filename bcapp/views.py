from django.shortcuts import render, HttpResponse
from bcapp.models import Staff

# Create your views here.

def homepage(request):
    return render(request, 'Staff/homepage.html')

def login(request):
    if request.method == "POST":
        sno = request.POST.get("sno")
        pwd = request.POST.get("pwd")

        return HttpResponse("登录成功")

    return render(request, 'Staff/login_a.html')

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
    staff_list = Staff.objects.all()   # 返回值为QuerySet类型
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