from django.test import TestCase

# Create your tests here.
import requests

response = requests.get('https://api.ipify.org?format=json')
ip_data = response.json()
external_ip = ip_data['ip']

print(f"External IP Address: {external_ip}")
