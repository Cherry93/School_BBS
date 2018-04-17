from django.shortcuts import render, get_object_or_404, redirect,HttpResponse,render_to_response
from posts.models import Post
from users.models import User
from .models import Comment,CommentReply
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
import datetime
import json
@login_required
def post_comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 Django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=post_pk)

    # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求，
    # 因此只有当用户的请求为 post 时才需要处理表单数据。
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        form = CommentForm(request.POST)

        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            print(comment)

            # 将评论和被评论的文章关联起来。
            comment.post=post
            # 将评论和作者关联起来。
            comment.user=request.user
            post.comment_num += 1

            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()

            post.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            comment_list = post.comment_set.all()

            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list,

                       }
            return render(request, 'posts/detail3.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)


def reply(request,com_pk):      # 评论回复逻辑：ajax请求评论的作者和内容，完了存入数据库，再渲染页面
    if request.is_ajax():
        content = request.POST.getlist('content')
        replay_user = request.POST.getlist('user')
        re_id = User.objects.filter(username = replay_user)
        replay_time = datetime.datetime.today()
        author = request.user
        author1 = author.id
        comment = Comment.objects.get(id=com_pk)
        # print(content, replay_user, replay_time, author,comment,author1)
        if content:
            CommentReply.objects.create(content=content,comment_id=com_pk,author_id=author1,replay_user_id=author1,replay_time=replay_time)
            return HttpResponse(json.dumps({'content':content}))
    else:
        reply_list = CommentReply.objects.all()
        return render_to_response('posts/detail3.html',{ 'reply_list':reply_list},content_type="application/json")


def new_comment(request):           # 最新评论逻辑：当前登录的作者，找到他所发布的所有帖子，再遍历每篇帖子，
    newcomment_list =[]              # 找到帖子下所有的评论，再截取最前面的评论，放到一个列表，再遍历列表，显示最前面的
    userid = request.user
    userid = 3
    post_list = Post.objects.filter(author = userid)
    for post in post_list:
        comm_list = post.comment_set.all()
        num = len(comm_list)
        print('-----------------------------------------------------num',num)
        if num ==0:
            pass
        else:
            newcomment_list.append(post[:-1])
    print('------------------------------------newcomment_list',newcomment_list)

    return render(request,'posts/index.html',newcomment_list)