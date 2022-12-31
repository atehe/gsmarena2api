# GSMArena2API
A minimalistic FastAPI implementation of [GSMArena](https://www.gsmarena.com/), reperesenting its data in json

#### About GSMArena
GSMArena is an online website that offers comprehensive and up-to-date mobile phone information.

The website offers information about various mobile brands, including Nokia, Samsung, Motorola, Sony, LG, and more. It enables its users to get to know about latest and real-time mobile phone trends and other related information. GSMArena’s blogoffers its users with articles about mobile phones and software, gaming applications, operating systems, social networks, web browsers, network operators, and many others.

GSMArena provides a comparison service that enables its users to compare mobile phones, photos and videos, battery life tables, and many other features. It also helps amateurs catch up with technical terms by providing a mobile terms glossary page.

**Source**: [Crunchbase](https://www.crunchbase.com/organization/gsmarena)

## Endpoints

- **Get Brands**

`/brands`: Returns all brands
```json
{
  "success": true,
  "total_brands": 123,
  "page": 1,
  "size": 10,
  "brands": [
    {
      "id": "acer-phones-59.php",
      "name": "Acer",
      "url": "https://www.gsmarena.com/acer-phones-59.php",
      "num_devices": 100
    },
    {
      "id": "alcatel-phones-5.php",
      "name": "alcatel",
      "url": "https://www.gsmarena.com/alcatel-phones-5.php",
      "num_devices": 407
    },
    ...,
  ]
}
```
- **Get Devices for Brand**

`brands/<brand_id>`: Returns all devices in a brand
```json
{
  "success": true,
  "total_devices": 111,
  "page": 1,
  "size": 10,
  "brand": {
    "id": "apple-phones-48.php",
    "name": "Apple",
    "url": "https://www.gsmarena.com/apple-phones-48.php",
  },
  "devices": [
    {
      "id": "apple_ipad_pro_12_9_(2022)-11939.php",
      "name": "iPad Pro 12.9 (2022)",
      "url": "https://www.gsmarena.com/apple_ipad_pro_12_9_(2022)-11939.php",
      "thumbnail": "https://fdn2.gsmarena.com/vv/bigpic/apple-ipad-pro-129-2022.jpg",
      "summary": "Apple iPad Pro 12.9 (2022) tablet. Announced Oct 2022. Features 12.9″  display, Apple M2 chipset, 10758 mAh battery, 2048 GB storage, 16 GB RAM, Scratch-resistant glass."
    },
    {
      "id": "apple_ipad_pro_11_(2022)-11940.php",
      "name": "iPad Pro 11 (2022)",
      "url": "https://www.gsmarena.com/apple_ipad_pro_11_(2022)-11940.php",
      "thumbnail": "https://fdn2.gsmarena.com/vv/bigpic/apple-ipad-pro-11-2022.jpg",
      "summary": "Apple iPad Pro 11 (2022) tablet. Announced Oct 2022. Features 11.0″  display, Apple M2 chipset, 7538 mAh battery, 2048 GB storage, 16 GB RAM, Scratch-resistant glass."
    },
    ...,
  ]
}
```

- **Get Specifications of Device**

`/devices/<device_id>`: Returns specifications for a device

```json
{
  "success": true,
  "total_devices": 112,
  "brand": {
    "id": "apple-phones-48.php",
    "name": "Apple",
    "url": "https://www.gsmarena.com/apple-phones-48.php",
  },
  "device": {
    "id": "apple_ipad_pro_11_(2022)-11940.php",
    "url": "https://www.gsmarena.com/apple_ipad_pro_11_(2022)-11940.php",
    "summary": "Apple iPad Pro 11 (2022) tablet. Announced Oct 2022. Features 11.0″  display, Apple M2 chipset, 7538 mAh battery, 2048 GB storage, 16 GB RAM, Scratch-resistant glass.",
    "name": "iPad Pro 11 (2022)",
    "thumbnail": "https://fdn2.gsmarena.com/vv/bigpic/apple-ipad-pro-11-2022.jpg",
  },
  "specifications": {
    "Network": {
      "Technology": "GSM / HSPA / LTE / 5G",
      "2G bands": "GSM 850 / 900 / 1800 / 1900 ",
      "3G bands": "HSDPA 850 / 900 / 1700(AWS) / 1900 / 2100 ",
      "4G bands": "1, 2, 3, 4, 5, 7, 8, 11, 12, 13, 14, 17, 18, 19, 20, 21, 25, 26, 28, 29, 30, 32, 34, 38, 39, 40, 41, 42, 46, 48, 66, 71 - A2435, A2761",
      " ": "1, 2, 3, 5, 7, 8, 12, 14, 20, 25, 26, 28, 29, 30, 38, 40, 41, 48, 66, 70, 71, 77, 78, 79 SA/NSA/Sub6 - A2761, A2762",
      "5G bands": "1, 2, 3, 5, 7, 8, 12, 14, 20, 25, 26, 28, 29, 30, 38, 40, 41, 48, 66, 70, 71, 77, 78, 79, 258, 260, 261 SA/NSA/Sub6/mmWave - A2435",
      "Speed": "HSPA, LTE-A, 5G"
    },
    "Launch": {
      "Announced": "2022, October 18",
      "Status": "Available. Released 2022, October 26"
    },
    "Body": {
      "Dimensions": "247.6 x 178.5 x 5.9 mm (9.75 x 7.03 x 0.23 in)",
      "Weight": "466 g (Wi-Fi), 470 g (5G) (1.03 lb)",
      "Build": "Glass front, aluminum back, aluminum frame",
      "SIM": "Nano-SIM and eSIM",
      " ": "Stylus support (Bluetooth integration; magnetic)"
    },
    "Display": {
      "Type": "Liquid Retina IPS LCD, 120Hz, HDR10, Dolby Vision, 600 nits (typ)",
      "Size": "11.0 inches, 366.5 cm",
      "Resolution": "1668 x 2388 pixels (~265 ppi density)",
      "Protection": "Scratch-resistant glass, oleophobic coating"
    }
  }
}

```

- **Get all devices**

`/devices`: Returns all devices
```json
{
  "success": true,
  "total_devices": 11500,
  "page": 1,
  "size": 10,
  "devices": [
    {
      "id": "acer_chromebook_tab_10-9139.php",
      "brand_id": "acer-phones-59.php",
      "name": "Chromebook Tab 10",
      "url": "https://www.gsmarena.com/acer_chromebook_tab_10-9139.php",
      "thumbnail": "https://fdn2.gsmarena.com/vv/bigpic/acer-chromebook-tab-10.jpg",
      "summary": "Acer Chromebook Tab 10 tablet. Announced Mar 2018. Features 9.7″  display, Rockchip RK3399 chipset, 5 MP primary camera, 2 MP front camera, 4500 mAh battery, 32 GB storage, 4 GB RAM."
    },
    {
      "id": "acer_iconia_talk_s-8306.php",
      "brand_id": "acer-phones-59.php",
      "name": "Iconia Talk S",
      "url": "https://www.gsmarena.com/acer_iconia_talk_s-8306.php",
      "thumbnail": "https://fdn2.gsmarena.com/vv/bigpic/acer-iconia-talk-s.jpg",
      "summary": "Acer Iconia Talk S Android tablet. Announced Aug 2016. Features 7.0″  display, MT8735 chipset, 13 MP primary camera, 2 MP front camera, 3400 mAh battery, 32 GB storage, 2 GB RAM."
    },
    {
      "id": "acer_liquid_z6_plus-8305.php",
      "brand_id": "acer-phones-59.php",
      "name": "Liquid Z6 Plus",
      "url": "https://www.gsmarena.com/acer_liquid_z6_plus-8305.php",
      "thumbnail": "https://fdn2.gsmarena.com/vv/bigpic/acer-liquid-z6-plus.jpg",
      "summary": "Acer Liquid Z6 Plus Android smartphone. Announced Aug 2016. Features 5.5″  display, MT6753 chipset, 13 MP primary camera, 5 MP front camera, 4080 mAh battery, 32 GB storage, 3 GB RAM."
    },
    ...,
  ]
}
```
**Optional Parameters**

- `page`: Page of API response
- `limit`: Number of result returned per page, default is 10






