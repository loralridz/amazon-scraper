import requests
from bs4 import BeautifulSoup
import openpyxl
from pathlib import Path
import pandas as pd
import time

headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'rtt': '600',
    'downlink': '1.5',
    'ect': '3g',
    'upgrade-insecure-requests': '1',
    'dnt': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://google.com',
    'accept-language': 'en-US,en;q=0.9,ur;q=0.8,zh-CN;q=0.7,zh;q=0.6',
}

API_KEY = 'c4d17514b3d4d5e426f576b7762adcad'


def writeFile(prods):
    df = pd.DataFrame(prods)
    df.to_csv('variation.csv', mode='a', index=False, header=False)


def get_request(url):
    payload = {'api_key': API_KEY, 'url': url, 'render': 'false'}
    r = requests.get('http://api.scraperapi.com', params=payload, timeout=80)
    return r


if __name__ == '__main__':

    # reading links file
    links = []
    df = pd.read_csv('/home/dev/pyy/scrap_asins/links.csv')
    for row in df.values:
        links.append(str(row[0]))

    products = []
    if len(links) > 0:
        print('Links fetched successfully.')
        for link in links:
            r = get_request(link)
            # time.sleep(5)
            if r.status_code == 200:
                text = r.text.strip()
                soup = BeautifulSoup(text, 'lxml')
            try:
                variation_color = soup.find("div", id='variation_color_name')
                variation_size = soup.find("div", id='variation_size_name')
                
                # product price
                price = soup.select('#priceblock_ourprice')[0].get_text()
                if price is None:
                    price = 0

                # variation in colors
                if variation_color is not None:
                    colors = variation_color.find_all("li")
                    # loop thru and store each with asin
                    for color in colors:
                        asin = color['data-defaultasin']
                        product = []
                        product.append(asin)
                        product.append(price)
                        products.append(product)
                        writeFile(products)
                        print(products)

                # variation in sizes
                if variation_size is not None:
                    sizes = variation_size.find_all("li")
                    # loop thru and store each with asin
                    for size in sizes:
                        asin = size['data-defaultasin']
                        product = []
                        product.append(asin)
                        product.append(price)
                        products.append(product)
                        writeFile(products)
                        print(products)
            except:
                print("Errror occured, can't get data!")