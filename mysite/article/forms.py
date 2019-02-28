from django import forms
from .models import ArticleColumn,ArticlePost,Comment,ArticleTag


class AtricleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ("column",)


class ArticlePostForm(forms.ModelForm):
    class Meta:
        model= ArticlePost
        fields =("title","body")

# 评论
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("commentator", "body",)

# 文章标签
class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ("tag",)