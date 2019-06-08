from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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
    description = models.TextField(max_length=100000)

    def __str__(self):
        return 'Tenancy guide'

    def save(self, *args, **kwargs):
        if Guide.objects.exists() and not self.pk:
            self.pk = 1
        return super(Guide, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Tenancy guide'
        verbose_name = 'Tenancy guide'
