from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .forms import StockForm
from .apis import ExchangeRateAPI, IEXApi, CryptoAPI


def home(request):
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST["ticker"]
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/"
            + ticker
            + "/quote?token=pk_062031d20883444f9ea74e2610fe2011"
        )

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, "home.html", {"api": api})

    else:
        return render(
            request, "home.html", {"ticker": "Enter a Ticker Symbol Above..."}
        )


# def about(request):
# 	 return render(request, 'about.html', {})

exchange_api = ExchangeRateAPI("https://api.exchangeratesapi.io/latest?base=USD")
iexapi = IEXApi(
    "https://cloud.iexapis.com/stable/stock/{}/quote?token=pk_062031d20883444f9ea74e2610fe2011"
)
coins_api = CryptoAPI("https://api.coingecko.com/api/v3/coins/{}?market_data=true")


def portfolio(request):

    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            ticker_name = form.cleaned_data.get("ticker")
            if not iexapi.ticker_available(ticker_name):
                messages.error(
                    request, f"Couldn't find stock with ticker `{ticker_name}`!"
                )
                return redirect("portfolio")
            form.save()
            messages.success(request, ("Stock Has Been Added!"))
            return redirect("portfolio")

    else:
        ticker = Stock.objects.all()
        output = []
        total_net_worth = 0
        cad_rate = exchange_api.process_data()
        for ticker_item in ticker:
            try:
                ticker_data = iexapi.process_data(
                    {
                        "cad_rate": cad_rate,
                        "ticker": ticker_item.ticker,
                        "ticker_item": ticker_item,
                    }
                )
                total_net_worth += ticker_data["market_value"]
                output.append(ticker_data)
            except Exception as e:
                print(e.args)
                api = None

        return render(
            request,
            "portfolio.html",
            {
                "ticker": ticker,
                "output": output,
                "total_net_worth": round(total_net_worth, 2),
            },
        )


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
    return render(request, "delete_stock.html", {"ticker": ticker})
