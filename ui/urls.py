from django.urls import path

from ui.views import index, check_coverage

urlpatterns = [
    path('', index),
    path('check_coverage/', check_coverage),
]
