from extractor import Extractor
from loggers.CsvLogger import CsvLogger
from models.Advertisement import Advertisement
from baseVisitor import Visitor


class DromVisitor(Visitor):
    def __init__(self, result_path: str):
        super().__init__()
        self.logger = CsvLogger(result_path, Advertisement.getColumns())
        self.extractor = Extractor(self.driver)
        self.result_path = result_path

    def parse_advertisement(self, url: str) -> Advertisement:
        self.driver.get(url)

        ad = Advertisement()
        self.extractor.fillAdvertisement(ad)

        return ad

    def parse(self) -> None:
        print("Start parsing...")
        page = 0
        count = 0
        while True:
            page += 1
            print(f'Parsing page {page} | Parsed: {count}')
            url = f'https://auto.drom.ru/all/page{page}'
            self.driver.get(url)

            ad_hrefs, ad_prices, ad_cities, ad_details = self.extractor.extract_listings(self.driver)

            for i in range(len(ad_hrefs)):
                ad = self.parse_advertisement(ad_hrefs[i])
                try:
                    ad.cost = int(ad_prices[i])
                except ValueError:
                    ad.cost = 0
                ad.city = ad_cities[i]
                if ad_details[i]:
                    ad.year = ad_details[i].year
                    ad.brand = ad_details[i].brand
                    ad.model = ad_details[i].model

                self.logger.save(ad)
                count += 1


if __name__ == "__main__":
    print("Initialize drom parser...")
    parser = DromVisitor("result2.csv")
    parser.parse()
