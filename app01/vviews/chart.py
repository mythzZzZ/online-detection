from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """ 数据统计页面 """
    return render(request, 'chart_list.html')


def chart_bar(request):
    """ 构造柱状图的数据 """
    # 数据可以去数据库中获取
    legend = ["梁吉宁", "武沛齐"]
    series_list = [
        {
            "name": '梁吉宁',
            "type": 'bar',
            "data": [15, 20, 36, 10, 10, 10]
        },
        {
            "name": '武沛齐',
            "type": 'bar',
            "data": [45, 10, 66, 40, 20, 50]
        }
    ]
    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼图的数据 """

    db_data_list = [
        {"value": 2048, "name": 'IT部门'},
        {"value": 1735, "name": '运营'},
        {"value": 580, "name": '新媒体'},
    ]

    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    legend = ["上海", "广西"]
    series_list = [
        {
            "name": '上海',
            "type": 'line',
            "stack": 'Total',
            "data": [15, 20, 36, 10, 10, 10]
        },
        {
            "name": '广西',
            "type": 'line',
            "stack": 'Total',
            "data": [45, 10, 66, 40, 20, 50]
        }
    ]
    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def highcharts(request):
    pass
    # """ highcharts示例 """
    #
    # return render(request,'highcharts.html')
