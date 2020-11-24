from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
	import requests 
	import json 

	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_062031d20883444f9ea74e2610fe2011")      	

		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
		return render(request, 'home.html', {'api': api})

	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})

# def about(request):
# 	return render(request, 'about.html', {})


def portfolio(request):
	import requests 
	import json 

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			ticker_name = form.cleaned_data.get("ticker")
			api_response = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker_name}/quote?token=pk_062031d20883444f9ea74e2610fe2011")
			if api_response.status_code == 404:
				messages.error(request, f"Couldn't find stock with ticker `{ticker_name}`!")
				return redirect('portfolio')
			form.save()
			messages.success(request, ("Stock Has Been Added!"))
			return redirect('portfolio')

	else:	
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_062031d20883444f9ea74e2610fe2011")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."
		
		return render(request, 'portfolio.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted!"))
	return redirect(delete_stock)



def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})