import os
import time

from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django import forms
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from deploy.testonnx import out_detection

# def upload_list(request):
#     if request.method == "GET":
#         return render(request, 'upload_list.html')
#
#     # # 'username': ['big666']
#     # print(request.POST)  # 请求体中数据
#     # # {'avatar': [<InMemoryUploadedFile: 图片 1.png (image/png)>]}>
#     # print(request.FILES)  # 请求发过来的文件 {}
#     print(request.POST)
#     print(request.FILES)
#     file_object = request.FILES.get("avatar")
#     print(file_object.name)  # 文件名：WX20211117-222041@2x.png
#
#     f = open('media/input_detection/'+file_object.name, mode='wb')
#     for chunk in file_object.chunks():
#         f.write(chunk)
#     f.close()
#     out_detection('media/input_detection/'+file_object.name)
#     return HttpResponse("...")

class UpModelForm(BootStrapModelForm):
    # img不使用样式
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.obj_det
        fields = "__all__"

class ouput_UpModelForm(BootStrapModelForm):
    # img不使用样式
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.output_obj_det
        fields = "__all__"

def obj_list(request):
    queryset = models.output_obj_det.objects.all()
    return render(request, 'obj_list.html', {'queryset': queryset})

def obj_upload_modal_form(request):
    """ 上传文件和数据（modelForm）"""
    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'obj_upload_form.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        form.save()
        saved_data = form.cleaned_data['img'].name
        name = form.cleaned_data['name']
        output_name = out_detection('media/obj_dect/'+saved_data)
        ouput_form = ouput_UpModelForm({'name': name, 'img': output_name})
        print(output_name)
        if ouput_form.is_valid():
            ouput_form.save()
        return redirect("/obj/list/")
    return render(request, 'obj_upload_form.html', {"form": form, 'title': title})