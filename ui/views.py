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

    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers['Content-Type'],
    )

