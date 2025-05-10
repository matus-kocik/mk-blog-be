from django import forms
from django.db import models
from django.utils.text import slugify
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock, StructBlock, URLBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from users.models import CustomUser


@register_snippet
class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Name of the category",
        verbose_name="Category Name",
    )
    description = models.TextField(
        blank=True,
        help_text="Description of the category",
        verbose_name="Category Description",
    )
    slug = models.SlugField(unique=True, blank=True, editable=False)

    panels = [
        FieldPanel("name"),
        FieldPanel("description"),
    ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


class Article(Page):
    author = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles",
        help_text="Author of the article",
        verbose_name="Author",
    )
    date_published = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the article was published",
        verbose_name="Date Published",
    )
    thumbnail = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Thumbnail image for the article",
        verbose_name="Thumbnail",
    )

    summary = models.CharField(
        max_length=250, blank=True, help_text="Short introduction to the article"
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Is the article published?",
        verbose_name="Published",
    )
    categories = models.ManyToManyField(
        Category,
        related_name="articles",
        blank=True,
        help_text="Categories for the article",
        verbose_name="Categories",
    )

    content = StreamField(
        [
            ("text", RichTextBlock()),
            ("image", ImageChooserBlock()),
            (
                "quote",
                StructBlock(
                    [
                        ("quote", RichTextBlock()),
                        ("author", RichTextBlock()),
                    ]
                ),
            ),
            ("link", URLBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("thumbnail"),
        FieldPanel("summary"),
        FieldPanel("is_published"),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-date_published"]
