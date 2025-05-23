from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from wagtail.models import Locale

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = "articles/articles.html"
    context_object_name = "articles"

    def get_queryset(self):
        current_locale = Locale.get_active()
        return (
            Article.objects.live()
            .filter(locale=current_locale)
            .order_by("-date_published")
        )


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article.html"
    context_object_name = "article"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        locale = Locale.get_active()
        return get_object_or_404(Article.objects.live(), slug=slug, locale=locale)
