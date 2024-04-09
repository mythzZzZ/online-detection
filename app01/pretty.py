from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from app01.utils.pagination import Pagination

def pretty_list(request):
    """ 用户管理 """

    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile="18383333333",price=10,
    #                                     level=1,status=1)


    data_dict = {}
    search_data = request.GET.get('q',"")
    if search_data:
        data_dict['mobile__contains'] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request,queryset)
    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request,"my_pretty_list.html",context)


    # 获取数据  level字段倒序
    queryset = models.PrettyNum.objects.all().order_by("-level")

    # 获取数据库的信息传给前端 让前端遍历出来
    return render(request, 'my_pretty_list.html', {"queryset": queryset})


class UserModelForm(forms.ModelForm):
    # 校验数据的格式
    mobile = forms.CharField(
        label="手机号",
        # 使用正则表达式验证数据格式
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    # create_time = forms.CharField(label="yyyy-yy-yy")
    class Meta:
        model = models.PrettyNum
        # 列表里面的名字对应数据库的列名
        # 给每个列名弄一个输入框给前端
        # gender 是choices 所以给前端的选择框
        # "depart" 是外键 所以给前端的选择框
        fields = ["mobile", "price", "level", 'status']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 给输入框添加样式
        for name,field in self.fields.items():
            field.widget.attrs = {
                "class": "form-control", "placeholder": field.label
            }

    # 验证：方式2 定义clean_字段（数据库字段） 方法 对数据进行校验
    def clean_mobile(self):
        # 获取用户输入的moble
        txt_mobile = self.cleaned_data["mobile"]
        # 通过输入的数据查询 数据是否存在
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


def pretty_add(request):
    # 添加用户form版本
    if request.method == "GET":
        form = UserModelForm()
        # 返回form的输入框
        return render(request,'my_pretty_add.html',{"form": form})
    # 用户POST提交过来的数据，使用form进行数据校验。
    form = UserModelForm(data=request.POST)

    # 开始校验数据
    # 验证信息格式对不对
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect('/pretty/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'my_pretty_add.html', {"form": form})


class PrettyEditModelForm(forms.ModelForm):

    # create_time = forms.CharField(label="yyyy-yy-yy")
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )
    class Meta:
        model = models.PrettyNum

        fields = ["mobile","price", "level", 'status']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 给输入框添加样式
        for name,field in self.fields.items():
            field.widget.attrs = {
                "class": "form-control", "placeholder": field.label}
    # 编辑的验证条件
    # 验证：方式2
    def clean_mobile(self):
        # 获取编辑时，当前编辑对象数据库存的id self.instance.pk 获取当前行的id
        # print(self.instance.pk)

        # 获取当前编辑对象数据库存的mobile号
        txt_mobile = self.cleaned_data["mobile"]
        # 判断除了当前id 这个手机号是否存在
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            # 如果存在 不给编辑
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile
def pretty_edit(request,nid):
    """ 编辑用户 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        # 在输入框里面显示数据库原本的数据
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'my_pretty_edit.html', {'form': form})
    # 把网页传过来要更新的数据 填入数据库
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'my_pretty_edit.html', {"form": form})

def user_delete(request,nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
