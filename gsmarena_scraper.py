import requests
from requests_ip_rotator import ApiGateway
from parsel import Selector


def get_brands():
    response = requests.get("https://www.gsmarena.com/makers.php3")

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


for i in get_brands():
    print(i)
