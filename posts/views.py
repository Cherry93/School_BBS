from django.shortcuts import render,get_object_or_404,render_to_response,HttpResponse
from posts.models import Post,Category,Like,Favorite,Tag,Transmit
from .forms import PostForm,AvaForm,UsrForm,PhForm,SigForm,QqForm,MaForm
from users.models import User
from comments.models import Comment
from comments.forms import CommentForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
import json
from comments.models import CommentReply
from hotinfo.models import HotInfo
from comments.views import new_comment

### 日期测试 文章按以下时间排序
today = datetime.date.today()
# print(today)
year = today.year
month = today.month
day = today.day
week = today.weekday()     #Day of week Monday = 0, Sunday = 6
# 本周是从周一开始 周天 按周查询逻辑: 如果今天是0 那么就是今天的日期.如果是6 那么就是今天日期,推6天

sartdata = datetime.date(year,month,day-week-2)
enddata = datetime.date(year,month,day+week)
# sartdata = datetime.date(2018,4,11)
# enddata = datetime.date(2018,4,16)
def index (request):
    # if request.method=='GET':
    #     return HttpResponse('welcome')
    return  render(request,'posts/index2.html',{})



class IndexView(ListView):          # 分页器写法
    global year,month,day,week,sartdata,enddata
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 9


    # 重写get_context_data,一遍放入我们的分页的起始页面和结束页码
    def get_context_data(self, **kwargs):
        print('--------------11111111111')
        print(kwargs)
        print('2222222222222222222')
        # 调用父类的get_context_data方法
        context = super().get_context_data(**kwargs)
        hot_list = Post.objects.all().order_by('-views')[0:8]   # 热点信息
        hotinfo = HotInfo.objects.all()[0:10]
        timeweek = Post.objects.filter(created_time__range=(sartdata,enddata)).order_by('-views')
        timemonth = Post.objects.filter(created_time__month= month).order_by('-views')[0:8]
        timeday = Post.objects.filter(created_time__day= day).order_by('-views')



        # 最新评论逻辑：当前登录的作者，找到他所发布的所有帖子，再遍历每篇帖子，
        # 找到帖子下所有的评论，再截取最前面的评论，放到一个列表，再遍历列表，显示最前面的
        ########## 最新评论 #########
        #context.get()
        print(context)
        context.update({'hot_list': hot_list,'hotinfo':hotinfo,'timeweek':timeweek,'timemonth':timemonth,'timeday':timeday})
        return context


    '''
    
    def get (self,request,*args,**kwargs):
        print('-------------------------------22222222222')
        print(kwargs)
        userid = request.user

        newcomment_list = []
        post_list = Post.objects.filter(author_id=userid)
        for post in post_list:
            comm_list = post.comment_set.all()
            num = len(comm_list)
            print('-----------------------------------------------------num', num)
            if num == 0:
                pass
            else:
                newcomment_list.append(post)
        print('------------------------------------newcomment_list', newcomment_list)
        hot_list = Post.objects.all().order_by('-views')[0:8]  # 热点信息
        post_list = Post.objects.all()
        # context = ({'newcomment_list':newcomment_list})
        paginate_by = self.paginate_by
        context = super()
        return render(request,self.template_name,locals())
    '''





def posts(request):         # 原始写法
    post_list = Post.objects.all().order_by('-created_time')
    hot_list = Post.objects.all().order_by("-views")

    return render(request,'posts/index.html',locals())


def detail(request, pk):

    post = get_object_or_404(Post, pk=pk)
    reply_list = CommentReply.objects.all()
    hot_list = Post.objects.all().order_by('-views')[0:8]  # 热点信息
    ####评论的用户#####

    # 阅读量 +1
    post.increase_views()
    # 生成评论form表单
    form = CommentForm()
    # 把post的评论列表传到前台
    comment_list = post.comment_set.all().order_by('-created_time')
    avt = []
    # 根据评论和post_id 查找评论的user_id 再获取user的信息
    if len(comment_list) > 0:
        for commen in comment_list:
            com_id = commen.id
            q = {'id': com_id, 'post_id': pk}
            com_list = Comment.objects.filter(**q)   # 找到用户对象集

            if len(com_list) > 0:
                for com in com_list:
                    userid = com.user_id        # 找到用户id
                    print(userid)
                    userobj = User.objects.get(id =userid)  # 用户对象单个
                    print(userobj)
                    print(userobj.avatar)
                    avt.append(userobj)
    print(avt,type(avt))

    # post.content = markdown.markdown(post.content,
    #                     extensions=[
    #                         'markdown.extensions.extra',
    #                         'markdown.extensions.codehilite',
    #                         'markdown.extensions.toc'
    #                     ])
    # post.increase_views()
    return render(request, 'posts/detail3.html', locals())

