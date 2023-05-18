from typing import List

import os 
from slack_sdk import WebhookClient 

import requests
from bs4 import BeautifulSoup

from pydantic import BaseModel

def send_message(msg):
    client = WebhookClient(os.environ['SLACK_API_TOKEN'])
    res = client.send(text=msg)

    assert res.status_code == 200
    assert res.body == 'ok'

class Apartment(BaseModel):
    title: str
    des: str
    availability: str
    price: str

url = 'https://www.baumhausapts.com/floorplans'
def get_apartments() -> List[Apartment]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.prettify())

    apartments = []
    for i, d in enumerate(soup.select('div.card')):
        title = d.find('h2')
        title = title.text.strip() if title else ''

        des = d.find('ul')
        des = ' '.join(des.text.strip().split()) if des else ''

        availability = d.find('span', attrs={'class': 'fp-availability'})
        availability = availability.text.strip() if availability else ''
        
        price = d.find('div', attrs={'class': 'p-2 fieldset bg-light border rounded d-flex flex-column align-items-center justify-content-center mb-2'})
        price = ' '.join(price.text.strip().split()) if price else ''

        print(title, des, availability, price)

        apartments.append(Apartment(
            title = title,
            des = des,
            availability = availability,
            price = price
        ))
    return apartments
