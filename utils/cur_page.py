class is_myPage(object):
    def __init__(self,total_count,cur_page,base_url,per_page=10):
        """
        :param total_count: 总页数即从数据库中取的对象的总数
        :param cur_page: 当前页数
        :param base_url: 指向哪个url
        :param per_page: 要分的页数
        """
        self.total_count=total_count
        self.cur_page=cur_page
        self.base_url=base_url
        self.per_page=per_page
        pass
    def is_start_db(self):
        return (self.cur_page-1)*self.per_page #10
    def is_end_db(self):
        return (self.cur_page)*self.per_page #10
    def total_page(self):
        vnum, a = divmod(self.total_count, self.per_page)
        if a != 0:
            vnum += 1
        return vnum
    def page_str(self):
        """
            每页显示10条数据
            """
        v=self.total_page()
        # print(v)
        page_list = []
        if self.cur_page == 1:
            page_list.append('<a class="a-style" href="javascript:void(0);">上一页</a>')
        else:
            page_list.append('<a class="a-style" href="%s?p=%s">上一页</a>' % (self.base_url,self.cur_page - 1))

        # 6   1-12
        # 7   2-13
        if v <= 11:
            page_range_start = 1
            page_range_end = v
        else:
            if self.cur_page < 6:
                page_range_start = 1
                page_range_end = 11 + 1
            else:
                page_range_start = self.cur_page - 5
                page_range_end = self.cur_page + 6
                if page_range_end > v:
                    page_range_end = v + 1
                    page_range_start = v - 10
        # page_range_start=cur_page-5
        # page_range_end=cur_page+5+1
        for i in range(page_range_start, page_range_end):
            if i == self.cur_page:
                page_list.append('<a class="a-style active" href="%s?p=%s">%s</a>' % (self.base_url,i, i,))
            else:
                page_list.append('<a class="a-style" href="%s?p=%s">%s</a>' % (self.base_url,i, i,))
        if self.cur_page == v:
            page_list.append('<a class="a-style" href="javascript:void(0);">下一页</a>')
        else:
            page_list.append('<a class="a-style" href="%s?p=%s">下一页</a>' % (self.base_url,self.cur_page + 1))
        page = "".join(page_list)
        # start = (self.cur_page - 1) * 10
        # end = (self.cur_page) * 10
        return page
