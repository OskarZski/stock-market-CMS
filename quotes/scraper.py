# Requires installing `selenium` and `webdriver_manager` via pip

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TheGlobeMailScarper:
    FUNDS_URL = "https://www.theglobeandmail.com/investing/markets/funds/{}/"
    STOCKS_URL = "https://www.theglobeandmail.com/investing/markets/stocks/{}/"

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            options=self.chrome_options,
        )

    def check_availability(self, symbol=None):
        if symbol is None:
            return None
        funds_check = requests.get(self.FUNDS_URL.format(symbol))
        if funds_check.status_code == 200:
            return "funds"
        stocks_check = requests.get(self.STOCKS_URL.format(symbol))
        if stocks_check.status_code == 200:
            return "stock"
        return None

    def scrap_funds(self, ticker):
        self.driver.get(self.FUNDS_URL.format(ticker.ticker))
        last_price_el = self.driver.find_element_by_xpath(
            '//barchart-field[@name="lastPrice"]'
        )
        prev_price_el = self.driver.find_element_by_xpath(
            '//barchart-field[@name="previousPrice"]'
        )
        company_name_el = self.driver.find_element_by_xpath(
            '//span[@id="instrument-name"]'
        )
        symbol_el = self.driver.find_element_by_xpath('//span[@id="instrument-symbol"]')
        ytd_exchange_el = self.driver.find_element_by_xpath(
            '//td[@data-barchart-field="returnYtd"]'
        )

        self.driver.close()

        return {
            "latestPrice": last_price_el.text,
            "previousClose": prev_price_el.text,
            "companyName": company_name_el.text,
            "symbol": symbol_el.text,
            "ytdChange": float(ytd_exchange_el.text.replace("%", "")),
            "shares_owned": ticker.shares_owned,
            "market_value": float(ticker.shares_owned) * float(last_price_el.text),
        }

    def scrap_stock(self, ticker):
        self.driver.get(self.STOCKS_URL.format(ticker.ticker))
        last_price_el = self.driver.find_element_by_xpath(
            '//barchart-field[@name="lastPrice"]'
        )
        prev_price_el = self.driver.find_element_by_xpath(
            '//barchart-field[@name="previousPrice"]'
        )
        high_price_1y = self.driver.find_element_by_xpath(
            '//barchart-field[@name="highPrice1y"]'
        )
        low_price_1y = self.driver.find_element_by_xpath(
            '//barchart-field[@name="lowPrice1y"]'
        )
        company_name_el = self.driver.find_element_by_xpath(
            '//span[@id="instrument-name"]'
        )
        symbol_el = self.driver.find_element_by_xpath('//span[@id="instrument-symbol"]')

        self.driver.close()

        return {
            "latestPrice": last_price_el.text,
            "previousClose": prev_price_el.text,
            "companyName": company_name_el.text,
            "symbol": symbol_el.text,
            "week52Low": low_price_1y.text,
            "week52High": high_price_1y.text,
            "shares_owned": ticker.shares_owned,
            "market_value": float(ticker.shares_owned) * float(last_price_el.text),
        }

    def scrap_data(self, ticker, type):

        if type == "funds":
            return self.scrap_funds(ticker)
        else:
            return self.scrap_stock(ticker)
