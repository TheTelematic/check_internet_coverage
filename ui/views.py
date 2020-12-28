from django.http import JsonResponse
from django.shortcuts import render

from coverage_checkers.controllers import CheckerCoverageController
from coverage_checkers.exceptions import CoverageCheckError
from ui.forms import AddressForm

ADDRESS = 'Avenida Plutarco, 68, Málaga'


def index(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
    else:
        form = AddressForm()

    if form.is_valid():
        try:
            has_coverage = CheckerCoverageController.check_address(form.cleaned_data['address'])
            return render(request, 'ui/index.html', {
                'form': form,
                'status': 'OK',
                'has_coverage': has_coverage,
                'message': 'Checked',
            })

        except CoverageCheckError:
            return render(request, 'ui/index.html', {
                'form': form,
                'status': 'ERROR',
                'has_coverage': None,
                'message': 'Something was wrong',
            })

    return render(request, 'ui/index.html', {'form': form})


def check_coverage(request):
    # TODO: Take address from address
    address = ADDRESS

    try:
        has_coverage = CheckerCoverageController.check_address(address)
        return JsonResponse({'status': 'OK', 'has_coverage': has_coverage, 'message': 'foo'})

    except CoverageCheckError:
        return JsonResponse({'status': 'ERROR', 'has_coverage': None, 'message': 'bar'})
