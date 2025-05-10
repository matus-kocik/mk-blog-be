from django.views.generic import DetailView, ListView

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "articles/articles.html"
    context_object_name = "articles"
    queryset = Article.objects.all().order_by("-date_published")


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article.html"
    context_object_name = "article"
