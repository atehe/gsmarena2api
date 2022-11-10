import scrapy


class PhonesSpider(scrapy.Spider):
    name = "phones"
    start_urls = ["https://www.gsmarena.com/makers.php3"]

    def parse(self, response):
        brands = response.xpath("//td")
        for brand in brands:
            brand_name = brand.xpath(".//a/text()").get()
            num_devices = brand.xpath(".//span/text()").get()

            brand_url = brand.xpath(".//a/@href").get()
            brand_url = response.urljoin(brand_url)
            yield scrapy.Request(
                brand_url,
                callback=self.parse_brand,
                meta={
                    "brand_name": brand_name,
                    "num_devices": num_devices,
                },
            )

    def parse_brand(self, response):
        brand = response.meta.get("brand_name")
        num_devices = response.meta.get("num_devices")

        devices = response.xpath('//div[@class="makers"]//li')

        for device in devices:
            device_name = device.xpath(".//a//text()").get()
            device_url = device.xpath(".//a/@href").get()
            device_url = response.urljoin(device_url)

            device_thumbnail = device.xpath("//img/@src").get()
            device_description = device.xpath("//img/@title").get()

            yield scrapy.Request(
                device_url,
                callback=self.parse_device,
                meta={
                    "device_name": device_name,
                    "device_url": device_url,
                    "device_thumbnail": device_thumbnail,
                    "device_description": device_description,
                    "brand": brand,
                    "num_devices": num_devices,
                },
            )

    def parse_device(self, response):

        tables = response.xpath('//table[@cellspacing="0"]')

        for table in tables:
            specification_group = table.xpath(".//th/text()").get()

            specification_rows = table.xpath(".//tr")
            for row in specification_rows:
                specification = row.xpath('.//td[@class="ttl"]//text()').get()
                if not specification:
                    specification = "Other Information"
                specification_value = row.xpath(
                    './/td[@class="ttl"]/following-sibling::td//text()'
                ).get()

                spec_dict = {
                    "specification_group": specification_group,
                    "specification": specification,
                    "specification_value": specification_value,
                }

                full_phone_dict = response.meta | spec_dict

                yield full_phone_dict
