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
		convert_fields = ["latestPrice", "previousClose", "marketCap", "week52High", "week52Low"]
		ticker = Stock.objects.all()
		output = []
		total_net_worth = 0
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_062031d20883444f9ea74e2610fe2011")
			currency_rates_res = requests.get("https://api.exchangeratesapi.io/latest?base=USD")
			try:
				api = json.loads(api_request.content)
				currency_rates = currency_rates_res.json()
				cad_rate = currency_rates["rates"]["CAD"]
				for field in convert_fields:
					api[field] = round(api[field] * cad_rate, 2)
     
				api["shares_owned"] = ticker_item.shares_owned
				api["market_value"] = round(ticker_item.shares_owned * api["latestPrice"], 2)
				api["ytdChange"] *= 100
				total_net_worth += api["market_value"]
				output.append(api)
			except Exception as e:
				api = "Error..."
		
		return render(request, 'portfolio.html', {'ticker': ticker, 'output': output, 'total_net_worth': round(total_net_worth, 2)})


def delete(request, stock_id):
	try:
		item = Stock.objects.get(pk=stock_id)
		item.delete()
		messages.success(request, ("Stock Has Been Deleted!"))
	except Stock.DoesNotExist:
		messages.error(request, "Can't find stock!")
	return redirect(portfolio)



def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})