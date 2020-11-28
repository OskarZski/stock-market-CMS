from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .forms import StockForm
from .apis import ExchangeRateAPI, IEXApi, CryptoAPI
from .scraper import TheGlobeMailScarper


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
globe_scrapper = TheGlobeMailScarper()


def portfolio(request):

    if request.method == "POST":
        form = StockForm(request.POST or None)
        if form.is_valid():
            ticker_name = form.cleaned_data.get("ticker")
            currency_type = form.cleaned_data.get("currency_type")
            if currency_type == "stock":
                if (
                    not iexapi.ticker_available(ticker_name)
                    and globe_scrapper.check_availability(ticker_name) is None
                ):
                    messages.error(
                        request, f"Couldn't find stock with ticker `{ticker_name}`!"
                    )
                    return redirect("portfolio")

            elif currency_type == "crypto" and not coins_api.ticker_available(
                ticker_name
            ):
                messages.error(
                    request, f"Couldn't find cryptocurrency with name `{ticker_name}`!"
                )
                return redirect("portfolio")
            form.save()
            messages.success(request, ("Stock Has Been Added!"))
            return redirect("portfolio")

        else:
            messages.error(request, "Form data is invalid.")
            return redirect("portfolio")

    ticker = Stock.objects.all()
    output = []
    output_crypto = []
    stock_net_worth = 0
    crypto_net_worth = 0
    cad_rate = exchange_api.process_data()
    for ticker_item in ticker:
        try:
            if ticker_item.currency_type == "stock":
                if iexapi.ticker_available(ticker_item.ticker):
                    ticker_data = iexapi.process_data(
                        {
                            "cad_rate": cad_rate,
                            "ticker": ticker_item.ticker,
                            "ticker_item": ticker_item,
                        }
                    )
                    stock_net_worth += ticker_data["market_value"]
                    output.append(ticker_data)
                else:
                    fund_type = globe_scrapper.check_availability(ticker_item.ticker)
                    if fund_type == False:
                        messages.error(
                            request, f"Something wrong with {ticker_item.ticker}"
                        )
                        return redirect("portfolio")
                    else:
                        ticker_data = globe_scrapper.scrap_data(ticker_item, fund_type)
                        stock_net_worth += ticker_data["market_value"]
                        output.append(ticker_data)
            else:
                ticker_data = coins_api.process_data(
                    {"ticker": ticker_item.ticker, "ticker_item": ticker_item}
                )
                crypto_net_worth += ticker_data["market_value"]
                output_crypto.append(ticker_data)
        except Exception as e:
            print(e.args)

    return render(
        request,
        "portfolio.html",
        {
            "ticker": ticker,
            "ticker_stock": ticker.filter(currency_type="stock"),
            "ticker_crypto": ticker.filter(currency_type="crypto"),
            "output_stock": output,
            "output_crypto": output_crypto,
            "stock_net_worth": round(stock_net_worth, 2),
            "crypto_net_worth": round(crypto_net_worth, 2),
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