def categories(request, pk):
    # 根据pk取得category对象db
    category = get_object_or_404(Category, pk=pk)
    # 根据取得category来正向查找post
    # post_list = Post.objects.filter(category=category)
    # 反向查
    post_list = category.post_set.all()
    return render(request, 'posts/index.html', locals())


def tags(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    # 反向查
    post_list = tag.post_set.all()
    return render(request, 'posts/index.html', {'post_list': post_list})

@login_required
def add_post(request):        # 发帖

    post_list = Post.objects.all().order_by('-created_time')
    hot_list = Post.objects.all().order_by("-views")[0:8]
    form = PostForm(instance=request.user)
    # 判断request的请求方法，如果是post方法，那么就处理数据
    if request.method == 'POST':
        # 获取前台传过来的数据，用来生成form对象
        form = PostForm(request.POST)

        # 判断form表单数据是否合法
        if form.is_valid():
            post = form.save(commit=False)
            # 如果合法，则保存数据
            post.author=request.user
            form.save()
            # print(form.cleaned_data)
            post_list = Post.objects.all().order_by('-created_time')
            return render(request,'posts/index.html', {'post_list': post_list})
            # return HttpResponse("{'status':'success'}", content_type='application/json')
            # messages.success(request, '保存成功！')
            # return HttpResponseRedirect('/index')
    return render(request, 'posts/add.html', locals())
    # 如果是get方法，就返回用户信息修改页面

@login_required
def profile(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    post_list = user.post_set.all()
    return render(request, 'posts/profile.html',locals())


def like(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    fav_list = user.like_set.all()
    return render(request, 'posts/profile.html',locals())


def favorite(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    fav_list = user.favorite_set.all()

    return render(request, 'posts/profile.html',locals())


def transmite(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    fav_list = user.transmit_set.all()

    return render(request, 'posts/profile.html',locals())

def comment(request,pk):    # 个人页面
    user = User.objects.get(pk=pk)
    fav_list = user.comment_set.all()
    return render(request, 'posts/profile.html',locals())

@login_required
def add_favorite(request):
    print('hello')
    if request.is_ajax():
        user = request.user
        contentid = request.POST.getlist('contend_id')

        # contentid = request.POST.get('contend_id')
        print(contentid[0])
        post = Post.objects.get(id=contentid[0])
        print(post)
        created_time = datetime.datetime.now()
        post_id = Favorite.objects.filter(post_id=post)
        print(post_id)
        if post_id.exists():
            resp = {'status': '已经收藏'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        else:
            post.favo_num +=1
            post.save()
            Favorite.objects.update_or_create(user=user, post=post, created_time=created_time)
            resp = {'errorcode': 100, 'status': '收藏成功'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def add_like(request):
    if request.is_ajax():
        user = request.user
        contentid = request.POST.getlist('contend_id')

        # contentid = request.POST.get('contend_id')
        post = Post.objects.get(id=contentid[0])
        created_time = datetime.datetime.now()
        post_id = Like.objects.filter(post_id=post)
        if post_id.exists():
            resp = {'status': '已经点赞'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            post.like_num +=1
            post.save()
            Like.objects.update_or_create(user=user, post=post, created_time=created_time)
            resp = {'errorcode': 100, 'status': '成功点赞'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def add_transmit(request):      # 转发
    path = request.path
    user = request.user
    post = Post.objects.all()

    if request.is_ajax():
        user = request.user
        contentid = request.POST.getlist('contend_id')

        # contentid = request.POST.get('contend_id')
        post = Post.objects.get(id=contentid[0])

        post.save()

        created_time = datetime.datetime.now()
        post_id = Transmit.objects.filter(post_id=post)
        if post_id.exists():
            resp = {'status': '已转发'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            post.transmit_num += 1
            post.save()
            post.id = None  # 只需要改变新对象的主键值，然后运行save() 复制数据库
            post.post_from += 1
            post.views = 0
            post.save()
            Transmit.objects.update_or_create(user=user, post=post, created_time=created_time)
            resp = {'errorcode': 100, 'status': '成功转发'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'posts/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(content_html__icontains=q))
    return render(request, 'posts/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})