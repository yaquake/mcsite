from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete


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
