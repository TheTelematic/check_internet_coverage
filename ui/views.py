from json import loads

import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


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
        'https://www.lowi.es/consulta-direccion/',
        data={
            "name": "",
            "email": "bar@bar.com",
            "phone": "627654233",
            "address": "Avenida+Plutarco,+69,+Málaga,+España",
            "province": "Málaga",
            "provinceId": "850000002",
            "town": "Málaga",
            "townId": "850000413",
            "street": "Plutarco",
            "thoroughfareType": "",
            "streetId": "",
            "number": "69"
        },
        allow_redirects=True,
        headers=dict(Referer='https://www.lowi.es/consulta-cobertura/')
    )
    response_dict = loads(response.content)

    if response_dict['address'][0]['horizontals'][0]['id_horizontal'] != 0:
        message = 'Hay cobertura!'
    else:
        message = 'No hay cobertura :('

    return render(request, 'ui/index.html', {'message': message})

    # return HttpResponse(
    #     content=response.content,
    #     status=response.status_code,
    #     content_type=response.headers['Content-Type'],
    # )

