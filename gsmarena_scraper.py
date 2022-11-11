import requests, os, csv
from requests_ip_rotator import ApiGateway
from parsel import Selector
from urllib.parse import urljoin
from multiprocessing import Pool


def dict_to_csv(data, file):
    try:
        with open(file, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
            if os.stat(file).st_size == 0:
                writer.writeheader()
            writer.writerow(data)

    except IOError:
        print("I/O error")


class GSMArenaScraper:
    def __init__(self, pool_size=4):
        self.domain = "https://www.gsmarena.com"
        self.pool_size = pool_size

    def open_aws_gateway(self, verbose=False):
        print(
            f"================= Starting AWS Gateway for: {self.domain} ================="
        )
        self.gateway = ApiGateway(self.domain, verbose=verbose)
        self.gateway.start()

        self.session = requests.Session()
        self.session.mount(self.domain, self.gateway)

    def close_aws_gateway(self):
        self.gateway.shutdown()
        print("Gateway Closed")

    def parse_gsmarena(self):
        response = self.session.get("https://www.gsmarena.com/makers.php3")

        page = Selector(text=response.text)

        brands = page.xpath("//td")

        for brand in brands:
            brand_name = brand.xpath(".//a/text()").get()
            brand_url = brand.xpath(".//a/@href").get()
            num_devices = brand.xpath(".//span/text()").get()

            yield {
                "brand_name": brand_name,
                "brand_url": brand_url,
                "num_devices": num_devices,
            }

    def parse_brands(self):

        for i, brand in enumerate(self.parse_gsmarena()):

            if i == 10:
                break
            brand_name = brand.get("brand_name")
            num_devices = brand.get("num_devices")
            brand_url = brand.get("brand_url")

            brand_url = urljoin(self.domain, brand_url)

            print(brand_name, num_devices, brand_url)

            response = self.session.get(brand_url)
            print(response.status_code, brand_url)

            response = Selector(text=response.text)

            devices = response.xpath('//div[@class="makers"]//li')

            for device in devices:
                device_name = device.xpath(".//a//text()").get()
                device_url = device.xpath(".//a/@href").get()

                device_thumbnail = device.xpath("//img/@src").get()
                device_description = device.xpath("//img/@title").get()

                yield {
                    "device_name": device_name,
                    "device_url": device_url,
                    "device_thumbnail": device_thumbnail,
                    "device_description": device_description,
                    "brand": brand,
                    "num_devices": num_devices,
                }

    def parse_devices(self):
        for device in self.parse_brands():
            device_name = device.get("device_name")
            device_url = device.get("device_url")

            device_url = urljoin(self.domain, device_url)

            response = self.session.get(device_url)
            print(response.status_code, device_name, device_url)

            response = Selector(response.text)
            tables = response.xpath('//table[@cellspacing="0"]')

            for table in tables:
                specification_group = table.xpath(".//th/text()").get()

                specification_rows = table.xpath(".//tr")
                for row in specification_rows:
                    specification = row.xpath('.//td[@class="ttl"]//text()').get()
                    if str(specification) == "0":
                        specification = "Other Information"
                    specification_value = row.xpath(
                        './/td[@class="ttl"]/following-sibling::td//text()'
                    ).get()

                    spec_dict = {
                        "specification_group": specification_group,
                        "specification": specification,
                        "specification_value": specification_value,
                    }

                    full_phone_dict = device | spec_dict

                    dict_to_csv(full_phone_dict, "testing.csv")


scraper = GSMArenaScraper()

scraper.open_aws_gateway()
scraper.parse_devices()
scraper.close_aws_gateway()

# scraper.test_class()


import datetime


# def f(arg):
#     print(arg**2)


# with Pool(20) as p:
#     start = datetime.datetime.now()

#     p.map(f, list(range(100000 * 100)))

#     print(start, datetime.datetime.now())


# # 2022-11-11 12:51:23.713634 2022-11-11 12:53:11.087937
