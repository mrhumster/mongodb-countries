import json

import motor.motor_asyncio
import requests as requests

ME_CONFIG_MONGODB_URL = "mongodb://root:password@0.0.0.0:27017/"
client = motor.motor_asyncio.AsyncIOMotorClient(ME_CONFIG_MONGODB_URL)
database = client.city
city_collection = database.get_collection("countries")


async def add_country(country: dict) -> bool:
    await city_collection.insert_one(country)
    return True


async def get_all_countries():
    city_list = []
    cursor = city_collection.find()
    for city in await cursor.to_list(length=1000):
        city_list.append(city)
    return city_list


r = requests.get("https://restcountries.com/v3.1/all/")
loop = client.get_io_loop()

for data in r.json():
    loop.run_until_complete(add_country(data['name']))

countries = loop.run_until_complete(get_all_countries())
with open('countries.json', 'w') as f:
    json.dump(countries, f, default=str)
