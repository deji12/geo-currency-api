from  django.urls import path
from . import views

urlpatterns = [
    path('', views.get_currency_location_conversion_data),
    path('<str:from_currency>/', views.get_currency_location_conversion_data_with_from_currency)
]