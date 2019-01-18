from __future__ import absolute_import, unicode_literals
import bs4 as bs
import requests
import base64
import os
from celery import shared_task, task, Celery
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from easy_thumbnails.files import get_thumbnailer


@shared_task()
def update_from_xml():
    from main.models import Property, PropertyImage

    username = 'advert@mcdonaldpm.co.nz'
    password = 'MCW@dvert$Pr0p291118'

    try:
        if requests.get('https://serviceapi.realbaselive.com/Service.svc/RestService/AvailableProperties',
                                     auth=(username, password)):

            Property.objects.all().delete()
            property_list_xml = requests.get(
                'https://serviceapi.realbaselive.com/Service.svc/RestService/AvailableProperties',
                auth=(username, password))
            soup = bs.BeautifulSoup(property_list_xml.text, 'xml')

            for property in soup.find_all('AvailableProperty'):
                if property.PropertyStatus.text == 'Active':
                    prop = Property()
                    prop.street_number = property.PropertyAddress1.text
                    prop.street_name = property.PropertyAddress2.text

                    if ' Auckland' in property.PropertyAddress3.text:
                        s = property.PropertyAddress3.text.replace(' Auckland', '')
                        prop.suburb = s
                    else:
                        prop.suburb = property.PropertyAddress3.text

                    if property.PropertyAddress4.text == '':
                        prop.city = 'Auckland'
                    if property.PropertyFeatures.PropertyPostCode.text != '':
                        prop.postcode = property.PropertyFeatures.PropertyPostCode.text
                    prop.code = property.PropertyCode.text
                    prop.date_available = property.PropertyDateAvailable.text[:10]

                    if property.PropertyFeatures.PropertyBathroomsNo.text != '':
                        prop.bathrooms = property.PropertyFeatures.PropertyBathroomsNo.text
                    if property.PropertyFeatures.PropertyBedroomsNo.text != '':
                        prop.bedrooms = property.PropertyFeatures.PropertyBedroomsNo.text
                    if property.PropertyFeatures.PropertyCarsNo.text != '':
                        prop.carparks = property.PropertyFeatures.PropertyCarsNo.text

                    prop.property_class = property.PropertyFeatures.PropertyClass.text
                    prop.is_new_construction = property.PropertyFeatures.PropertyNewConstruction.text
                    prop.pets = property.PropertyFeatures.PropertyPetsAllowed.text
                    prop.smokers = property.PropertyFeatures.PropertySmokersAllowed.text

                    prop.agent_email1 = property.PropertyAgent.PropertyAgentEmail1.text
                    prop.agent_email2 = property.PropertyAgent.PropertyAgentEmail2.text
                    prop.agent_name = property.PropertyAgent.PropertyAgentFullName.text
                    prop.agent_mobile_num = property.PropertyAgent.PropertyAgentPhoneMobile.text
                    prop.agent_work_num = property.PropertyAgent.PropertyAgentPhoneWork.text

                    prop.rental_period = property.PropertyRentalPeriod.text
                    prop.rent = property.PropertyRentAmount.text
                    if property.PropertyFeatures.PropertyAdvertText.text != '':
                        garbage, prop.advert_text = property.PropertyFeatures.PropertyAdvertText.text.split('****')
                    else:
                        prop.advert_text = ''
                    prop.save()

                    images_xml = requests.get(
                        'https://serviceapi.realbaselive.com/Service.svc/RestService/AvailablePropertyImages/' +
                        property.PropertyCode.text, auth=(username, password), stream=True)
                    sauce = bs.BeautifulSoup(images_xml.text, 'xml')

                    for index, value in enumerate(sauce.find_all('AvailablePropertyImages')):
                        property_images = PropertyImage(property=prop)
                        image_data = base64.b64decode(value.PropertyImageBase64.text)

                        property_images.image = ContentFile(image_data, str(property.PropertyCode.text) + '_' + str(
                            index) + '*.jpg')
                        property_images.save()

                    if PropertyImage.objects.filter(property__code=property.PropertyCode.text):
                        image_thumbnail = PropertyImage.objects.filter(
                            property__code=property.PropertyCode.text).first()
                        image_url = image_thumbnail.image.url
                        print(image_url)
                        thumb_url = get_thumbnailer(image_thumbnail.image)['prop_image']
                        print(thumb_url)
                        prop.thumbnail = str(thumb_url)
                        prop.save()
    except requests.exceptions.RequestException as e:
        print(e)


@shared_task()
def send_email_task(topic, details, email):
    return send_mail(topic, details, email, ['yaquake@live.ru', ])
