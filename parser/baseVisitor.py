import os
import time
import pickle
from selenium import webdriver

basedir = os.path.abspath(os.path.dirname(__file__))


class Visitor:

    def __init__(self):
        self.__op = webdriver.FirefoxOptions()
        self.__op.add_argument("--no-sandbox")
        self.__op.add_argument("--disable-dev-shm-usage")
        self.__op.add_argument(f"--log-path=parser.log")
        self.driver = webdriver.Firefox()

    def close_parser(self):
        try:
            self.driver.close()
        except Exception as e:
            return e

    def create_session(self, url: str):
        try:
            self.driver.get(url=url)
            time.sleep(25)
            pickle.dump(self.driver.get_cookies(), open(f'sessions/cookie', 'wb'))
            print(f"session saved!")
        except Exception as e:
            return e
        finally:
            self.close_parser()

    def load_cookie(self, url: str):
        try:
            self.driver.get(url)
            for cookie in pickle.load(open(f'../sessions/cookie', 'rb')):
                self.driver.add_cookie(cookie)
            self.driver.get(url)
        except Exception as e:
            return e

