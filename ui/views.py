from json import loads

import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
ADDRESS = 'Avenida Plutarco, 69'


def index(request):
    session = requests.Session()
    response = session.get('https://www.lowi.es/')
    csrf_token = response.cookies['csrftoken']

    session.post(
        'https://www.lowi.es/configura-tu-compra/',
        data={
            'csrfmiddlewaretoken': csrf_token,
            'purchaseItems': '[{"index":0,"package_id":11}]',
            'hideBtnC2C': False,
            'product_selection': 'INSTALLATION',
        },
        allow_redirects=True,
        headers=dict(Referer='https://www.lowi.es/')
    )

    response = session.post(
        'https://www.lowi.es/geo/suggest/',
        data={
            'address': ADDRESS,
        },
        allow_redirects=True,
        headers=dict(Referer='https://www.lowi.es/')
    )
    response_dict = loads(response.content)
    if response_dict['status'] == 'OK':
        results = response_dict['results'][0]
        address_components = results['address_components']
        street_number = address_components[0]['short_name']
        street_id = address_components[1]['short_name']
        thoroughfare_type = address_components[2]['long_name']
        street = address_components[3]['long_name']
        province_id = address_components[6]['short_name']
        province = address_components[6]['long_name']
        town_id = address_components[7]['short_name']
        town = address_components[7]['long_name']

        response = session.post(
            'https://www.lowi.es/consulta-direccion/',
            data={
                "name": "",
                "email": "bar@bar.com",
                "phone": "627654233",
                "address": ADDRESS,
                "province": province,
                "provinceId": province_id,
                "town": town,
                "townId": town_id,
                "street": street,
                "thoroughfareType": thoroughfare_type,
                "streetId": street_id,
                "number": street_number,
            },
            allow_redirects=True,
            headers=dict(Referer='https://www.lowi.es/consulta-cobertura/')
        )
        response_dict = loads(response.content)

        if response_dict['address'][0]['horizontals'][0]['id_horizontal'] != 0:
            message = 'You have coverage in that address :D'
        else:
            message = 'You have NOT coverage in that address :('

        return render(request, 'ui/index.html', {'message': message})
    else:
        return render(request, 'ui/index.html', {'message': 'Something was wrong'})

    # return HttpResponse(
    #     content=response.content,
    #     status=response.status_code,
    #     content_type=response.headers['Content-Type'],
    # )

