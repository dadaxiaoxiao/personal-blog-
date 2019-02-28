from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import ArticleColumn,ArticlePost,Comment
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import redis
from django.conf import settings
from .forms import CommentForm
from django.db.models import Count

# 与redis 数据库的连接
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# 指定作者的文章列表
def article_titles(request,username=None):
    if username:                                                          # 用户名存在
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)         # 指定作者的文章
        try:
            userinfo = user.userinfo                # 通过User类实例获取 Userinfo 实例， 一对一关系
        except:
            userinfo = None                         # userinfo 为空，个人信息没有
    else:
        articles_title = ArticlePost.objects.all()                       # 全部文章

    # articles_title = ArticlePost.objects.all()
    paginator = Paginator(articles_title, 3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    if username:                                 # 用户名存在
        return render(request, "article/list/author_articles.html",
                      {"articles": articles, "page": current_page, "userinfo": userinfo, "user": user})
    return render(request, "article/list/article_titles.html", {"articles":articles, "page": current_page})


def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)   #指定当前的文章
    total_views = r.incr("article:{}:views".format(article.id))  # 对访问文章的次数进行记录

    r.zincrby('article_ranking', article.id, 1)

    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]     #阅读量前10
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))           # 排序

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
    else:
        comment_form = CommentForm()
    article_tags_ids = article.article_tag.values_list("id", flat=True)     # 返回 article 对象 article_tag 的 id 列表
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)        # 找出 article_tags_ids 里面对应的文章，排除当前文章
    similar_articles = similar_articles.annotate(same_tags = Count("article_tag")).order_by('-same_tags', '-created')[:4]

    return render(request, "article/list/article_detail.html",
                  {"article": article, "total_views": total_views, "most_viewed": most_viewed,
                   "comment_form": comment_form, "similar_articles": similar_articles})
@csrf_exempt
@require_POST
@login_required(login_url='/account/login/')
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)     # 登录状态才能评价
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")

