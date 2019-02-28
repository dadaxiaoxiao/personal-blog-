from django.shortcuts import render
from django.http import  HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,RegistrationForm,UserProfileForm,UserForm,UserInfoForm
from django.contrib.auth.decorators import login_required   #登录修饰符
from .models import UserInfo,UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect



def user_login(request):
    if request.method == 'POST':
        """处理填写好的表单"""
        login_form = LoginForm(request.POST)

        """ 表单的数据是否有效 ，第一层"""
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            #authenticate() 检验用户是否为本网站项目的用户，验证密码

            if user:         #user 对象实例存在
                login(request,user)          #  """ 登录"""
                return HttpResponse("欢迎你，你已经验证成功！")
            else:
                return HttpResponse("Sorry,你的用户名或者密码不正确。")
        else:
            return HttpResponse("Invalid login (无效码)")

    if request.method == "GET":
        login_form = LoginForm()    #空绑定实例

        return render(request,"account/login.html", {'form': login_form})

def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form=UserProfileForm(request.POST)
        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit= False)  # commit= False 表单数据没有保存到数据库，返回生成一个数据库对象
            new_user.set_password(user_form.cleaned_data['password'])  #就是读取表单返回的值，返回类型为字典dict型
            new_user.save()
            new_profile=userprofile_form.save(commit=False)
            new_profile.user = new_user  #关联
            new_profile.save()   #存储
            UserInfo.objects.create(user=new_user)
            return  HttpResponse("successfully")
        else:
            return HttpResponse("Sorry ,your can not register.")
    else:
        user_form = RegistrationForm()
        userprofile_form=UserProfileForm()
        return render(request,"account/register.html",{"from": user_form,"profile": userprofile_form})



# 从UserInfo,UserProfile, User三个数据库表构成个性信息的视图函数

@login_required (login_url='/account/login')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request,"account/myself.html",{"user":user,"userinfo":userinfo,"userprofile":userprofile})


@login_required (login_url='/account/login')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)

    if request.method == "POST":
        # 返回表单
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data  # 返回表单的数据
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd['email'])
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            # 更新数据库
            user.save()
            userinfo.save()
            userprofile.save()
        return HttpResponseRedirect('/account/my-information/')  # 重定向页面
    else:
        user_form = UserForm(instance= request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth,"phone":userprofile.phone})
        userinfo_form = UserInfoForm( initial={"school":userinfo.school,"company": userinfo.company,
                                                   "profession":userinfo.profession,"address":userinfo.address,"aboutme":userinfo.aboutme})
        context = {"user_form":user_form,"userprofile_form": userprofile_form,"userinfo_form":userinfo_form}
        return render(request,"account/myself_edit.html",context)


@login_required (login_url='/account/login')
def my_image(request):
    #用于处理显示，上传，和剪裁头像，实现存储前端传递的图片
    if request.method == 'POST':
        img =request.POST['img']   #得到前端以POST 提交的图片信息
        userinfo = UserInfo.objects.get(user = request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html')





