from django.shortcuts import render


from coverage_checkers.exceptions import CoverageCheckError
from coverage_checkers.providers.lowi import LowiChecker

ADDRESS = 'Avenida Plutarco, 68, Málaga'


def index(request):
    checker = LowiChecker(ADDRESS)
    try:
        if checker.has_coverage():
            message = 'You have coverage in that address :D'
        else:
            message = 'You have NOT coverage in that address :('

        return render(request, 'ui/index.html', {'message': message})
    except CoverageCheckError:
        return render(request, 'ui/index.html', {'message': 'Something was wrong'})

    # return HttpResponse(
    #     content=response.content,
    #     status=response.status_code,
    #     content_type=response.headers['Content-Type'],
    # )
