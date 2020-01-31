from django.shortcuts import render,HttpResponse
from web_app import models
# Create your views here.
import os
import json

def upload(request):

    if request.method=='GET':
        return render(request,'Test/up_File.html')
    if request.method=="POST":
        user=request.POST.get('user','')
        fafafa=request.POST.get('fafafa','')
        obj=request.FILES.get('fafafa','')
        print(user,obj,fafafa)
        file_path=os.path.join('static','img/Test/',obj.name)
        f=open(file_path,'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        response={
            'status':True,
            'path':file_path,
        }
        return HttpResponse(json.dumps(response))

admin_app={}
class model_admin(object):
    pass

def register(model_class,admin_class=None):
    if model_class._meta.app_label not in admin_app:
        admin_app[model_class._meta.app_label]={}
        admin_class=model_class
        admin_app[model_class._meta.app_label][model_class._meta.model_name]=admin_class

def reg(app_name):
    if app_name._meta.app_label not in admin_app:
        admin_app[app_name._meta.app_label]={}
    table_name=app_name
    admin_app[app_name._meta.app_label][app_name._meta.model_name]=table_name


reg(models.User)
reg(models.UserInfo)
reg(models.Topic)
reg(models.Kind)

def index(request):
    response={}
    # print(models.User.model)
    response['admin_app']=admin_app
    # for app_name,tables in admin_app.items():
    #     print(app_name)
    #     for table in tables.items():
    #         print(table)
    # print(models.User.Meta.verbose_name_plural)

    return render(request,'Test/table_index.html',response)

def display_table(request,app_name,table_name):
    # print(app_name,table_name)
    table=admin_app[app_name][table_name]
    # print(table._meta.verbose_name)
    # print(table.objects.all())
    response={}
    response['table']=table
    # response['table_objs']=table.objects.all()
    """
    @todo:分页
    """
    baseurl='/test/web_app/user/'


    page_list = []
    # user_list=[]
    user_obj = table.objects.all()

    # print(user_obj.all())
    # 通过前端得到当前页
    cur_page = request.GET.get('p','1')
    print(cur_page)
    cur_page = int(cur_page)
    if (cur_page) < 1:
        cur_page = 1

    # 定义每页显示的数据条数
    num_page = 10

    # 定义显示标签的个数<a>12345</a>
    a_count = 5

    # 通过models获得数据总数
    obj_count = table.objects.count()
    # 计算得出总页数

    total_page, more = divmod(obj_count, num_page)
    # 有余数，说明页数不够，再加一页
    if more:
        total_page += 1
    if int(cur_page) > total_page:
        cur_page = total_page
    # 确定开始索引
    start_page = (int(cur_page) - 1) * 10
    end_page = int(cur_page) * num_page
    response['table_objs'] = user_obj[start_page:end_page]
    # print(user_obj[start_page:end_page])

    page_list.append(
        '<a class="btn btn-primary" href="%s?p=%d">上一页</a>' % (baseurl,int(cur_page) - 1)
    )
    if cur_page <= a_count / 2 + 1:
        start_page = 1
        end_page = a_count + 1
    else:
        start_page = cur_page - 2
        end_page = cur_page + 2 + 1
    if cur_page > total_page - a_count / 2 + 1:
        start_page = total_page - a_count + 1
        end_page = total_page + 1
    for i in range(start_page, end_page):

        if i == cur_page:
            page_list.append(
                '<a class="btn btn-primary btn-danger" href="%s?p=%d">%d</a>' % (baseurl,i, i)
            )
        else:
            page_list.append(
                '<a class="btn btn-primary" href="%s?p=%d">%d</a>' % (baseurl,i, i)
            )
    # for i in range(1,num_page+1):
    #     if i==cur_page:
    #         page_list.append(
    #             '<a class="btn btn-primary btn-danger" href="/my_admin/?p=%d">%d</a>' % (i, i)
    #         )
    #     else:
    #         page_list.append(
    #             '<a class="btn btn-primary" href="/my_admin/?p=%d">%d</a>' % (i,i)
    #         )

    page_list.append(
        '<a class="btn btn-primary" href="%s?p=%d">下一页</a>' % (baseurl,int(cur_page) + 1)
    )
    response['page_list'] = page_list
    response['request'] = request
    return render(request,'Test/table_display.html',response)

def display_table_chage(request,app_name,table_name,id):
    print(app_name,table_name,id)
    from test_app import forms
    response={}

    response['User']=forms.User

    return render(request,'Test/display_table_chage.html',response)
    pass