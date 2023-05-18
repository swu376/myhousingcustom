import os, ssl, random
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request
from slack_sdk import WebhookClient 
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List

def send_message(blocks):
    client = WebhookClient(os.environ['SLACK_API_TOKEN'])
    res = client.send(
        text='New Message',
        blocks=blocks
    )

    assert res.status_code == 200
    assert res.body == 'ok'

class Apartment(BaseModel):
    title: str
    des: str
    availability: str
    price: str

def get_res(url):
  username = os.environ.get('BRIGHTDATA_USERNAME')
  password = os.environ.get('BRIGHTDATA_PASSWORD')
  port = 22225
  session_id = random.random()
  super_proxy_url = ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' %
      (username, session_id, password, port))
  proxy_handler = urllib.request.ProxyHandler({
      'http': super_proxy_url,
      'https': super_proxy_url,
  })
  opener = urllib.request.build_opener(proxy_handler)
  return opener.open(url).read().decode('utf8')

def get_apartments(url = 'https://www.baumhausapts.com/floorplans') -> List[Apartment]:
    soup = BeautifulSoup(get_res(url), 'html.parser')

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
