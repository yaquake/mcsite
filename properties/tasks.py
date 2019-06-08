from __future__ import absolute_import, unicode_literals
import bs4 as bs
import requests
import base64

from celery import shared_task
from django.core.files.base import ContentFile
from easy_thumbnails.files import get_thumbnailer


# Get account details for getpalace.com API
def get_login_password():
    from properties.models import Palace

    palace = Palace.objects.first()
    return palace.login, palace.password


# Create a new properties or update an existing one
def property_update(property_data, state):
    from properties.models import Property

    # If the properties exists then get the object to update
    if state == 0:
        prop = Property.objects.filter(code=property_data.PropertyCode.text).first()
    else:
        prop = Property()

    prop.change_code = int(property_data.PropertyChangeCode.text)
    prop.publish_entry = property_data.PropertyPublishEntry.text
    if property_data.PropertyUnit.text:
        prop.unit = property_data.PropertyUnit.text
    else:
        prop.unit = ''
    prop.street_number = property_data.PropertyAddress1.text
    prop.street_name = property_data.PropertyAddress2.text

    if ' Auckland' in property_data.PropertyAddress3.text:
        prop.suburb = property_data.PropertyAddress3.text.replace(' Auckland', '')
    else:
        prop.suburb = property_data.PropertyAddress3.text

    if property_data.PropertyAddress4.text == '':
        prop.city = 'Auckland'
    if property_data.PropertyFeatures.PropertyPostCode.text != '':
        prop.postcode = property_data.PropertyFeatures.PropertyPostCode.text
    prop.code = property_data.PropertyCode.text
    prop.date_available = property_data.PropertyDateAvailable.text[:10]

    if property_data.PropertyFeatures.PropertyBathroomsNo.text != '':
        prop.bathrooms = property_data.PropertyFeatures.PropertyBathroomsNo.text
    if property_data.PropertyFeatures.PropertyBedroomsNo.text != '':
        prop.bedrooms = property_data.PropertyFeatures.PropertyBedroomsNo.text
    if property_data.PropertyFeatures.PropertyCarsNo.text != '':
        prop.carparks = property_data.PropertyFeatures.PropertyCarsNo.text

    prop.property_class = property_data.PropertyFeatures.PropertyClass.text
    prop.is_new_construction = property_data.PropertyFeatures.PropertyNewConstruction.text
    prop.pets = property_data.PropertyFeatures.PropertyPetsAllowed.text
    prop.smokers = property_data.PropertyFeatures.PropertySmokersAllowed.text

    prop.agent_email1 = property_data.PropertyAgent.PropertyAgentEmail1.text
    prop.agent_email2 = property_data.PropertyAgent.PropertyAgentEmail2.text
    prop.agent_name = property_data.PropertyAgent.PropertyAgentFullName.text
    prop.agent_mobile_num = property_data.PropertyAgent.PropertyAgentPhoneMobile.text
    prop.agent_work_num = property_data.PropertyAgent.PropertyAgentPhoneWork.text

    prop.rental_period = property_data.PropertyRentalPeriod.text
    prop.rent = property_data.PropertyRentAmount.text
    aster = '****'
    if property_data.PropertyFeatures.PropertyAdvertText.text != '':
        if aster in property_data.PropertyFeatures.PropertyAdvertText.text:
            splitted_text = property_data.PropertyFeatures.PropertyAdvertText.text.split(aster)
            prop.advert_text = splitted_text[-1]
        else:
            prop.advert_text = property_data.PropertyFeatures.PropertyAdvertText.text
    else:
        prop.advert_text = ''
    prop.save()

    update_images(property_data.PropertyCode.text)


# Update images for a particular properties
def update_images(property_code):
    from properties.models import PropertyImage, Property

    username, password = get_login_password()

    property = Property.objects.filter(code=property_code).first()

    images_xml = requests.get(
        'https://serviceapi.realbaselive.com/Service.svc/RestService/AvailablePropertyImages/' +
        property_code, auth=(username, password), stream=True)
    sauce = bs.BeautifulSoup(images_xml.text, 'xml')

    for index, value in enumerate(sauce.find_all('AvailablePropertyImages')):
        property_images = PropertyImage(property=property)
        image_data = base64.b64decode(value.PropertyImageBase64.text)

        property_images.image = ContentFile(image_data, str(property_code) + '_' + str(
            index) + '*.jpg')
        property_images.save()

    if PropertyImage.objects.filter(property__code=property_code):
        image_thumbnail = PropertyImage.objects.filter(
            property__code=property_code).first()
        image_url = image_thumbnail.image.url
        print(image_url)
        thumb_url = get_thumbnailer(image_thumbnail.image)['prop_image']
        print(thumb_url)
        property.thumbnail = str(thumb_url)
        property.save()


@shared_task()
def update_from_xml():
    from properties.models import Property

    username, password = get_login_password()

    try:
        if requests.get('https://serviceapi.realbaselive.com/Service.svc/RestService/AvailableProperties',
                        auth=(username, password)):

            property_list_xml = requests.get(
                                'https://serviceapi.realbaselive.com/Service.svc/RestService/AvailableProperties',
                                auth=(username, password))
            soup = bs.BeautifulSoup(property_list_xml.text, 'xml')

            # Delete all properties that were removed from getpalace.com
            for property_obj in Property.objects.all():
                if not soup.find_all(property_obj.code):
                    property_obj.delete()

            # Main task
            for property_data in soup.find_all('AvailableProperty'):
                if property_data.PropertyPublishEntry.text == 'Yes':
                    existing_property = Property.objects.filter(code=property_data.PropertyCode.text).first()
                    if existing_property:
                        # Check if the change_code was modified (it means that properties details were updated)
                        if existing_property.change_code != int(property_data.PropertyChangeCode.text):
                            # Execute property_update function with properties data as a payload
                            # (0 means that this properties exists in db)
                            property_update(property_data, 0)
                    # If we don't have this properties in our database then execute
                    # property_update function with properties data as a payload (1 means that this is a new properties
                    else:
                        property_update(property_data, 1)

                # If we have PublishEntry == 'No' in a particular properties payload then search for it
                # in our database to delete
                else:
                    existing_property = Property.objects.filter(code=property_data.PropertyCode.text).first()
                    if existing_property:
                        existing_property.delete()

    except requests.exceptions.RequestException as e:
        print(e)


# Send email
@shared_task()
def send_email_task(topic, details):
    from django.core import mail
    from info.models import EmailSettings

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


