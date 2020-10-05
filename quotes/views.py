#Copyright 2020 All Rights Reserved

from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm

def home(request):
    import requests
    import json

    if request.method == 'POST': #if user posts on homepage
        ticker = request.POST['ticker']#name of input of form. if we type google. ticker becomes google.
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_4283ca3d51574ede8e156536fafafe1d")
        #symbol request
        try:
            api = json.loads(api_request.content) #call api. json parse content
        except Exception as e: #if an error..
            api = "Error..."
        return render(request, 'home.html', {'api': api}) #else return api info

    else: #else if user didnt post.. return..
        return render(request, 'home.html', {'ticker': "Enter Ticker Symbol Above.."})


    

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added"))
            return redirect('add_stock')
    
    else:
        ticker = Stock.objects.all() #from model
        output = [] #create a list

        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_4283ca3d51574ede8e156536fafafe1d")
            try:
                api = json.loads(api_request.content)
                output.append(api) #we need to save the api data into out list
            except Exception as e:
                api = "Error..."
        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output}) #render the list

def delete(request, stock_id): #pass in stock id
    item = Stock.objects.get(pk=stock_id) #the item id number
    item.delete()
    messages.success(request, ("Stock has been deleted"))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})