import logging
import asyncio
import sys
from datetime import datetime
import xml.etree.ElementTree as ET

import aiohttp


link = "http://api.nbp.pl/api/cenyzlota/today/?format=xml"

def parse_xml(xml_data):
    root = ET.fromstring(xml_data)
    for cena_zlota in root.findall('CenaZlota'):
        data = cena_zlota.find('Data').text
        cena = cena_zlota.find('Cena').text
        print(f"Data: {data}, Cena złota: {cena}")


async def get_price(date):
    if date:
        url = f"http://api.nbp.pl/api/cenyzlota/{date}/?format=xml"
    else:
        url = "http://api.nbp.pl/api/cenyzlota/?format=xml"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    parse_xml(data)
                else:
                    logging.error(f'Error status: {response.status}')

        except aiohttp.ClientConnectorError:
            logging.error(f'Connection error: {link}')
        except aiohttp.client_exceptions.InvalidURL as er:  # noqa
            logging.error(f'{link}')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        date = sys.argv[1]
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Error: The date should be in YYYY-MM-DD format.")
            sys.exit(1)
    else:
        date = None

    logging.basicConfig(level=logging.ERROR, format='%(message)s')
    asyncio.run(get_price(date))

