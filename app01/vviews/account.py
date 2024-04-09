from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO

from app01.utils.code import check_code
from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5

class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        # 获取传入password字段的值
        pwd = self.cleaned_data.get("password")
        # password的值变成md5格式返回
        # 'password': '5e5c3bad7eb35cba3638e145c830c35f'
        return md5(pwd)

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request,'login.html',{'form':form})

    form = LoginForm(data=request.POST)

    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code',"")
        if code.upper() != user_input_code.upper():
            form.add_error("code","验证码错误")
            return render(request,'login.html',{'form':form})


        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()

        if not admin_object:
            form.add_error("password","用户名或密码错误")
            return render(request,'login.html',{'form':form})
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/admin/list/")


    return render(request,'login.html',{'form':form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)
    # 字节流
    stream = BytesIO()
    # 把文件写在字节流里面，存放在内存中
    img.save(stream, 'png')
    # 返回图片到绑定的url
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')

