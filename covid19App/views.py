from django.shortcuts import render 
import requests

ac = None
# Create your views here.
def index(request):
    result = requests.get('https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true.')
    ac = result.json()['activeCases']
    return render(request, 'index1.html' , {'ac' : ac})
