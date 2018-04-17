from .forms import PostForm,AvaForm,UsrForm,PhForm,SigForm,QqForm,MaForm
from django.shortcuts import render,get_object_or_404,render_to_response


def update_ava(request):    # 个人页面头像修改
    pro_form = AvaForm(request.POST, request.FILES, instance=request.user)
    # print(pro_form)
    if pro_form.is_valid():
        pro_form.save()
    return render(request, 'posts/profile.html')


def update_signature(request):
    signatur_form = SigForm(request.POST, instance=request.user)
    if signatur_form.is_valid():
        signatur_form.save()
    return render(request, 'posts/profile.html')


def update_name(request):
    name_form = UsrForm(request.POST, instance=request.user)
    if  name_form.is_valid():
        name_form.save()
        # return HttpResponse("{'status':'success'}", content_type='application/json')
    return render(request, 'posts/profile.html')

def update_qq(request):
    signatur_form = QqForm(request.POST, instance=request.user)
    if signatur_form.is_valid():
        signatur_form.save()
    return render(request, 'posts/profile.html')

def update_ph(request):
    signatur_form = PhForm(request.POST, instance=request.user)
    if signatur_form.is_valid():
        signatur_form.save()
    return render(request, 'posts/profile.html')

def update_maj(request):
    signatur_form = MaForm(request.POST, instance=request.user)
    if signatur_form.is_valid():
        signatur_form.save()
    return render(request, 'posts/profile.html')