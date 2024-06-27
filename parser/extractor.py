from typing import Optional
import re

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from models.Advertisement import Advertisement


class VehicleInfo:
    def __init__(self, brand: str, model: str, year: int):
        self.brand = brand
        self.model = model
        self.year = year


class Extractor:
    AdModelPattern = r"(\w+)\s+([\w\s]+),\s+(\d{4})"
    AdDatePattern = r"Объявление (\d+) от (\d{2}\.\d{2}\.\d{4})"
    EngineXPath = '//th[contains(text(),"Двигатель")]/following-sibling::td/span'
    HorsePowerXPath = '//th[contains(text(), "Мощность")]/following-sibling::td/span'
    GearXPath = '//th[contains(text(),"Привод")]/following-sibling::td'
    SWheelXPath = '//th[contains(text(),"Руль")]/following-sibling::td'
    ProbegXPath = '//th[contains(text(), "Пробег")]/following-sibling::td/span'
    DateBlockXPath = '//*[@class="css-pxeubi evnwjo70"]'

    VehicleInfoXPath = '//table'
    HrefsXPath = '//a[@data-ftid="bulls-list_bull"]'
    PricesXPath = '//span[@data-ftid="bull_price"]'
    LocationXPath = '//span[@data-ftid="bull_location"]'
    TitleXPath = '//div[@data-ftid="bull_title"]'

    LoadTimeout = 10000

    def __init__(self, driver: webdriver):
        self.driver = driver

    def fillAdvertisement(self, ad: Advertisement) -> None:
        block = EC.presence_of_element_located((By.XPATH, self.VehicleInfoXPath))
        vehicleInfo = WebDriverWait(self.driver, self.LoadTimeout).until(block)

        block2 = self.extract_field(self.driver, self.DateBlockXPath)

        adId, date = self.extract_ad_date(block2.text)

        ad.id, ad.date = adId, date
        ad.engine = self.extract_field(vehicleInfo, self.EngineXPath).text if self.extract_field(vehicleInfo, self.EngineXPath) else None
        ad.power = self.extractHorsePower(vehicleInfo)
        ad.gear = self.extract_field(vehicleInfo, self.GearXPath).text if self.extract_field(vehicleInfo, self.GearXPath) else None
        ad.sWheel = self.extract_field(vehicleInfo, self.SWheelXPath).text if self.extract_field(vehicleInfo, self.SWheelXPath) else None
        ad.probeg = self.extractProbeg(vehicleInfo)

    def extract_ad_model(self, car_string: str) -> Optional[VehicleInfo]:
        match = re.search(self.AdModelPattern, car_string)
        if match:
            brand = match.group(1)
            model = match.group(2).strip()
            year = int(match.group(3))

            return VehicleInfo(brand, model, year)
        return None

    def extract_ad_date(self, ad_string: str):
        match = re.search(self.AdDatePattern, ad_string)
        if match:
            ad_id = match.group(1)
            ad_date = match.group(2)
            return ad_id, ad_date
        else:
            return None, None

    def extract_listings(self, driver: webdriver) -> tuple[list[str], list[str], list[str], list[Optional[VehicleInfo]]]:
        hrefs = driver.find_elements(by=By.XPATH, value=self.HrefsXPath)
        prices = driver.find_elements(by=By.XPATH, value=self.PricesXPath)
        cities = driver.find_elements(by=By.XPATH, value=self.LocationXPath)
        title_elements = driver.find_elements(by=By.XPATH, value=self.TitleXPath)

        ad_hrefs = [elem.get_attribute('href') for elem in hrefs]
        ad_prices = [elem.text.replace(' ', '').replace('₽', '') for elem in prices]
        ad_cities = [elem.text for elem in cities]
        ad_details = [self.extract_ad_model(title_element.text) for title_element in title_elements]

        return ad_hrefs, ad_prices, ad_cities, ad_details

    def extract_field(self, driver: webdriver, xpath: str) -> Optional[WebElement]:
        try:
            return driver.find_element(By.XPATH, xpath)
        except Exception as ex:
            print(f"EXTRACT FIELD ERROR: {ex}")
            return None

    def extractHorsePower(self, driver: webdriver) -> Optional[int]:
        try:
            power_element = self.extract_field(driver, self.HorsePowerXPath)
            if power_element:
                power = power_element.text
                return int(power.split(' ')[0])
            return None
        except Exception as ex:
            print(f"EXTRACT HORSE POWER ERROR: {ex}")
            return None

    def extractProbeg(self, driver: webdriver) -> Optional[int]:
        try:
            probeg_element = self.extract_field(driver, self.ProbegXPath)
            if probeg_element:
                probegStr = probeg_element.text.replace('\xa0', '').replace('км', '').split(',')[0].replace(' ', '')
                return int(probegStr)
            return None
        except Exception as ex:
            print(f"EXTRACT PROBEG ERROR: {ex}")
            return None
