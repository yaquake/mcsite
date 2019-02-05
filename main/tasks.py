from __future__ import absolute_import, unicode_literals
import bs4 as bs
import requests
import base64

from celery import shared_task, task, Celery
from django.core.files.base import ContentFile
from django.core.mail import send_mail, get_connection
from easy_thumbnails.files import get_thumbnailer


@shared_task()
def update_from_xml():
    from main.models import Property, PropertyImage, Palace

    palace = Palace.objects.first()
    username = palace.login
    password = palace.password

    try:
        if requests.get('https://serviceapi.realbaselive.com/Service.svc/RestService/AvailableProperties',
                        auth=(username, password)):

            property_list_xml = requests.get(
                                'https://serviceapi.realbaselive.com/Service.svc/RestService/AvailableProperties',
                                auth=(username, password))
            soup = bs.BeautifulSoup(property_list_xml.text, 'xml')

            for property in soup.find_all('AvailableProperty'):
                if property.PropertyPublishEntry.text == 'Yes':
                    existing_property = Property.objects.filter(code=property.PropertyCode.text).first()
                    if existing_property:
                        if existing_property.change_code != int(property.PropertyChangeCode.text):
                            existing_property.change_code = int(property.PropertyChangeCode.text)
                            existing_property.publish_entry = property.PropertyPublishEntry.text
                            existing_property.street_number = property.PropertyAddress1.text
                            existing_property.street_name = property.PropertyAddress2.text

                            if ' Auckland' in property.PropertyAddress3.text:
                                s = property.PropertyAddress3.text.replace(' Auckland', '')
                                existing_property.suburb = s
                            else:
                                existing_property.suburb = property.PropertyAddress3.text

                            if property.PropertyAddress4.text == '':
                                existing_property.city = 'Auckland'
                            if property.PropertyFeatures.PropertyPostCode.text != '':
                                existing_property.postcode = property.PropertyFeatures.PropertyPostCode.text
                            existing_property.code = property.PropertyCode.text
                            existing_property.date_available = property.PropertyDateAvailable.text[:10]

                            if property.PropertyFeatures.PropertyBathroomsNo.text != '':
                                existing_property.bathrooms = property.PropertyFeatures.PropertyBathroomsNo.text
                            if property.PropertyFeatures.PropertyBedroomsNo.text != '':
                                existing_property.bedrooms = property.PropertyFeatures.PropertyBedroomsNo.text
                            if property.PropertyFeatures.PropertyCarsNo.text != '':
                                existing_property.carparks = property.PropertyFeatures.PropertyCarsNo.text

                            existing_property.property_class = property.PropertyFeatures.PropertyClass.text
                            existing_property.is_new_construction = property.PropertyFeatures.PropertyNewConstruction.text
                            existing_property.pets = property.PropertyFeatures.PropertyPetsAllowed.text
                            existing_property.smokers = property.PropertyFeatures.PropertySmokersAllowed.text

                            existing_property.agent_email1 = property.PropertyAgent.PropertyAgentEmail1.text
                            existing_property.agent_email2 = property.PropertyAgent.PropertyAgentEmail2.text
                            existing_property.agent_name = property.PropertyAgent.PropertyAgentFullName.text
                            existing_property.agent_mobile_num = property.PropertyAgent.PropertyAgentPhoneMobile.text
                            existing_property.agent_work_num = property.PropertyAgent.PropertyAgentPhoneWork.text

                            existing_property.rental_period = property.PropertyRentalPeriod.text
                            existing_property.rent = property.PropertyRentAmount.text
                            aster = '****'
                            if property.PropertyFeatures.PropertyAdvertText.text != '':
                                if aster in property.PropertyFeatures.PropertyAdvertText.text:
                                    splitted_text = property.PropertyFeatures.PropertyAdvertText.text.split(aster)
                                    existing_property.advert_text = splitted_text[-1]
                                else:
                                    existing_property.advert_text = property.PropertyFeatures.PropertyAdvertText.text
                            else:
                                existing_property.advert_text = ''
                            existing_property.save()

                            images_xml = requests.get(
                                'https://serviceapi.realbaselive.com/Service.svc/RestService/AvailablePropertyImages/' +
                                property.PropertyCode.text, auth=(username, password), stream=True)
                            sauce = bs.BeautifulSoup(images_xml.text, 'xml')

                            for index, value in enumerate(sauce.find_all('AvailablePropertyImages')):
                                property_images = PropertyImage(property=existing_property)
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
                                existing_property.thumbnail = str(thumb_url)
                                existing_property.save()
                    else:
                        prop = Property()
                        prop.publish_entry = property.PropertyPublishEntry.text
                        prop.change_code = int(property.PropertyChangeCode.text)
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
                        # TODO: decide how to implement splitting in an advert text
                        aster = '****'
                        if property.PropertyFeatures.PropertyAdvertText.text != '':
                            if aster in property.PropertyFeatures.PropertyAdvertText.text:
                                splitted_text = property.PropertyFeatures.PropertyAdvertText.text.split(
                                    aster)
                                prop.advert_text = splitted_text[-1]
                            else:
                                prop.advert_text = property.PropertyFeatures.PropertyAdvertText.text
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
                else:
                    existing_property = Property.objects.filter(code=property.PropertyCode.text)
                    if existing_property:
                        existing_property.delete()

    except requests.exceptions.RequestException as e:
        print(e)


@shared_task()
def send_email_task(topic, details):
    from django.core import mail
    from main.models import EmailSettings

    try:
        email_settings = EmailSettings.objects.first()
        connection = mail.get_connection(
            host=email_settings.email_host,
            port=email_settings.email_port,
            username=email_settings.email_host_user,
            password=email_settings.email_host_password,
            use_ssl=email_settings.email_use_ssl,
        )
        connection.open()

        email_to_send = mail.EmailMessage(
            topic,
            details,
            from_email=email_settings.full_email,
            to=(email_settings.full_email,),
            connection=connection
        )
        email_to_send.send()
        connection.close()
        return True

    except Exception as _error:
        print('Error in sending mail >> {}'.format(_error))
        return False

    # return send_mail(topic, details, email, [email_settings.full_email, ])
