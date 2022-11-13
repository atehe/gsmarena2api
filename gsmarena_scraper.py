import requests, os, csv
from requests_ip_rotator import ApiGateway
from parsel import Selector
from urllib.parse import urljoin
from model import db_session, Brand, Device, DeviceSpecification


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
            f"================= Opening AWS Gateway for: {self.domain} ================="
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

        page_selector = Selector(text=response.text)

        brands = page_selector.xpath("//td")

        for brand in brands:

            brand_name = brand.xpath(".//a/text()").get()
            brand_id = brand.xpath(".//a/@href").get()
            num_devices = (
                brand.xpath(".//span/text()").get().replace("devices", "").strip()
            )
            brand_url = urljoin(self.domain, brand_id)

            scraped_brand = db_session.query(Brand).filter_by(name=brand_name).first()

            if scraped_brand:
                db_num_devices = scraped_brand.num_devices

                # checks if new devices in brand
                if int(num_devices) > int(db_num_devices):
                    print(f"Found new Device in Brand: {brand_name}")
                    scraped_brand.num_devices = num_devices
                    scraped_brand.update()
                else:
                    print(f"No new Device in Brand: {brand_name}")
                    continue
            else:
                new_brand = Brand(
                    id=brand_id, url=brand_url, name=brand_name, num_devices=num_devices
                )
                new_brand.insert()

            yield {
                "brand_name": brand_name,
                "brand_url": brand_url,
                "brand_id": brand_id,
            }

    def parse_brands(self):

        for brand in self.parse_gsmarena():

            brand_name = brand.get("brand_name")
            brand_url = brand.get("brand_url")
            brand_id = brand.get("brand_id")

            response = self.session.get(brand_url)

            print(f"[{response.status_code}] Parsing Brand: {brand_name}")

            page_selector = Selector(text=response.text)
            devices = page_selector.xpath('//div[@class="makers"]//li')

            for device in devices:
                device_id = device.xpath(".//a/@href").get()
                device_name = device.xpath(".//a//text()").get()
                device_url = urljoin(self.domain, device_id)

                device_thumbnail = device.xpath(".//img/@src").get()
                device_description = device.xpath(".//img/@title").get()

                scraped_device = db_session.query(Brand).filter_by(id=device_id).first()

                if scraped_device:
                    print(f"Device Already in Database: {device_name}")
                    continue
                else:
                    new_device = Device(
                        id=device_id,
                        brand_id=brand_id,
                        url=device_url,
                        name=device_name,
                        summary=device_description,
                        thumbnail=device_thumbnail,
                    )
                    new_device.insert()

                yield {
                    "device_name": device_name,
                    "device_url": device_url,
                    "device_id": device_id,
                }

    def parse_devices(self):
        for device in self.parse_brands():
            device_name = device.get("device_name")
            device_url = device.get("device_url")
            device_id = device.get("device_id")

            response = self.session.get(device_url)

            print(f"[{response.status_code}] Parsing Device: {device_name}")

            page_selector = Selector(response.text)
            tables = page_selector.xpath('//table[@cellspacing="0"]')

            specs = []

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

                    device_spec = DeviceSpecification(
                        device_id=device_id,
                        spec_category=specification_group,
                        specification=specification,
                        spec_value=specification_value,
                    )
                    specs.append(device_spec)

            db_session.add_all(specs)
            db_session.commit()
