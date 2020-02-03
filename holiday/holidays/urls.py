from django.urls import path
from . import views

urlpatterns = [
    path('<str:country_code>/<int:year>', views.index, name='index')
]