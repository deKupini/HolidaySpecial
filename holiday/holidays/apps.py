from django.apps import AppConfig
from django.conf import settings


class HolidaysConfig(AppConfig):
    name = 'holidays'

    def ready(self):
        from .models import Country, PublicHoliday
        from .utils import MissingHolidays
        holidays = []
        for country in settings.COUNTRIES:
            if not Country.objects.filter(name=country['name']):
                Country(name=country['name'], local_name=country['local_name'], code=country['code']).save()
            for year in settings.YEARS:
                holidays = MissingHolidays(country['code'], year).holidays
        if holidays:
            PublicHoliday.objects.bulk_create(holidays)
