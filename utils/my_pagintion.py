def Page(baseurl,table,cur_page):
    page_list = []
    # user_list=[]
    user_obj = table.objects.all()

    # print(user_obj.all())
    # 通过前端得到当前页
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
    # print(user_obj[start_page:end_page])

    page_list.append(
        '<a class="btn btn-primary" href="%s?p=%d">上一页</a>' % (baseurl, int(cur_page) - 1)
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
                '<a class="btn btn-primary btn-danger" href="%s?p=%d">%d</a>' % (baseurl, i, i)
            )
        else:
            page_list.append(
                '<a class="btn btn-primary" href="%s?p=%d">%d</a>' % (baseurl, i, i)
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
        '<a class="btn btn-primary" href="%s?p=%d">下一页</a>' % (baseurl, int(cur_page) + 1)
    )
    return page_list