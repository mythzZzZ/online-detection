from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination

# Create your views here.

def depart_list(request):
    """ 部门列表 """

    # 去数据库中获取所有的部门列表
    #  [对象,对象,对象]
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    if request.method == "GET":
        return render(request,'depart_add.html')
    # 获取用户POST提交过来的数据（title输入为空）
    title = request.POST.get("title")
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向回部门列表
    return redirect("/depart/list/")

def depart_delete(request):
    # 获取get请求传来的参数
    nid = request.GET.get('nid')
    # 通过传进来的id 从数据库删除数据
    models.Department.objects.filter(id = nid).delete()

    # 重定向回部门列表
    return redirect("/depart/list/")

def depart_edit(request,nid):

    # 修改部门

    if request.method == "GET":
        row_object = models.Department.objects.filter(id = nid).first()
        return render(request,'depart_edit.html',{"row_object":row_object})

    title = request.POST.get("title")
    # 获取用户提交的新的标题,原标题改为新的标题

    models.Department.objects.filter(id = nid).update(title=title)
    return redirect("/depart/list/")

def user_list(request):
    """ 用户管理 """

    # 获取所有用户列表 [obj,obj,obj]
    queryset = models.UserInfo.objects.all()
    page_object = Pagination(request,queryset)
    context = {

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    """
    # 用Python的语法获取数据
    for obj in queryset:
        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(), obj.depart_id, obj.depart.title)
        # print(obj.name, obj.depart_id)
        # obj.depart_id  # 获取数据库中存储的那个字段值
        # obj.depart.title  # 根据id自动去关联的表中获取哪一行数据depart对象。
    """
    # 获取数据库的信息传给前端 让前端遍历出来
    return render(request, 'user_list.html', context)

def user_add(request):
    # 添加用户 原始方式
    if request.method == "GET":
        context = {
            'gender_choices':models.UserInfo.gender_choices,
            'depart_list':models.Department.objects.all()
        }
        return render(request,"user_add.html",context)

    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 把网页传来的数据传到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=account, create_time=ctime,
                                   gender=gender, depart_id=depart_id)

    # 返回到用户列表页面
    return redirect("/user/list/")

# forms的使用

from django import forms

class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3,label="用户名",
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    # create_time = forms.CharField(label="yyyy-yy-yy")
    class Meta:
        model = models.UserInfo
        # 列表里面的名字对应数据库的列名
        # 给每个列名弄一个输入框给前端
        # gender 是choices 所以给前端的选择框
        # "depart" 是外键 所以给前端的选择框
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 给输入框添加样式
        for name, field in self.fields.items():
            # 字段中有属性，保留原来的属性，没有属性，才增加。
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }



def user_model_form_add(request):
    # 添加用户form版本
    if request.method == "GET":
        form = UserModelForm()
        # 返回form的输入框
        return render(request,'user_model_form_add.html',{"form": form})
    # 用户POST提交过来的数据，使用form进行数据校验。
    form = UserModelForm(data=request.POST)

    # 开始校验数据
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request,nid):
    """ 编辑用户 """
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        # 在输入框里面显示数据库原本的数据
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})
    # 把网页传过来要更新的数据 填入数据库
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {"form": form})

def user_delete(request,nid):
    models.UserInfo.objects.filter(id = nid).delete()
    return redirect('/user/list/')





