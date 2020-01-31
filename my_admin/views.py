from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from web_app import models
# from my_admin.util import paginator
from utils import pagination

def my_admin(request):
    """
        @todo
        :param total_page: 总页数
        :param cur_page: 当前页数
        :param per_page:显示的数量
        :return:
        """

    page_list=[]
    response={}
    #user_list=[]
    user_obj=models.User.objects.all()

    # print(user_obj.all())
    # 通过前端得到当前页
    cur_page=request.GET.get('p')
    cur_page=int(cur_page)
    if (cur_page)<1:
        cur_page=1

    #定义每页显示的数据条数
    num_page=10

    #定义显示标签的个数<a>12345</a>
    a_count=5

    #通过models获得数据总数
    obj_count = models.User.objects.count()
    #计算得出总页数

    total_page,more=divmod(obj_count,num_page)
    #有余数，说明页数不够，再加一页
    if more:
        total_page+=1
    if int(cur_page) >total_page:
        cur_page=total_page
    # 确定开始索引
    start_page=(int(cur_page)-1)*10
    end_page=int(cur_page)*num_page
    response['users']=user_obj[start_page:end_page]
    # print(user_obj[start_page:end_page])

    page_list.append(
        '<a class="btn btn-primary" href="/my_admin/?p=%d">上一页</a>'%(int(cur_page)-1)
    )
    if cur_page<=a_count/2+1:
        start_page=1
        end_page=a_count+1
    else:
        start_page=cur_page-2
        end_page=cur_page+2+1
    if cur_page>total_page-a_count/2+1:
        start_page=total_page-a_count+1
        end_page=total_page+1
    for i in range(start_page,end_page):

            if i == cur_page:
                page_list.append(
                    '<a class="btn btn-primary btn-danger" href="/my_admin/?p=%d">%d</a>' % (i, i)
                )
            else:
                page_list.append(
                    '<a class="btn btn-primary" href="/my_admin/?p=%d">%d</a>' % (i, i)
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
        '<a class="btn btn-primary" href="/my_admin/?p=%d">下一页</a>'%(int(cur_page)+1)
    )
    response['page_list']=page_list
    # for i in range(1,100):
    #     models.User.objects.create(uid='0859033%s'%(i),password=123456)

    # print(obj)

    # response['is_test']="<a>大家库萨克的黑科技撒</a>"
    return render(request,'my_admin/index.html',response)