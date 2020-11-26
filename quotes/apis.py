from dataclasses import dataclass
from datetime import date
import requests


@dataclass
class APIHandler:
    original_url: str
    post_data: dict = None
    data: dict = None
    updated: date = None

    def __post_init__(self):
        self.url = self.original_url

    def get(self):
        res = requests.get(self.url)
        if res.status_code == 404:
            raise HTTP404NotFound
        self.data = res.json()
        self.updated = date.today()
        return self.data

    def process_data(self, data=None):
        raise NotImplementedError


class ExchangeRateAPI(APIHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cad_rate = None

    def process_data(self, data="CAD"):
        if self.cad_rate is None or self.updated != date.today():
            self.get()
            self.cad_rate = self.data["rates"][data]
        return self.cad_rate


class IEXApi(APIHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.convert_fields = [
            "latestPrice",
            "previousClose",
            "marketCap",
            "week52High",
            "week52Low",
        ]

    def ticker_available(self, ticker):
        self.url = self.original_url.format(ticker)
        try:
            self.get()
        except HTTP404NotFound:
            return False
        return True

    def process_data(self, data=None):
        self.url = self.original_url.format(data["ticker"])
        self.get()
        self.data["ytdChange"] *= 100
        for field in self.convert_fields:
            self.data[field] = round(self.data[field] * data["cad_rate"], 2)
        self.data["shares_owned"] = data["ticker_item"].shares_owned
        self.data["market_value"] = round(
            data["ticker_item"].shares_owned * self.data["latestPrice"], 2
        )
        return self.data


class HTTP404NotFound(Exception):
    pass
