from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.http import HttpResponse
import json
from rest_framework.exceptions import ValidationError

@api_view(["GET"])
def Documentation(request):
    response_data = {
    
        "endpoints": [
            {
                "endpoint": "/geo-currency/",
                "description": "Converts the price from USD to the local currency based on the user's location.",
                "method": "GET",
                "example_response": {
                    "status": "success",
                    "data": {
                        "base": "USD",
                        "convertedTo": "NGN",
                        "rate": 1471.70463884,
                        "currency_symbol": "₦"
                    },
                    "user_location": {
                        "country": "Nigeria",
                        "countryCode": "NG",
                        "city": "Lagos"
                    }
                }
            },
            {
                "endpoint": "/geo-currency/{currency}/",
                "description": "Converts the price from the specified currency to the local currency based on the user's location.",
                "method": "GET",
                "parameters": {
                    "currency": "The currency code to convert from (e.g., EUR, GBP, JPY)."
                },
                "example_response": {
                    "status": "success",
                    "data": {
                        "base": "EUR",
                        "convertedTo": "NGN",
                        "rate": 1631.59510503,
                        "currency_symbol": "₦"
                    },
                    "user_location": {
                        "country": "Nigeria",
                        "countryCode": "NG",
                        "city": "Lagos"
                    }
                }
            }
        ],
        "live_url": "https://geo-currency-api.onrender.com"
    }

    return Response(response_data)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def locate_client(request):

    ip = get_client_ip(request)
   
    request = requests.get(f'http://ip-api.com/json/{ip}')
    location_data_one = request.text
    location_data = json.loads(location_data_one)

    return location_data

def country_code_and_currency_symbol(country_code):

    with open('core/countries.json', encoding="utf8") as f:
        data = json.load(f)
        for keyval in data:
            if country_code == keyval['isoAlpha2']:
                code = keyval['currency']['code']
                symbol = keyval['currency']['symbol']
                return [code, symbol]
                
    return [None, None]

def get_conversion_rate(client_currency, from_currency='USD'):

    request = requests.get(f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{from_currency.lower()}.json")
    if request.status_code == 200:
        response = request.json()

        country = country_code_and_currency_symbol(client_currency)

        conversion_rate = next((response[from_currency.lower()][i] for i in response[from_currency.lower()] if i.upper() == country[0].upper()), None)
            
        return conversion_rate, country, from_currency

    else:
        raise ValidationError({
            "status": "error",
            "message": f"An error occurred: {request.status_code} - {request.text}"
        })

@api_view(['GET'])
def get_currency_location_conversion_data(request):

    location_data = locate_client(request)
    conversion_rate, country_data, from_currency = get_conversion_rate(client_currency=location_data["countryCode"])

    return Response({
        "status": "success",
        "data": {
            "base": from_currency,
            "convertedTo": country_data[0],
            "rate": conversion_rate,
            "currency_symbol": country_data[1]
        },
        "user_location": {
            "country": location_data["country"],
            "countryCode": location_data["countryCode"],
            "city": location_data["city"]
        }
    })

@api_view(['GET'])
def get_currency_location_conversion_data_with_from_currency(request, from_currency):

    location_data = locate_client(request)

    conversion_rate, country_data, from_currency = get_conversion_rate(client_currency=location_data["countryCode"], from_currency=from_currency)

    return Response({
        "status": "success",
        "data": {
            "base": from_currency,
            "convertedTo": country_data[0],
            "rate": conversion_rate,
            "currency_symbol": country_data[1]
        },
        "user_location": {
            "country": location_data["country"],
            "countryCode": location_data["countryCode"],
            "city": location_data["city"]
        }
    })