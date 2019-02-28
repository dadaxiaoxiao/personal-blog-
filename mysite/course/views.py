from django.views.generic import TemplateView,ListView
from .models import Course
from braces.views import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,DeleteView
from django.shortcuts import redirect



from .forms import CreateCourseForm




# 基于类的视图
class AboutView(TemplateView):
    template_name = "course/about.html"    # 声明模板


class CourseListView(ListView):
    model = Course       # 查询所有记录
    context_object_name = "courses"       # 声明传入模板中的变量名称
    template_name = "course/course_list.html"


class UserMixin:
    def get_queryset(self):
        qs = super(UserMixin, self).get_queryset()
        return qs.filter(user=self.request.user)

class UserCourseMixin(UserMixin,LoginRequiredMixin):
    model = Course
    login_url = "/account/login/"



class ManageCourseListView(UserCourseMixin, ListView):
    context_object_name = "courses"
    template_name = 'course/manage/manage_course_list.html'


class CreateCourseView(UserCourseMixin, CreateView):
    fields = ['title', 'overview']                                # 声明显示字段
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kargs):
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect("course:manage_course")
        return self.render_to_response({"form":form})

class DeleteCourseView(UserCourseMixin, DeleteView):
    template_name = 'course/manage/delete_course_confirm.html'            # 确认删除的模板
    success_url = reverse_lazy("course:manage_course")                    # 删除完成后的界面 返回 manage-course
