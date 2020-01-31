from django.shortcuts import render,HttpResponse,redirect
#from django.contrib.auth import authenticate, login, logout
# Create your views here.
from io import BytesIO
from utils.check_code import create_validate_code
from web_app import models
import json





def home(request):
    response={}
    topic_recomend=models.Topic.objects.filter(recommend=1)#查询推荐帖子
    #print(topic_recomend)
    uid=request.session.get('uid','')
    if uid is not None:
        user=models.UserInfo.objects.filter(user_id=uid)
    else:
        user=None
    response['user']=user[0]
    response['topic_recommend']=topic_recomend
    return render(request,'web/home.html',response)

#发帖
def publish(request):
    if request.method == 'GET':
        kinds = models.Kind.objects.filter()
        response = {
            'kinds': kinds
        }
        return render(request, 'web/publish.html', response)
    elif request.method == 'POST':
        # session获取uid
        uid = request.session['uid']
        # 提交发布的文章
        t_title = request.POST.get('t_title')
        t_introduce = request.POST.get('t_introduce')
        t_content = request.POST.get('t_content')
        t_kind = request.POST.get('t_kind')
        print(t_title, t_introduce)

        obj = models.Topic.objects.create(t_title=t_title, t_introduce=t_introduce,
                                          t_content=t_content, t_kind=t_kind, t_uid=uid)
        t_id = obj.id

        # 存帖子图片
        t_photo = request.FILES.get('t_photo', None)
        t_photo_path = 'static/img/t_photo/' + str(t_id) + '_' + t_photo.name

        if t_photo:
            # 保存文件
            import os
            f = open(os.path.join(t_photo_path), 'wb')
            for line in t_photo.chunks():
                f.write(line)
            f.close()

        # 吧图片路径存入数据库
        models.Topic.objects.filter(id=t_id).update(t_photo='/' + t_photo_path)

        return redirect('/single/' + str(t_id))


# 单个帖子页面
def single(request, tid):
    if request.method == 'GET':
        # 帖子内容
        # 时间类别作者，标题，正文，图片path
        try:
            topic = models.Topic.objects.get(id=tid)
        except Exception as e:
            return redirect('/home')

        t_time = topic.create_time
        t_kind = topic.t_kind
        t_title = topic.t_title
        t_content = topic.t_content
        t_photo = topic.t_photo
        t_uid = topic.t_uid
        t_introduce = topic.t_introduce
        uid = request.session['uid']
        admin_uid = request.session.get('admin_uid')

        response = {
            'tid': tid,
            't_uid': t_uid,
            't_time': t_time,
            't_kind': t_kind,
            't_title': t_title,
            't_content': t_content,
            't_photo': t_photo,
            't_introduce': t_introduce,
            'uid': uid,
            'admin_uid': admin_uid,
        }

        # 留言内容
        # 留言者，留言时间，留言内容
        replys = models.Reply.objects.filter(r_tid=tid)
        reply_list = []
        for reply in replys:
            single_reply = {
                'r_uid': reply.r_uid,
                'r_time': reply.r_time,
                'r_content': reply.r_content,
                'r_id': reply.id,
                'r_photo': reply.r_photo,
            }
            reply_list.append(single_reply)
        response['reply_list'] = reply_list

        return render(request, 'web/single.html', response)

    elif request.method == 'POST':
        # 判断是否登录
        uid = request.session.get('uid')

        # 删除回复，管理员才可以删除
        p_type = request.POST.get('type')
        print(p_type)
        if p_type == 'delete':
            response = {'msg': '', 'status': False}
            r_id = request.POST.get('r_id')
            models.Reply.objects.filter(id=r_id).delete()
            response['status'] = True
            return HttpResponse(json.dumps(response))

        if not uid:
            return redirect('/login')
        # 进行回复
        r_content = request.POST.get('r_content')

        # 提交数据库
        obj = models.Reply.objects.create(r_tid=tid,r_uid=uid,r_content=r_content)

        r_id = str(obj.id)
        r_photo = request.FILES.get('r_photo')
        r_photo_path = ''
        if r_photo:
            # 保存文件
            r_photo_path = 'static/img/r_photo/' + r_id + '_' + r_photo.name
            import os
            f = open(os.path.join(r_photo_path), 'wb')
            for line in r_photo.chunks():
                f.write(line)
            f.close()

        # 吧图片路径存入数据库
        models.Reply.objects.filter(id=r_id).update(r_photo='/'+r_photo_path)
        return redirect('/single/' + tid)


