import requests
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    session = requests.Session()
    response = session.get('https://www.lowi.es/')
    csrf_token = response.cookies['csrftoken']

    print(f'CSRF Token: {csrf_token}')
    response = session.post(
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
        'https://www.lowi.es/consulta-cobertura/',
        data={
            'csrfmiddlewaretoken': csrf_token,
            "name": "",
            "email": "bar@bar.com",
            "phone": "627654233",
            "address": "Avenida+Plutarco,+69,+Málaga,+España",
            "address_number": "69",
            "check-privacy-policy": "on",
            "legal_offer": "false",
            "province": "MALAGA",
            "province_id": "850000002",
            "town": "MALAGA",
            "town_id": "850000413",
            "postal_code": "29010",
            "stairwell": "",
            "name_street": "PLUTARCO",
            "number": "69",
            "floor": "1",
            "door": "B",
            "horizontal": "8510078790",
            "vertical": "851000000437236",
            "street": "850010014",
            "thoroughfare_type": "AV",
            "error": "false",
        },
        allow_redirects=True,
        headers=dict(Referer='https://www.lowi.es/consulta-cobertura/')
    )
    print(response.url)
    url = response.url
    if url.endswith('/datos-titular/'):
        message = 'Hay cobertura!'
    else:
        message = 'No hay cobertura :('

    return render(request, 'ui/index.html', {'message': message})
