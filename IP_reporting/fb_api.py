
# Block x script for Facebook API
### IP Reporting API ###

import requests
import json
from youtube.models import AppConfig
def get_additional_info(movie_name):
    appObj = AppConfig.objects.get(id=1)
    return appObj.ip_reporting_template.format(movie_name=movie_name)

def get_data(access_token, email, job, name, original_type, owner_country, owner_name, relationship, type,
             organization=None, relationship_other=None, address=None, original_urls=None, content_urls=None,
             additional_info=None, phone=None, tm=None, tm_jurisdiction=None, tm_reg_number=None, tm_url=None):
    data = {
        "email": email,
        "job": job,
        "name": "Shahul Hameed Mubeena",
        "original_type": original_type,
        "owner_country": owner_country,
        "owner_name": owner_name,
        "relationship": relationship,
        "type": type,
        "access_token": access_token
    }

    if additional_info is not None:
        data["additional_info"] = additional_info
    if address is not None:
        data["address"] = address
    if content_urls is not None: # array
        data["content_urls"] = str(content_urls).split()
    if organization is not None:
        data["organization"] = organization
    if original_urls is not None: # array
        data["original_urls"] = str(original_urls).split()
    if phone is not None:
        data["phone"] = phone
    if relationship_other is not None:
        data["relationship_other"] = relationship_other

    return data


def make_request(data):
    try:
        url = "https://graph.facebook.com/v12.0/ip_reporting?fields=report_id,report_type"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        return requests.post(url, headers=headers, data=json.dumps(data))
    except Exception as e:
        return str(e)
#
# if __name__ == '__main__':
#     movie_name = "Kalki 2898 AD (2024)"
#     access_token = ("EAANNzoa1UqQBO8aDlZAURIjz05ep75yJrAeZA6w8Hcd38g5ZAKYEtwyTsg0hroUpnGhQ5ZBwGBIZC9gHhwGQaZAc0g6Ce6LPBbiuWv2ZAVLjuacEZCadzIb6rzTwi83ZA3PIwsfEpmO2gsPTZBEqSLy0dn08IVZB1DaDaZBZBCiufpPjFRvKf8y2o3rihZBEZBG7QZDZD")
#     email = settings.bx_legal_email
#     job= "TEST"
#     name= settings.bx_name
#     original_type= "VIDEO" #PHOTO, VIDEO, ARTWORK, SOFTWARE, NAME, CHARACTER, OTHER
#     owner_country= "IN" # IN-india,
#     owner_name= "AGS Entertainment" # client name
#     relationship = "AGENT" #OWNER, COUNSEL, EMPLOYEE, AGENT, OTHER
#     type= "COPYRIGHT" #COPYRIGHT, TRADEMARK, COUNTERFEIT
#     content_urls= """https://www.fakework.com/example_1 https://www.fakework.com/example_2"""
#     organization = settings.bx_name
#     address = settings.bx_address
#     original_urls = ["https://en.m.wikipedia.org/wiki/Dragon_(upcoming_film)"]
#     additional_info = get_additional_info(movie_name)
#
#     # data = get_data(access_token, email, job, name, original_type, owner_country, owner_name, relationship, type,
#     #          content_urls, address, original_urls,additional_info)
#
#     data = get_data(access_token=access_token, email=email, job=job, name=name, original_type=original_type,
#                     owner_country=owner_country, owner_name=owner_name, relationship=relationship, type=type,
#              organization=organization, address=address, original_urls=original_urls, content_urls=content_urls)
#
#     response = make_request(data)
#     print(data)
#     print(response.status_code)
#     print(response.json())