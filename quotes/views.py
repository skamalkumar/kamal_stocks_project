from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .forms import StockForm

def home(request):
    import requests
    import json

    if request.method=='POST':

        ticker = request.POST['ticker']

        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_5aa5ffc4c1f348f68a47eb2130550df2")

        try:

            api = json.loads(api_request.content)

        except Exception as e:

            api = "Error..."
        return render(request,'home.html',{'api': api})



    else:

        return render(request,'home.html',{'ticker': "Please enter a symbol in the Get Stock Quote"})






    #pk_5aa5ffc4c1f348f68a47eb2130550df2



def about(request):
    return render(request,'about.html')


def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or none)

        if form.is_valid():
            form.save()
            messages.success(request,("stock has been added to portfolio"))
            return redirect('add_stock')

    else:
        ticker = Stock.objects.all()

        output = []

        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_5aa5ffc4c1f348f68a47eb2130550df2")

            try:

                api = json.loads(api_request.content)
                output.append(api)

            except Exception as e:

                api = "Error..."

        return render(request,'add_stock.html',{'ticker': ticker, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request,("stock has been deleted"))
    return redirect(delete_stock)

def donation(request):
    
    return render(request,'donation.html',)


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request,'delete_stock.html', {'ticker': ticker})
