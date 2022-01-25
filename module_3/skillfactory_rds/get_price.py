import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import sqlite3

if __name__ == '__main__':

    con = sqlite3.connect('main_task.db')
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE prices (id integer, price text)''')
    except:
        pass

    df = pd.read_csv('main_task.xls')

    price_update = {}
    threads = []

    cur.execute(f"SELECT * from prices")
    l_prices = cur.fetchall()
    l_ids = [x[0] for x in l_prices]

    for index, row in df[df['Price Range'].isna()].iterrows():

        url = f'https://www.tripadvisor.com{row["URL_TA"]}'

        while True:
            try:
                if index not in l_ids:
                    soup = BeautifulSoup(requests.get(url).text, 'lxml')
                    price = json.loads(soup.find_all('script', {'type': 'application/ld+json'})[0]
                                       .contents[0]).get('priceRange')

                    price_update[index] = price
                    cur.execute(f"INSERT INTO prices VALUES ({index}, '{price}')")
                    con.commit()

                    print(index, url)
                    break
                else:
                    break

            except:
                print(f'retrying {url}')

    con.close()
    print()

