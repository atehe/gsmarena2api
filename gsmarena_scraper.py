import requests
from requests_ip_rotator import ApiGateway
from parsel import Selector
import asyncio
from requests_html import AsyncHTMLSession


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


# for i in get_brands():
#     print(i)


async def send_requests(session, brand_dict):

    brand_name = brand_dict.get("brand_name")
    brand_url = brand_dict.get("brand_url")
    if not brand_url.startswith("https://"):
        brand_url = "http://www.gsmarena.com/" + brand_url.strip("/")
    resp = await session.get(brand_url)
    print(brand_name, resp.status_code, sep="--->")


async def test_gsmarena_async():
    session = AsyncHTMLSession()

    task = [send_requests(session, brand_dict) for brand_dict in get_brands()]

    return await asyncio.gather(*task)


asyncio.run(test_gsmarena_async())
