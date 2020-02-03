from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=64)
    local_name = models.CharField(max_length=64)
    code = models.CharField(max_length=3)


class PublicHoliday(models.Model):
    name = models.CharField(max_length=64)
    local_name = models.CharField(max_length=64)
    holiday_date = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
