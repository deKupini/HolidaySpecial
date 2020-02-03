from django.test import TestCase
from .models import PublicHoliday, Country
from .utils import MissingHolidays
from django.test.utils import override_settings


class GetHolidaysTestCase(TestCase):

    def setUp(self):
        Country.objects.create(name='Poland', local_name='Polska', code='PL')

    def test_get_exisitng_holidays(self):
        holidays = MissingHolidays('PL', 2020).holidays
        self.assertIsInstance(holidays, list)
        self.assertEqual(len(holidays), 13)
        self.assertIsInstance(holidays[0], PublicHoliday)

    def test_get_not_existing_holidays(self):
        holidays = MissingHolidays('TT', 2020).holidays
        self.assertEqual(holidays, [])

    @override_settings(HOLIDAY_EXT_APIS=[])
    def test_without_defined_external_api(self):
        holidays = MissingHolidays('PL', 2020).holidays
        self.assertEqual(holidays, [])

    @override_settings(
        HOLIDAY_EXT_APIS=[{'root': 'https://date.wrong.at', 'rest': '/PublicHoliday/Country', 'name': 'date_nager'}])
    def test_without_working_external_api(self):
        holidays = MissingHolidays('PL', 2020).holidays
        self.assertEqual(holidays, [])

    @override_settings(
        HOLIDAY_EXT_APIS=[{'root': 'https://date.nager.at', 'rest': '/PublicHoliday/Country', 'name': 'date_bager'}])
    def test_without_proper_type_external_api(self):
        holidays = MissingHolidays('PL', 2020).holidays
        self.assertEqual(holidays, [])

    def test_with_all_holidays(self):
        holidays = MissingHolidays('PL', 2020).holidays
        PublicHoliday.objects.bulk_create(holidays)
        new_holidays = MissingHolidays('PL', 2020).holidays
        self.assertEqual(new_holidays, [])

    def test_with_lacking_holiday(self):
        holidays = MissingHolidays('PL', 2020).holidays
        PublicHoliday.objects.bulk_create(holidays[:-1])
        new_holidays = MissingHolidays('PL', 2020).holidays
        self.assertEqual(len(new_holidays), 1)
