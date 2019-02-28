from django.urls import path,re_path
from django.urls import reverse_lazy

from . import views
from django.conf import settings
from django.contrib.auth.views import LoginView ,LogoutView #导入类
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView


urlpatterns = [
    #path('login/', views.user_login, name='user_login'), #自定义的登录
    path('login/', LoginView.as_view(template_name='account/login.html'), name='user_login'),

    # 注销页面
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='user_logout'),

    #注册页面
    path('register/', views.register, name="user_register"),

    #修改成功后重新定向 url 页面
    path('password-change/',PasswordChangeView.as_view(template_name='registration/password_change_form.html',
                                                       success_url = reverse_lazy('account:password_change_done') ),name='password_change'),   #修改密码页面
    path('password-change-done/',PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    #通过邮箱 重置密码
    path('password-reset/',PasswordResetView.as_view(template_name='account/password_reset_form.html',
                                                      email_template_name='account/password_reset_email.html',
                                                      subject_template_name='account/password_reset_subject.txt',
                                                      success_url=reverse_lazy('account:password_reset_done') ),name='password_reset'),
    #发送邮箱成功的页面
    path('password-reset-email/',PasswordResetDoneView.as_view(template_name = 'account/password_reset_done.html'),name='password_reset_done'),

    #修改密码的页面
    re_path('password-reset-comfirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/',PasswordResetConfirmView.as_view(success_url=reverse_lazy('account:password_reset_complete'),
         template_name='account/password_reset_confirm.html'),name='password_reset_confirm' ),

    #修改密码成功页面
    path('password-reset-email/', PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),

    path('my-information/',views.myself,name="my_information"),

    path('edit-my-information/',views.myself_edit,name="edit_my_information"),

    path('my-image/',views.my_image,name="my_image"),



]
app_name = 'account'