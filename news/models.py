from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class News(models.Model):
    name = models.CharField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add=True, null=False)
    image = models.ImageField(upload_to='media/news/', null=True, default=None)
    description = models.TextField()
    slug = models.SlugField(unique=True, default=False)

    # TODO: change logic
    def save(self, *args, **kwargs):
        length = 50
        if News.objects.filter(slug=slugify(self.name[:length])).exists():
            self.slug = slugify(self.name[:length-3])
        else:
            self.slug = slugify(self.name[:length-1])

        super(News, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def pubdate_pretty(self):
        return self.pub_date.strftime('%A, %d %B  %Y')

    def get_absolute_url(self):
        return reverse('news', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
