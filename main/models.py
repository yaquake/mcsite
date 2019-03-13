from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField


# Class that contains info about Motto, Email, and Phone number on a main page.
class MottoEmailPhone(models.Model):
    motto = models.CharField(max_length=100, default='Your future starts with us')
    email = models.EmailField()
    phone = models.CharField(max_length=18, default='(09) 215 1267')
    facebook = models.URLField(default='http://facebook.com')
    linkedin = models.URLField(default='http://linkedin.com')

    def __str__(self):
        return 'Motto, email, and phone number'

    class Meta:
        verbose_name = 'Motto, email, and phone number'
        verbose_name_plural = 'Motto, email, and phone number'

    def save(self, *args, **kwargs):
        if MottoEmailPhone.objects.exists() and not self.pk:
            self.pk = 1
        return super(MottoEmailPhone, self).save(*args, **kwargs)


# Information on an About page
class About(models.Model):
    description = models.TextField(max_length=10000)

    def __str__(self):
        return 'About us'

    class Meta:
        verbose_name_plural = 'About us'
        verbose_name = 'About'

    def save(self, *args, **kwargs):
        if About.objects.exists() and not self.pk:
            self.pk = 1
        return super(About, self).save(*args, **kwargs)


# Info and a picture about company on a main page
class MainPageInfo(models.Model):
    image = models.ImageField(upload_to='media/main_page', null=False, default=False)
    description = models.TextField()

    def __str__(self):
        return 'Main page info'

    def save(self, *args, **kwargs):
        if MainPageInfo.objects.exists() and not self.pk:
            self.pk = 1
        return super(MainPageInfo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Main page info'
        verbose_name_plural = 'Main page info'

# TODO: figure out how to delete previous image before updating image field
# @receiver(pre_save, sender=MainPageInfo)
# def delete_main_info(sender, instance, **kwargs):
#     instance.image.delete(False)


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
        return '/news/' + self.slug

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'


class Person(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    about = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='media/personnel/', null=False, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


@receiver(pre_delete, sender=Person)
def delete_personnel_image(sender, instance, **kwargs):
    instance.image.delete(False)


class Property(models.Model):
    unit = models.CharField(max_length=7, default=None)
    street_number = models.CharField(max_length=5)
    street_name = models.CharField(max_length=40)
    suburb = models.CharField(max_length=50)
    city = models.CharField(max_length=20, default='Auckland')
    postcode = models.IntegerField(null=True)
    code = models.CharField(max_length=11)
    change_code = models.IntegerField(default=1)
    publish_entry = models.CharField(max_length=3, default=None)
    date_available = models.CharField(max_length=35)
    bathrooms = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    carparks = models.IntegerField(null=True, blank=True)
    property_class = models.CharField(max_length=15, blank=True)
    is_new_construction = models.CharField(max_length=3, blank=True, default=False)
    pets = models.CharField(max_length=3)
    smokers = models.CharField(max_length=3)
    agent_email1 = models.EmailField()
    agent_email2 = models.EmailField()
    agent_name = models.CharField(max_length=50)
    agent_mobile_num = models.CharField(max_length=15)
    agent_work_num = models.CharField(max_length=15)
    rental_period = models.CharField(max_length=6, default='Week')
    rent = models.IntegerField()
    advert_text = models.TextField(max_length=2000, blank=True)
    thumbnail = models.ImageField(upload_to='media/property_images', blank=True, null=True)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['-id']

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return '/properties/' + self.code


@receiver(pre_delete, sender=Property)
def delete_thumbnail(sender, instance, **kwargs):
    instance.thumbnail.delete()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/property_images', null=True, default=None)


@receiver(post_delete, sender=PropertyImage)
def delete_images(sender, instance, **kwargs):
    instance.image.delete(False)


# Login and password for getpalace.com API
class Palace(models.Model):
    name = models.CharField(max_length=50, blank=False)
    login = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=50, blank=False)

    def save(self, *args, **kwargs):
        if Palace.objects.exists() and not self.pk:
            self.pk = 1
        return super(Palace, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Palace credentials'
        verbose_name_plural = 'Palace credentials'

    def __str__(self):
        return self.name


# Services on a services page
class Services(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


# Contact info
class ContactUs(models.Model):
    description = models.TextField()

    def save(self, *args, **kwargs):
        if ContactUs.objects.exists() and not self.pk:
            self.pk = 1
        return super(ContactUs, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Contact us'
        verbose_name_plural = 'Contact us'

    def __str__(self):
        return 'Contact us'


# Email settings model for a contact form
class EmailSettings(models.Model):
    full_email = models.CharField(max_length=60, default=None)
    email_host = models.CharField(max_length=40)
    email_port = models.PositiveIntegerField()
    email_host_user = models.CharField(max_length=50)
    email_host_password = models.CharField(max_length=50)
    email_use_ssl = models.BooleanField(default=True)

    def __str__(self):
        return 'Email settings for a contact form'

    def save(self, *args, **kwargs):
        if EmailSettings.objects.exists() and not self.pk:
            self.pk = 1
        return super(EmailSettings, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Email settings'
        verbose_name = 'Email settings'


class WhyUs(models.Model):
    description = models.TextField(max_length=3000)

    def __str__(self):
        return 'Why McDonald Property?'

    def save(self, *args, **kwargs):
        if WhyUs.objects.exists() and not self.pk:
            self.pk = 1
        return super(WhyUs, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Why McDonald Property?'
        verbose_name = 'Why McDonald Property?'


class Guide(models.Model):
    description = models.TextField(max_length=3000)

    def __str__(self):
        return 'Tenancy guide'

    def save(self, *args, **kwargs):
        if Guide.objects.exists() and not self.pk:
            self.pk = 1
        return super(Guide, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Tenancy guide'
        verbose_name = 'Tenancy guide'


