import bs4 as bs
import requests

username = 'advert@mcdonaldpm.co.nz'
password = 'MCW@dvert$Pr0p291118'


property_list_xml = requests.get('https://serviceapi.realbaselive.com/Service.svc/RestService/AvailableProperties', auth=(username, password), stream=True)


prop = {}
all = {}
soup = bs.BeautifulSoup(property_list_xml.text, 'xml')

for property in soup.find_all('AvailableProperty'):
    prop['street_number'] = property.PropertyAddress1.text
    prop['street'] = property.PropertyAddress2.text
    prop['suburb'] = property.PropertyAddress3.text
    prop['city'] = property.PropertyAddress4.text
    prop['email1'] = property.PropertyAgent.PropertyAgentEmail1.text
    prop['email2'] = property.PropertyAgent.PropertyAgentEmail2.text
    prop['agent_name'] = property.PropertyAgent.PropertyAgentFullName.text
    prop['agent_phone_work'] = property.PropertyAgent.PropertyAgentPhoneWork.text
    prop['agent_phone_mobile'] = property.PropertyAgent.PropertyAgentPhoneMobile.text
    prop['rental_period'] = property.PropertyRentalPeriod.text
    prop['rent_amount'] = property.PropertyRentAmount.text
    prop['pets_allowed'] = property.PropertyFeatures.PropertyPetsAllowed.text
    prop['smoking_allowed'] = property.PropertyFeatures.PropertySmokersAllowed.text
    if property.PropertyFeatures.PropertyParking.text != '':
        prop['parking'] = property.PropertyFeatures.PropertyParking.text
    else:
        prop['parking'] = 'No'

    images_xml = requests.get('https://serviceapi.realbaselive.com/Service.svc/RestService/AvailablePropertyImages/' + property.PropertyCode.text, auth=(username, password), stream=True)
    sauce = bs.BeautifulSoup(images_xml.text, 'xml')

    for index, value in enumerate(sauce.find_all('AvailablePropertyImages')):
        prop['image' + str(index)] = index
    all[property.PropertyCode.text] = prop
    prop = {}


f = open('xml1.txt', 'w')
for key, value in all.items():
    f.write('{0}, {1}\n'.format(key, value))
f.close()
