import requests
from bs4 import BeautifulSoup
import openpyxl
from pathlib import Path
import pandas as pd

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


def get_request(asin):
    URL_TO_SCRAPE = f'https://www.amazon.com/s?k={asin}&ref=nb_sb_noss'
    payload = {'api_key': API_KEY, 'url': URL_TO_SCRAPE, 'render': 'false'}
    r = requests.get('http://api.scraperapi.com', params=payload, timeout=100)
    return r


def writeFile(items):
    df = pd.DataFrame(items)
    df.to_csv('links.csv', mode='a', index=False, header=False)


if __name__ == '__main__':

    # reading excel file
    list = []
    # Setting the path to the xlsx file:
    xlsx_file = Path("/home/dev/pyy/ASINTEST.xlsx")
    wb_obj = openpyxl.load_workbook(xlsx_file)
    sheet = wb_obj.active
    for row in sheet.iter_rows():
        for cell in row:
            list.append(cell.value)

    # get links
    links = []
    for asin in list:
        r = get_request(asin)
        if r.status_code == 200:
            text = r.text.strip()
            soup = BeautifulSoup(text, 'lxml')
            # find href of asin
            selector = 'div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.sg-col-4-of-20 > div > span > div > div > div > div:nth-child(1) > h2 > a'
            link = soup.select_one(selector)
            if link is not None:
                main_link = 'https://amazon.com'+str(link['href'])
                links.append(main_link)
                print(main_link)

    if len(links) > 0:
        writeFile(links)
        print('Links stored successfully.')
