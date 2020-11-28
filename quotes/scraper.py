# Requires installing `selenium` and `webdriver_manager` via pip

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TheGlobeMailScarper:
    FUNDS_URL = "https://www.theglobeandmail.com/investing/markets/funds/{}/"
    STOCKS_URL = "https://www.theglobeandmail.com/investing/markets/stocks/{}/"

    def check_availability(self, symbol=None):
        if symbol is None:
            return False
        funds_check = requests.get(self.FUNDS_URL.format(symbol))
        if funds_check.status_code == 200:
            return True, "funds"
        stocks_check = requests.get(self.STOCKS_URL.format(symbol))
        if stocks_check.status_code == 200:
            return True, "stock"
        return False

    def scrap_data(self, symbol, type):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            options=chrome_options,
        )
        if type == "funds":
            driver.get(self.FUNDS_URL.format(symbol))
        else:
            driver.get(self.STOCKS_URL.format(symbol))

        last_price_el = driver.find_element_by_xpath(
            '//barchart-field[@name="lastPrice"]'
        )
        prev_price_el = driver.find_element_by_xpath(
            '//barchart-field[@name="previousPrice"]'
        )
        company_name_el = driver.find_element_by_xpath('//span[@id="instrument-name"]')
        symbol_el = driver.find_element_by_xpath('//span[@id="instrument-symbol"]')
        ytd_exchange_el = driver.find_element_by_xpath(
            '//td[@data-barchart-field="returnYtd"]'
        )

        ret = {
            "lastPrice": last_price_el.text,
            "previousClose": prev_price_el.text,
            "companyName": company_name_el.text,
            "symbol": symbol_el.text,
            "ytdChange": float(ytd_exchange_el.text.replace("%", "")) / 100,
        }

        driver.quit()

        return ret