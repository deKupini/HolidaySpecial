from django.shortcuts import render
from .models import PublicHoliday
from django.conf import settings


def index(request, country_code, year):
    holidays = PublicHoliday.objects.filter(country__code=country_code, holiday_date__year=year)
    context = {
        'holidays': holidays,
        'year': year,
        'country_code': country_code,
        'years': settings.YEARS,
        'countries': settings.COUNTRIES
    }
    return render(request, 'holidays/index.html', context)