def test(request):
    response={

    }
    uid=request.session['uid']
    userobj=models.UserInfo.objects.get(user_id=uid)
    response['userobj']=userobj
    print(userobj)

    return render(request,'base.html',response)


# 所有帖子
def all_top(request, kid, reply_limit, time_limit):
    """
        @todo:全部文章
        :param request:
        :return:
        """
    uid = request.session.get('uid')
    if request.method == 'GET':
        kinds = models.Kind.objects.filter()
        if kid == '0' and reply_limit == '0' and time_limit == '0':
            # 默认时间排序把帖子传过去
            topics = models.Topic.objects.filter()
        else:
            # request.path_info   # 获取当前url
            # from django.urls import reverse
            # reverse('all_tie', kwargs={'kid': '0', 'reply_limit': '0', 'time_limit': '0'})

            topics = models.Topic.objects.filter()

            # 筛选分类
            if kid != '0':
                topics = models.Topic.objects.filter(t_kind=kid)

            # 筛选回复数量
            tmp = []
            for topic in topics:
                # 查看每个帖子的回复数量
                count = len(models.Reply.objects.filter(r_tid=topic.id))
                # print(count)
                print(reply_limit)
                if reply_limit == '0':
                    pass
                elif reply_limit == '1':  # 1是大于100
                    print('到1了')
                    if count < 100:
                        print('到了')
                        continue
                elif reply_limit == '2':  # 2是30-100
                    if count < 30 or count > 100:
                        continue
                elif reply_limit == '3':  # 3是小于30
                    if count > 30:
                        continue
                tmp.append(topic)
            topics = tmp
            print(topics)

            # 筛选发布时间
            tmp = []
            for topic in topics:
                if time_limit == '0': # 0是全部时间
                    pass
                elif time_limit == '1':   # 1是1个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '2':   # 2是3个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '3':   # 3是6个月内
                    # 如果在限制之前，就筛掉
                    pass
                elif time_limit == '4':   # 4是1年内
                    # 如果在限制之前，就筛掉
                    pass
                tmp.append(topic)
            topics = tmp

        response = {
            'topics': topics,
            'kinds': kinds,
            'kid': kid,
            'time_limit': time_limit,
            'reply_limit': reply_limit,
            'uid': uid,
        }
        return render(request, 'web/all_top.html', response)

    elif request.method == 'POST':
        # 搜索接收一个字段，查询标题或者简介里有关键字的帖子
        keys = request.POST.get('keys')
        # 按关键字查询标题里含有关键字的
        topics = models.Topic.objects.filter(t_title__icontains=keys)

        kinds = models.Kind.objects.filter()
        return render(request, 'web/all_top.html', {'topics': topics, 'kinds': kinds, 'uid': uid})
"""
def all_top(request):
    
    response={}
    topic=models.Topic.objects.all()
    response['topic']=topic
    return render(request,'web/all_top.html',response)
"""


def my_art(request):
    """
    @todo:查看自己发布文章
    :param request:
    :return:
    """
    if request.method=="GET":
        response={}
        uid=request.session['uid']
        obj=models.Topic.objects.filter(t_uid=str(uid))
        #obj=models.Topic.objects.all()
        print(obj,request.session['uid'])
        response['t_user']=models.UserInfo.objects.get(user_id=uid)
        response['t_obj']=obj

        return render(request,'web/my_art.html',response)
    if request.method=='POST':
        if request.POST.get('type')=='logout':
            #print('OK')
            """删除登录信息"""
            del request.session['uid']

def pwd_edit(request):
    """
    @todo:修改密码
    :param request:
    :return:
    """

    return render(request,'web/pwd_edit.html')

