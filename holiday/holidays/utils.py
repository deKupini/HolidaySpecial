import urllib.request as urllib
import urllib.error as urlerror
from django.conf import settings
from .models import PublicHoliday, Country


class MissingHolidays:
    def __init__(self, country_code, year):
        self.country_code = country_code
        self.year = year
        self.ext_api = self._get_working_api()
        self.holidays = self.get_missing_holidays()

    def _get_working_api(self):
        for api in settings.HOLIDAY_EXT_APIS:
            try:
                urllib.urlopen(api['root'])
                return api
            except (urlerror.HTTPError, urlerror.URLError):
                pass
        return {}

    def get_missing_holidays(self):
        if not self.ext_api:
            return []
        holidays = []
        if self.ext_api['name'] == 'date_nager':
            holidays = self._get_missing_holidays_from_date_nager()
        return holidays

    def _get_missing_holidays_from_date_nager(self):
        csv_url = '%s%s/%s/%d/CSV' % (self.ext_api['root'], self.ext_api['rest'], self.country_code, self.year)
        try:
            response = urllib.urlopen(csv_url)
        except (urlerror.HTTPError, urlerror.URLError):
            return []
        holidays = []
        holidays_str = str(response.read(), 'utf-8')[62:-2]
        country_obj = Country.objects.get(code=self.country_code)
        for holiday in holidays_str.split('\r\n'):
            h = holiday.split(',')
            if not PublicHoliday.objects.filter(name=h[2]):
                holidays.append(PublicHoliday(name=h[2], local_name=h[1], holiday_date=h[0], country=country_obj))
        return holidays