def user_info(request):
    """
    @todo：用户信息
    :param request:
    :return:
    """
    response = {"status":False,"mag":''}
    if request.method=="GET":
        userobj = models.UserInfo.objects.get(user_id=request.session['uid'])
        response['userobj'] = userobj
        return render(request, 'web/user_info.html', response)
    if request.method=="POST":
        if request.POST.get('type')=='logout':
            #print('OK')
            """删除登录信息"""
            del request.session['uid']
        response['status']=True
        response['msg']='提交成功'
        #身份证和姓名不能改
        user_id=request.POST.get('user_id')
        name=request.POST.get('name')

        email=request.POST.get('email')
        nickname =request.POST.get('nickname')
        sex=request.POST.get('sex')
        age=request.POST.get('age')
        phone=request.POST.get('phone')
        country=request.POST.get('country')
        province=request.POST.get('province')
        city=request.POST.get('city')
        location=request.POST.get('location')
        #avatar=request.FILES.get('avatar')
        #print(user_id,name)
        print(user_id,name,email,nickname,sex,age,phone,country,province,country,city,location)
        #进行数据更新
        if email != None:
            models.UserInfo.objects.filter(user_id=user_id).update(email=email)
            """
            同上一个作用
            obj=models.UserInfo.objects.filter(user_id=user_id)
            obj.email=email
            obj.save()
            """
        if nickname != None:
            models.UserInfo.objects.filter(user_id=user_id).update(nickname=nickname)
        if sex != None:
            models.UserInfo.objects.filter(user_id=user_id).update(sex=sex)
        if age != None:
            models.UserInfo.objects.filter(user_id=user_id).update(age=age)
        if phone != None:
            models.UserInfo.objects.filter(user_id=user_id).update(phone=phone)
        if country != None:
            models.UserInfo.objects.filter(user_id=user_id).update(country=country)
        if province != None:
            models.UserInfo.objects.filter(user_id=user_id).update(province=province)
        if city != None:
            models.UserInfo.objects.filter(user_id=user_id).update(city=city)
        if location != None:
            models.UserInfo.objects.filter(user_id=user_id).update(location=location)
        return HttpResponse(json.dumps(response))


def index(request):
    """
    @todo:主页
    :param request:
    :return:
    """
    if request.method=="POST":
        if request.POST.get('type')=='logout':
            #print('OK')
            """删除登录信息"""
            del request.session['uid']
    if request.method == 'GET':
        response = {}

        # top 10（公告）的处理，筛选10个也要改
        announcements = models.Announcement.objects.filter()
        # 把这10个公告封装成字典
        a_list = []
        for a in announcements:
            dic = {'a_id': a.id, 'a_title': a.a_title}
            a_list.append(dic)
        # 把列表装进回复字典里
        n = 10 if len(a_list) < 10 else len(a_list)

        response['a_list'] = a_list[::-1][0:n - 1]

        # 帖子推荐列表，推荐8个帖子，推荐8个要改
        recommends = models.Topic.objects.filter(recommend=True)
        # 推荐列表
        r_list = []

        for t in recommends:
            dic = {'t_id': t.id, 't_title': t.t_title, 't_introduce': t.t_introduce, 't_photo': t.t_photo}
            r_list.append(dic)
        # 把列表装进response
        response['r_list'] = r_list

        # 把uid装进返回字典里
        response['uid'] = request.session['uid']
        userobj=models.UserInfo.objects.get(user_id=request.session['uid'])
        response['userobj']=userobj
        # 把所有类别装入返回字典里
        kinds = models.Kind.objects.filter()
        response['kinds'] = kinds

        return render(request, 'web/index.html', response)

def check_code(request):
    """
    @todo:验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream,'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

def login(request):
    """
    @todo:登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'web/login.html')
    elif request.method == 'POST':
        # 验证用户名密码是否正确，然后登陆存入session
        type = request.POST.get('type')
        response = {'msg': '', 'status': False}

        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        if type == 'login':
            if len(models.User.objects.filter(uid=uid, password=pwd)) != 0:
                # 登录成功
                response['status'] = True
                request.session['uid'] = uid
                return HttpResponse(json.dumps(response))
                pass
            else:
                # 登录失败
                response['msg'] = '用户名或者密码错误'
                return HttpResponse(json.dumps(response))
                pass
        elif type == 'register':
            models.User.objects.create(uid=uid, password=pwd)
            response['status'] = True
            request.session['uid'] = uid
            return HttpResponse(json.dumps(response))
    '''
    response={'msg':'','status':False}
    if  request.method == 'POST':
        code = request.POST.get('check_code')
        username=request.POST.get('uid')
        password=request.POST.get('pwd')
        print(username,password,code)
        
        
        if username==models.User.objects.filter(uid=username)[0].uid and password==models.User.objects.get(uid=username).password and code.upper() == request.session['CheckCode'].upper():
        
            #登录成功
            
            print(password)
            response['status']=True
            request.session['uid']=username
            return HttpResponse(json.dump(response))
        else:
            response['msg']='用户名或密码错误'
            return HttpResponse(json.dump(response))'''

    return render(request, 'web/login.html')